from win32com.client import Dispatch
import timetappy
import PySimpleGUI as sg
import yaml

from collections import namedtuple
from contextlib import closing
from datetime import datetime
import pathlib
import sqlite3
import sys
import threading

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    key = str(config['key'])
    secret = config['secret']
    location = config['location']

# Initialize Dymo Printer
barcode_path = pathlib.Path('./Address Asset.label')
printer_com = Dispatch('Dymo.DymoAddIn')
if config.get('printer'):
    printer_com.SelectPrinter(config.get('printer'))
else:
    printer_com.SelectPrinter(printer_com.GetCurrentPrinterName())
printer_com.Open(barcode_path)
printer_label = Dispatch('Dymo.DymoLabels')


# Define Appointment Record type
class Appointment(namedtuple('Appointment', 'calendarId status subStatus emailAddress fullName dateOfBirth, printed')):
    @classmethod
    def convert_dateOfBirth(self, dateOfBirth: str) -> str:
        try:
            _ = dateOfBirth.split('-')  # Split the date of birth.
            return f'{_[1]}{_[-1]}{_[0]}'  # MMDDYYYY
        except Exception:
            return dateOfBirth


    @classmethod
    def from_sqlite(cls, calendarId, status, subStatus, emailAddress, fullName, dateOfBirth, printed):
        return cls(calendarId, status, subStatus, emailAddress, fullName, dateOfBirth, printed)

    @classmethod
    def from_dict(cls, d: dict):
        apt = {
            'calendarId': d['calendarId'],
            'status': d['status'],
            'subStatus': d['subStatus'],
            'emailAddress': d['client']['emailAddress'],
            'fullName': d['client']['fullName'],
            'dateOfBirth': Appointment.convert_dateOfBirth(d['client']['dateOfBirth']),
        }
        apt.update({'printed': 0})
        return cls(**apt)

    # Define row factory
    @classmethod
    def appointment_factory(cls, cursor, row):
        """Returns sqlite3 rows as Appointment objects"""
        # return Appointment(*row)
        return Appointment.from_sqlite(*row)


# Cleanup database
def cleanup_db(client: timetappy.Client, conn: sqlite3.Connection):
    with closing(conn.cursor()) as cur:
        print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Removing non-open appointments from the database...')
        rows = cur.execute("SELECT * FROM appointments ORDER BY emailAddress")
        updated = [Appointment.from_dict(client.get_appointment_by_id(row.calendarId)) for row in rows]
        to_delete = [(row.calendarId,) for row in updated if row.status != 'OPEN']
        cur.executemany(
            "DELETE FROM appointments WHERE calendarId = ?",
            to_delete
        )
        print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Finished removing non-open appointments from the database.')
        return


# Print labels
def print_labels(event_values):
    num_names_print = 0
    num_email_print = 0
    if event_values['ONE']:
        num_names_print = 1
    if event_values['TWO']:
        num_names_print = 2
    if event_values['THREE']:
        num_names_print = 3
    if event_values['EONE']:
        num_email_print = 1
    if event_values['ETWO']:
        num_email_print = 2
    if event_values['ETHREE']:
        num_email_print = 3
    if(printer_com.IsPrinterOnline(printer_com.GetCurrentPrinterName())):
        print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Printing labels to {printer_com.GetCurrentPrinterName()}')
        # Get all rows from database.
        rows = cursor.execute("SELECT * FROM appointments ORDER BY emailAddress").fetchall()
        for row in rows:
            if row.subStatus == 'CHECKEDIN':
                if row.printed == 0:
                    printer_label.SetField('Barcode', f'{row.fullName}\n{row.dateOfBirth}')
                    printer_label.SetField('Text', f'{row.fullName}\n{row.dateOfBirth}')

                    printer_com.StartPrintJob()
                    printer_com.Print(num_names_print, False)
                    printer_com.EndPrintJob()

                    printer_label.SetField('Barcode', f'{row.emailAddress}')
                    printer_label.SetField('Text', f'{row.emailAddress}')

                    printer_com.StartPrintJob()
                    printer_com.Print(num_email_print, False)
                    printer_com.EndPrintJob()
                    # Update the appointment to show we've already printed it.
                    cursor.execute("UPDATE appointments SET printed = ? WHERE calendarId = ?", (1, row.calendarId))
        print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Finished printing labels.')
    else:
        print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Printer Offline: {printer_com.GetCurrentPrinterName()}')


# Define window layout
layout = [
    [sg.Text('Print Appointment Client Labels')],
    [sg.MLine(size=(80, 5), k='-ML-', reroute_stdout=True, write_only=True, autoscroll=True, auto_refresh=True)],
    [sg.Radio('Print one name label', 1, default=True, key='ONE'), sg.Radio('Print two name labels', 1, key='TWO'), sg.Radio('Print three name labels', 1, key='THREE')],
    [sg.Radio('Print one email label', 2, default=True, key='EONE'), sg.Radio('Print two email labels', 2, key='ETWO'), sg.Radio('Print three email labels', 2, key='ETHREE')],
    [sg.Button('Sync'), sg.Button('Print Labels')],
]


if __name__ == "__main__":
    # Create app window
    window = sg.Window(title='Automatic Appointment Label Printer', layout=layout, finalize=True)
    # Define timeout for app
    # Get TimeTap API key and secret from environment variables
    # Initialize TimeTap API Client
    client = timetappy.Client(APIKey=key, PrivateKey=secret)
    # Open a database connection in memory
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    # Assign row factory
    conn.row_factory = Appointment.appointment_factory
    # Open a cursor
    cursor = conn.cursor()
    # Create table "Appointments"
    cursor.execute("CREATE TABLE appointments (calendarId INTEGER, status TEXT, subStatus TEXT, emailAddress TEXT, fullName TEXT, dateOfBirth TEXT, printed INTEGER)")
    event, values = window.read()
    while True:
        event, values = window.read(timeout=5000)
        # End the program if the users closes the window
        if event == sg.WIN_CLOSED:
            cursor.close()
            conn.close()
            window.close()
            sys.exit()
        # User clicked sync or 3 seconds without input passed.
        if event == 'Sync' or event == sg.TIMEOUT_KEY:
            # Get all appointments
            appointments = client.get_appointments_report(statusList=['OPEN'], pageSize=100)
            print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Checking TimeTap for latest appointments...')
            for a in appointments:
                if a['location']['locationId'] != location:
                    continue
                cursor.execute(
                    "SELECT * FROM appointments WHERE calendarId = ?",
                    (a['calendarId'],)
                )
                result = cursor.fetchone()
                if result:
                    # Record already exists
                    if result.subStatus != a['subStatus']:
                        cursor.execute(
                            "UPDATE appointments SET subStatus = ? WHERE calendarId = ?",
                            (a['subStatus'], result.calendarId)
                        )
                else:
                    cursor.execute(
                        "INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?)",
                        Appointment.from_dict(a)
                    )
            # Delete unneeded appointments
            if threading.active_count() < 3:  # Only if we don't already have a thread running.
                thread = threading.Thread(target=cleanup_db, args=(client, conn), daemon=True)
                thread.start()
            print_labels(values)
        if event == 'Print Labels':
            print_labels(values)
