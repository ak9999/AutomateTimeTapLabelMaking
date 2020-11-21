from .utils import return_response, api_get_request


class CalendarMixin():
    TIMETAP_API_CALENDAR_RANGE = '/calendar/range/'
    TIMETAP_API_CALENDAR_EVENT = '/calendar/event/'

    api_get_request = api_get_request

    @return_response
    def get_calendar_events_range(self, staffIdList: list):
        if not staffIdList:
            raise ValueError('staffIdList needs to be set to a list of `staffId`s')
        staffIdList = ','.join(map(str, staffIdList))
        return self.api_get_request(f'{self.TIMETAP_API_CALENDAR_RANGE}{staffIdList}')

    @return_response
    def get_calendar_event(self, eventType: str, eventId: int):
        if not eventType:
            raise ValueError('eventType needs to be a set to either "APPOINTMENT", "CLASS", "TIME_OFF", or "VACATION"')
        if not eventId:
            raise ValueError('eventId needs to be set to the numeric ID for an event')
        return self.api_get_request(f'{self.TIMETAP_API_CALENDAR_EVENT}{eventType}/{eventId}')
