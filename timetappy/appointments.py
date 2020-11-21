from .utils import return_response, api_get_request


class AppointmentsMixin():
    TIMETAP_API_APPOINTMENTS = '/appointments/'
    TIMETAP_API_APPOINTMENTS_REPORT = '/appointments/report'

    api_get_request = api_get_request

    @return_response
    def get_appointments_report(self, statusList: list = ['OPEN'], pageSize: int = 1, pageNumber: int = 1):
        params = {
            'statusList': statusList,
            'pageSize': pageSize,
            'pageNumber': pageNumber
        }
        return self.api_get_request(f'{self.TIMETAP_API_APPOINTMENTS_REPORT}', params=params)
    
    @return_response
    def get_appointment_by_id(self, calendarId):
        return self.api_get_request(f'{self.TIMETAP_API_APPOINTMENTS}{calendarId}')

    @return_response
    def get_locations(self):
        return self.api_get_request(f'{self.TIMETAP_API_LOCATIONS}')

    @return_response
    def get_staff(self):
        return self.api_get_request(f'{self.TIMETAP_API_STAFF}')
