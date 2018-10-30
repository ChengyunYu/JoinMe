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


def edit_event(user:UserModel, event: EventModel):
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

    sql = "INSERT INTO joins (joinid, eventid)" \
          "VALUES(%s, %s)"
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
        connector.rollback()
        if not handled:
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
