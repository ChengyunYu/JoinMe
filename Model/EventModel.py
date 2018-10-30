from Constants.Constants import Tags
import datetime


class EventModel:
    def __init__(self, eid, title, tags: [Tags], description, image, hosts: [str], attendees: [str], event_date,
                 location, register_period):
        self.eid = eid
        self.title = title
        self.tags = tags
        self.description = description
        self.image = image
        self.hosts = hosts
        self.attendees = attendees
        self.event_date = event_date
        self.location = location
        self.register_period = register_period
        self.expire_date = self.calculate_date(event_date, register_period)

    def calculate_date(self, initial_date, register_period):
        cur_date = [int(x) for x in initial_date.strip().split('-')]
        d1 = datetime.date(cur_date[0], cur_date[1], cur_date[2])
        d = d1 + datetime.timedelta(days=int(register_period))
        year = str(d.year)
        month = str(d.month).zfill(2)
        date = str(d.day).zfill(2)
        return year + '-' + month + '-' + date
