from Controller.SqlController import *
from Model.EventModel import EventModel
from Model.UserModel import UserModel
from Constants.Constants import Errors
import datetime


def add_event(user: UserModel, event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    handled = False

    sql = "INSERT INTO event " \
          "(title, tags, eventdate, description, image, location, expiretime) " \
          "VALUES " \
          "(%s, %s, %s, %s, %s, %s,%s)"
    val = (event.title, event.tags, event.event_date,
           event.description, event.image, event.location, event.expire_date)
    try:
        cursor.execute(sql, val)
        connector.commit()
        handled = True
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        handled = True
        return Errors.DUPLICATE.name
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name

    cursor.execute("SELECT @@identity")
    for x in cursor:
        event_id = x[0]
    return event_id


def edit_event(event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    handled = False

    sql = "UPDATE event " \
          "SET title = %s, tags = %s, eventdate = %s, description = %s, " \
          "image = %s, location = %s, expiretime = %s " \
          "WHERE eventid = %s"
    val = (event.title, event.tags, event.event_date, event.description, event.image,
           event.location, event.expire_date, event.eid)

    try:
        cursor.execute(sql, val)
        connector.commit()
        if cursor.rowcount == 0:
            handled = True
            return Errors.MISSING.name
        else:
            handled = True
            return Errors.SUCCESS.name
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name


def expire():
    connector = SqlController().sql_connector
    cursor = connector.cursor()

    today = datetime.date.today()
    cur_year = str(today.year)
    cur_month = str(today.month).zfill(2)
    cur_day = str(today.day).zfill(2)
    expire_date = cur_year+'-'+cur_month+'-'+cur_day
    sql = "DELETE FROM event WHERE expiretime < %s"
    val = [expire_date]
    try:
        cursor.execute(sql, val)
        connector.commit()
        return cursor.rowcount
    finally:
        connector.rollback()
        return Errors.FAILURE.name


def remove_user(user: UserModel, event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()

    sql = "DELETE FROM joins WHERE joinid = %s and eventid = %s"
    val = (user.uid, event.eid)
    try:
        cursor.execute(sql, val)
        connector.commit()
        return cursor.rowcount
    finally:
        connector.rollback()
        return Errors.FAILURE.name


def join_event(user: UserModel, event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    handled = False

    sql = "INSERT INTO JoinTable (JoinID, EventID)" \
          "VALUES (%s, %s)"
    val = (user.uid, event.eid)

    try:
        cursor.execute(sql, val)
        connector.commit()
        event.attendees.append(user.uid)
        user.join_events.append(event.eid)
        handled = True
        return user.uid, event.eid
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        handled = True
        return Errors.DUPLICATE.name
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name


def host_event(user: UserModel, event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    handled = False

    sql = "INSERT INTO Host (hostid, eventid)" \
          "VALUES(%s, %s)"
    val = (user.uid, event.eid)

    try:
        cursor.execute(sql, val)
        connector.commit()
        handled = True
        return event.eid, user.uid
    except mysql.connector.errors.IntegrityError as err:
        if not handled:
            print(err.msg)
            handled = True
            return Errors.DUPLICATE.name
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name


def get_hosted_event(user: UserModel):
    events = []
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    sql = "SELECT eventid " \
          "FROM host "\
          "WHERE hostid = %s"
    val = [user.uid]

    try:
        cursor.execute(sql, val)
        event_list = cursor.fetchone()
        if not event_list:
            return events
        for result in event_list:
            events.append(result[0])
        return events
    except mysql.connector.errors as err:
        print(err.msg)
        return Errors.FAILURE.name
    finally:
        connector.rollback()
        return Errors.FAILURE.name


def retrieve_event(event_id: str):
    handled = False
    connector = SqlController().sql_connector
    cursor = connector.cursor()

    sql = "SELECT * " \
          "FROM event " \
          "WHERE eventid = %s"
    val = [int(event_id)]

    try:
        cursor.execute(sql, val)
        event_info = cursor.fetchone()
        if not event_info:
            handled = True
            return Errors.MISSING.name
        else:
            handled = True
            return_event = decode_string_event(str(event_info))
            return_event.hosts = get_host(return_event.eid)
            return_event.attendees = get_join(return_event.eid)
            return return_event
    except mysql.connector.errors as err:
        print(err.msg)
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name


def decode_string_event(event_info: str):
    event_info = event_info[1: -1]
    field_list = event_info.split(',')
    eid = field_list[0]
    event_title = field_list[1][2: -1]
    tags = field_list[2][2: -1]
    event_date = decode_date(field_list[3] + ',' + field_list[4] + ',' + field_list[5])
    description = field_list[6][2: -1]
    image = field_list[7][2: -1]
    location = field_list[8][2: -1]
    expire_date = decode_date(field_list[9] + ',' + field_list[10] + ',' + field_list[11])

    decoded_event = EventModel(eid, event_title, tags, description, image, None,
                               [], event_date, location, 0)
    decoded_event.expire_date = expire_date
    return decoded_event


def decode_date(date_time: str):
    date_time = date_time[15: -1]
    date_list = date_time.split(',')
    return date_list[0] + '-' + date_list[1][1:] + '-' + date_list[2][1:]


def print_event(event: EventModel):
    if not event:
        print('This event is empty. \n')
    if type(event) == str:
        print(event)
        print()
    else:
        print('eid: ' + str(event.eid))
        print('title: ' + event.title)
        print('tags: ' + event.tags)
        print('description: ' + event.description)
        print('image: ' + event.image)
        print('hosts: ' + str(event.hosts))
        print('attendees: ' + str(event.attendees))
        print('event date: ' + event.event_date)
        print('location: ' + event.location)
        print('expire date: ' + event.expire_date)
        print()


def get_host(event_id: str):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    got = False

    sql = 'SELECT HostID '\
          'FROM Host ' \
          'WHERE EventID = %s'
    val = [event_id]

    try:
        cursor.execute(sql, val)
        host = cursor.fetchone()
        got = True
        return str(host[0])
    finally:
        if not got:
            return None


def get_join(event_id: str):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    got = False
    result = []

    sql = 'SELECT HostID '\
          'FROM JoinTable ' \
          'WHERE EventID = %s'
    val = [event_id]

    try:
        cursor.execute(sql, val)
        join = cursor.fetchall()
        for attendee in join:
            result.append(str(attendee[0]))
        got = True
        return result
    finally:
        if not got:
            return []
