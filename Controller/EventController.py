from Controller.SqlController import *
from Model.EventModel import EventModel
from Model.UserModel import UserModel
from Constants.Constants import Errors
import datetime


def post_event(user: UserModel, event: EventModel):
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
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        handled = True

    cursor.execute("SELECT @@identity")
    for x in cursor:
        event_id = x[0]

    sql = "INSERT INTO host (hostid, eventid)" \
          "VALUES(%s, %s)"
    val = (user.uid, event_id)

    try:
        cursor.execute(sql, val)
        connector.commit()
        return event_id
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        handled = True
    finally:
        connector.rollback()
        if not handled:
            return Errors.FAILURE.name
        else:
            return Errors.DUPLICATE.name


def edit_event(event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()

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
            return Errors.MISSING.name
        else:
            return Errors.SUCCESS.name
    finally:
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

    sql = "INSERT INTO joins (joinid, eventid)" \
          "VALUES(%s, %s)"
    val = (user.uid, event.eid)

    try:
        cursor.execute(sql, val)
        connector.commit()
        event.attendees.append(user.uid)
        user.join_events.append(event.eid)
        return user.uid, event.eid
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        handled = True
    finally:
        connector.rollback()
        if not handled:
            return Errors.FAILURE.name
        else:
            return Errors.DUPLICATE.name


def host_event(user: UserModel, event: EventModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    handled = False

    sql = "INSERT INTO host (hostid, eventid)" \
          "VALUES(%s, %s)"
    val = (user.uid, event.eid)

    try:
        cursor.execute(sql, val)
        connector.commit()
        event.hosts.append(user.uid)
        user.host_events.append(event.eid)
        return user.uid, event.eid
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        handled = True
    finally:
        connector.rollback()
        if not handled:
            return Errors.FAILURE.name
        else:
            return Errors.DUPLICATE.name


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


def get_hosted_event(user: UserModel):
    events = []
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    sql = "SELECT eventid " \
          "FROM joins "\
          "WHERE joinid = %s"
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
