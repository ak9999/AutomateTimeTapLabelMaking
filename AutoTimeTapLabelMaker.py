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

# Initialize Dymo Printer
barcode_path = pathlib.Path('./Address Asset.label')
printer_com = Dispatch('Dymo.DymoAddIn')
if config.get('printer'):
    printer_com.SelectPrinter(config.get('printer'))
else:
    printer_com.SelectPrinter(printer_com.GetCurrentPrinterName())
    pass
printer_com.Open(barcode_path)
printer_label = Dispatch('Dymo.DymoLabels')


# Define Appointment Record type
class Appointment(namedtuple('Appointment', 'calendarId status subStatus emailAddress fullName dateOfBirth')):
    @classmethod
    def convert_dateOfBirth(self, dateOfBirth: str) -> str:
        _ = dateOfBirth.split('-')  # Split the date of birth.
        return f'{_[1]}{_[-1]}{_[0][-2:]}'  # MMDDYY

    @classmethod
    def from_sqlite(cls, calendarId, status, subStatus, emailAddress, fullName, dateOfBirth):
        return cls(calendarId, status, subStatus, emailAddress, fullName, dateOfBirth)

    @classmethod
    def from_dict(cls, d: dict):
        apt = {
            'calendarId': d['calendarId'],
            'status': d['status'],
            'subStatus': d['subStatus'],
            'emailAddress': d['client']['emailAddress'],
            'fullName': d['client']['fullName'],
            'dateOfBirth': Appointment.convert_dateOfBirth(d['client']['dateOfBirth'])
        }
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


# Define window layout
layout = [
    [sg.Text('Print Appointment Client Labels')],
    [sg.MLine(size=(80, 5), k='-ML-', reroute_stdout=True, write_only=True, autoscroll=True, auto_refresh=True)],
    [sg.Button('Manual Sync'), sg.Button('Print Labels')],
]


if __name__ == "__main__":
    # Create app window
    window = sg.Window(title='Automatic Appointment Label Printer', layout=layout)
    # Define timeout for app
    timeout = thread = None
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
    cursor.execute("CREATE TABLE appointments (calendarId INTEGER, status TEXT, subStatus TEXT, emailAddress TEXT, fullName TEXT, dateOfBirth TEXT)")
    while True:
        event, values = window.read(timeout=3000)
        # End the program if the users closes the window
        if event == sg.WIN_CLOSED:
            cursor.close()
            conn.close()
            window.close()
            sys.exit()
        # User clicked sync or 3 seconds without input passed.
        if event == 'Manual Sync' or event == sg.TIMEOUT_KEY:
            # Get all appointments
            appointments = client.get_appointments_report(statusList=['OPEN'], pageSize=99999)
            print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Checking TimeTap for latest appointments...')
            for a in appointments:
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
                        "INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?)",
                        Appointment.from_dict(a)
                    )
            # Delete unneeded appointments
            if threading.active_count() < 3:  # Only if we don't already have a thread running.
                thread = threading.Thread(target=cleanup_db, args=(client, conn), daemon=True)
                thread.start()
        if event == 'Print Labels':
            # Print out data to text for looking at data
            if(printer_com.IsPrinterOnline(printer_com.GetCurrentPrinterName())):
                print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Printing labels to {printer_com.GetCurrentPrinterName()}')
                rows = cursor.execute("SELECT * FROM appointments ORDER BY emailAddress").fetchall()
                for row in rows:
                    if row.subStatus == 'CHECKEDIN':
                        printer_label.SetField('Barcode', f'{row.fullName}\n{row.dateOfBirth}')
                        printer_label.SetField('Text', f'{row.fullName}\n{row.dateOfBirth}')

                        printer_com.StartPrintJob()
                        printer_com.Print(1, False)
                        printer_com.EndPrintJob()

                        printer_label.SetField('Barcode', f'{row.emailAddress}')
                        printer_label.SetField('Text', f'{row.emailAddress}')

                        printer_com.StartPrintJob()
                        printer_com.Print(1, False)
                        printer_com.EndPrintJob()
                print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Finished printing labels.')
            else:
                print(f'[{datetime.now().strftime("%I:%M:%S %p")}] Printer Offline: {printer_com.GetCurrentPrinterName()}')
