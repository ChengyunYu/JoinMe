import mysql.connector
from flask import Blueprint
from Model.UserModel import UserModel
from Controller.SqlController import SqlController
from Constants.Constants import Errors


user_controller = Blueprint('user_controller', __name__)


@user_controller.route("/Controller")
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
        return 'Success'
    except mysql.connector.errors.IntegrityError as err:
        print(err.msg)
        if not handled:
            handled = True
            return Errors.DUPLICATE.name

    finally:
        connector.rollback()
        if not handled:
            return Errors.FAILURE.name


@user_controller.route("/Controller")
def edit_user(user: UserModel):
    connector = SqlController().sql_connector
    cursor = connector.cursor()

    sql = "UPDATE user " \
          "SET realname = %s, nickname = %s, gender = %s, location = %s, " \
          "email = %s, tags = %s, selfdescription = %s " \
          "WHERE email = %s"

    val = (user.name, user.nickname, user.gender, user.location, user.email,
           user.tags, user.description, user.email)
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


@user_controller.route("/Controller")
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
            return str(user_info)
    except mysql.connector.errors as err:
        print(err.msg)
    finally:
        if not handled:
            connector.rollback()
            return Errors.FAILURE.name

def delete_user(user_nick_name: str, user_email: str):
	handled = False
	connector = SqlController().sql_connector
	cursor = connector.cursor()

	sql = "DELETE " \
		  "FROM user " \
		  "WHERE nickname = %s AND email = %s" 
	val = (user_nick_name, user_email)
	try:
		cursor.execute(sql, val)
		connector.commit()
		handled = True
		return "SUCCESS"
	except mysql.connector.errors as err:
		print(err.msg)
	finally:
		if not handled:
			connector.rollback()
			return Errors.FAILURE.name