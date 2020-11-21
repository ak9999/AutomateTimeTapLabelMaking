from timetappy.appointments import AppointmentsMixin
from timetappy.locations import LocationsMixin
from timetappy.staff import StaffMixin
from timetappy.calendar import CalendarMixin
from timetappy.clients import ClientsMixin
from timetappy.services import ServicesMixin
from timetappy.auth import TimeTapAuthentication


class Client(AppointmentsMixin, LocationsMixin, StaffMixin, CalendarMixin, ClientsMixin, ServicesMixin):
    TIMETAP_BASE_URL_LIVE = "https://api.timetap.com/live"
    TIMETAP_BASE_URL_TEST = "https://api.timetap.com/test"

    def __init__(self, APIKey: str, PrivateKey: str, Testing=False):
        self.key = APIKey
        self.secret = PrivateKey
        self.testing = Testing
        self.base_url = self.TIMETAP_BASE_URL_LIVE if not self.testing else self.TIMETAP_BASE_URL_TEST
        self.token = TimeTapAuthentication(self.key, self.secret, None).get_authorization_header()

    def __repr__(self):
        return f'{type(self).__name__}(APIKey={self.key!r}, PrivateKey={self.secret!r}, Testing={self.testing!r})'
