from .utils import return_response, api_get_request


class ServicesMixin():
    TIMETAP_API_SERVICES = '/services'

    api_get_request = api_get_request

    @return_response
    def get_services(self):
        return self.api_get_request(f'{self.TIMETAP_API_SERVICES}')
