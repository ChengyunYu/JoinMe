import mysql.connector
from Model.UserModel import UserModel
from Controller.SqlController import SqlController
from Constants.Constants import Errors


def add_user(user: UserModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()
    handled = False

    sql = "INSERT INTO user " \
          "(realname, nickname, gender, location, email, tags, selfdescription) " \
          "VALUES " \
          "(%s, %s, %s, %s, %s, %s,%s)"
    val = (user.name, user.nickname, user.gender,
           user.location, user.email, user.tags, user.description)
    try:
        cursor.execute(sql, val)
        connector.commit()
        handled = True
        return Errors.SUCCESS.name
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        if not handled:
            handled = True
            return Errors.DUPLICATE.name

    finally:
        connector.rollback()
        if not handled:
            return Errors.FAILURE.name


def edit_user(user: UserModel):
    handled = False
    connector = SqlController().sql_connector
    cursor = connector.cursor()

    sql = "UPDATE user " \
          "SET realname = %s, nickname = %s, gender = %s, location = %s, " \
          "email = %s, tags = %s, selfdescription = %s " \
          "WHERE userid = %s"

    val = (user.name, user.nickname, user.gender, user.location, user.email,
           user.tags, user.description, user.uid)
    try:
        cursor.execute(sql, val)
        connector.commit()
        handled = True
        if cursor.rowcount == 0:
            return Errors.MISSING.name
        else:
            return user.uid
    finally:
        connector.rollback()
        if not handled:
            return Errors.FAILURE.name


def retrieve_user(field: str, value: str):
    handled = False
    connector = SqlController().sql_connector
    cursor = connector.cursor()

    sql = "SELECT * " \
          "FROM user " \
          "WHERE {field} = %s".format(field=field)
    val = [value]

    try:
        cursor.execute(sql, val)
        user_info = cursor.fetchone()
        if not user_info:
            handled = True
            return Errors.MISSING.name
        else:
            handled = True
            return decode_string(str(user_info))
    except mysql.connector.errors as err:
        print(err.msg)
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name


def decode_string(user_info: str):
    user_info = user_info[1: -1]
    field_list = user_info.split(',')
    field_list[0] = field_list[0][1: -1]
    field_list[1] = field_list[1][2: -1]
    field_list[2] = field_list[2][2: -1]
    field_list[3] = field_list[3][2: -1]
    field_list[4] = field_list[4][2: -1]
    field_list[5] = field_list[5][2: -1]
    field_list[6] = field_list[6][2: -1]
    field_list[7] = field_list[7][1:]

    decoded_user = UserModel(field_list[0], field_list[1], field_list[2], field_list[3], field_list[4], field_list[5],
                             field_list[6], field_list[7], [], [])
    return decoded_user



