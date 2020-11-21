from .utils import return_response, api_get_request


class StaffMixin():
    TIMETAP_API_STAFF = '/staff'

    api_get_request = api_get_request

    @return_response
    def get_staff(self):
        return self.api_get_request(f'{self.TIMETAP_API_STAFF}')

    @return_response
    def get_staff_by_professionalId(self, professionalId: int):
        if not professionalId:
            raise ValueError('professionalId has not been set')
        return self.api_get_request(f'{self.TIMETAP_API_STAFF}/{professionalId}')

    @return_response
    def get_service_staff(self, professionalId: int):
        if not professionalId:
            raise ValueError('professionalId has not been set')
        return self.api_get_request(f'{self.TIMETAP_API_STAFF}/{professionalId}/serviceStaff')
