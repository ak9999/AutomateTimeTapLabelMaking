from .utils import return_response, api_get_request


class LocationsMixin():
    TIMETAP_API_LOCATIONS = '/locations'

    api_get_request = api_get_request

    @return_response
    def get_locations(self):
        return self.api_get_request(f'{self.TIMETAP_API_LOCATIONS}')
