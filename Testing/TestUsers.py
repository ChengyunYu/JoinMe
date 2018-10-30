from flask import Flask
from Controller.SqlController import sql_controller
from Controller import UserController
from Constants.Constants import UserFields
from Model.UserModel import UserModel

app = Flask(__name__)
app.register_blueprint(sql_controller, url_prefix='/Controllers')


@app.route("/")
# TODO: Replace the placeholder for main function with test cases.
def test_retrieve_hit():
    user_one = UserModel('0',
                         'chengyun yu',
                         'yuche',
                         'male',
                         'cy2468@columbia.edu',
                         '0,0',
                         'sports, dining',
                         'i am a sports guy who likes to eat. '
                         )
    user_two = UserModel('0',
                         'chengyun yu',
                         'yuche',
                         'male',
                         'cy2468@columbia.edu',
                         '0,0',
                         'sports, dining',
                         'this is my new description. '
                         )
    user_three = UserModel('0',
                           'non existent',
                           'noext',
                           'male',
                           'non_existent@email.com',
                           '0.0',
                           'sports, dining',
                           'i am a sports guy who does not exist. '
                           )

    print("Insert New: " + UserController.add_user(user_one))
    print("Insert Conflict: " + UserController.add_user(user_two))
    print("Update: " + UserController.edit_user(user_two))
    print("Retrieve Hit: " + UserController.retrieve_user(UserFields.email.name, user_two.email))
    print("Retrieve Miss: " + UserController.retrieve_user(UserFields.email.name, user_three.email))
    return 'Tests Finished'


if __name__ == "__main__":
    app.run()
