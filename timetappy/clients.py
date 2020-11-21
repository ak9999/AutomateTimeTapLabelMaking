from .utils import return_response, api_get_request


class ClientsMixin():
    TIMETAP_API_CLIENTS = '/clients'

    api_get_request = api_get_request

    @return_response
    def get_clients(self, clientId: int = None, order_field: str = None, order_mode: str = None,
                    pageNumber: int = 1, pageSize: int = 1):
        params = {
            'clientId': clientId, 'order_field': order_field,
            'order_mode': order_mode, 'pageNumber': pageNumber, 'pageSize': pageSize
        }
        return self.api_get_request(f'{self.TIMETAP_API_CLIENTS}', params=params)

    @return_response
    def get_clients_by_id(self, clientId: int = None):
        return self.api_get_request(f'{self.TIMETAP_API_CLIENTS}/{clientId}')

    @return_response
    def get_clients_count(self):
        return self.api_get_request(f'{self.TIMETAP_API_CLIENTS}/count')
