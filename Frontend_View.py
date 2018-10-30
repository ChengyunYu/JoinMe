from tkinter import *
from tkinter import ttk
import Controller.EventController as EventController
import Controller.UserController as UserController
from Model.EventModel import EventModel as EventModel
from Model.UserModel import UserModel as UserModel
from Constants.Constants import Errors
from Constants.Constants import UserFields

current_event: UserModel = None
current_user: UserModel = None


def read_event():
    eid = 0
    event_title = str(title_input.get())
    tags = str(tags_input.get())
    description = str(description_input.get())
    image = str(image_input.get())
    hosts = None
    attendees = []
    event_date = str(event_date_input.get())
    location = str(location_input.get())
    register_period = str(period_input.get())

    new_event = EventModel(eid, event_title, tags, description, image, hosts, attendees, event_date,
                           location, register_period)
    return new_event


def read_user():
    uid = 0
    real_name = str(realname_input.get())
    nickname = str(nickname_input.get())
    gender = str(gender_input.get())
    email = str(email_input.get())
    location = str(user_location_input.get())
    tags = user_tags_input.get()
    description = user_description_input.get()
    host_events = []
    join_events = []

    new_event = UserModel(uid, real_name, nickname, gender, email, location, tags, description,
                          host_events, join_events)
    return new_event


def post_event():
    global current_event
    global current_user
    current_event = read_event()
    if not current_user:
        add_output("You have to login first! \n")
    else:
        result = EventController.add_event(current_user, current_event)
        if result == Errors.DUPLICATE.name:
            current_event.eid = None
            add_output("A same event already exists! \n")
        elif result == Errors.FAILURE.name:
            current_event.eid = None
            return_failure()
        add_output('Event #' + str(result) + ' has been posted. \n')
        current_event.eid = result

        result = EventController.host_event(current_user, current_event)
        if result == Errors.DUPLICATE.name:
            current_event.eid = None
            add_output("You have already hosted this event! \n")
        elif result == Errors.FAILURE.name:
            current_event.eid = None
            return_failure()
        add_output("You are the host of event " + str(current_event.eid) + " now. \n")
        current_event.hosts = current_user.uid
        current_user.host_events.append(current_event.eid)
        print('User #' + current_event.hosts + ' posted event #' + str(current_event.eid) + '. \n')
        EventController.print_event(current_event)
    return


def update_event():
    global current_event
    global current_user
    event_id = event_id_input.get()
    current_event = read_event()
    current_event.eid = event_id
    host_id = None
    temp_event = EventController.retrieve_event(event_id)
    if temp_event == Errors.MISSING.name:
        add_output('No such event. \n')
        current_event = None
        return
    if type(temp_event) == type(current_event):
        host_id = str(EventController.retrieve_event(event_id).hosts)
    if current_user.uid != host_id:
        add_output('You have to be the owner to update event #' + event_id + ' . \n')
        current_event = None
        return

    result = EventController.edit_event(current_event)

    if result == Errors.MISSING.name:
        add_output('No such event exists. \n')
        current_event = None
        EventController.print_event(current_event)
        return
    elif result == Errors.SUCCESS.name:
        add_output('Event #' + event_id + ' changed. \n')
        current_event = EventController.retrieve_event(event_id)
        EventController.print_event(current_event)
    else:
        add_output('Update failed, please try again. \n')
        current_event = None
        EventController.print_event(current_event)
        return


def remove_user():
    print('remove')
    return


def register():
    global current_user
    current_user = read_user()
    result = UserController.add_user(current_user)
    if result == Errors.DUPLICATE.name:
        add_output("A user with the same credentials already exists! \n")
        current_user = None
    elif result == Errors.FAILURE.name:
        return_failure()
        current_user = None
    else:
        add_output("User registered JoinMe with email " + current_user.email + ". \n")
        current_user = UserController.retrieve_user(UserFields.email.name, current_user.email)
    UserController.print_user(current_user)
    return


def update_profile():
    global current_user
    if not current_user:
        add_output("You have to login first! \n")
        return
    temp = UserController.retrieve_user(UserFields.email.name, current_user.email)
    if temp == Errors.MISSING.name:
        add_output("No user with such credentials exists. \n")
        return
    elif temp == Errors.FAILURE.name:
        return_failure()
        return
    user_id = current_user.uid
    current_user = read_user()
    current_user.uid = user_id

    result = UserController.edit_user(current_user)
    if result == Errors.MISSING.name:
        add_output("No user with such credentials exists. \n")
        current_user = temp
    elif result == Errors.FAILURE.name:
        return_failure()
        current_user = temp
    elif result == Errors.DUPLICATE.name:
        add_output("A user with the same credentials already exists! \n")
        current_user = temp
    else:
        add_output("User updated. Email now at: " + current_user.email + ". \n")
        current_user = UserController.retrieve_user(UserFields.userid.name, result)
    UserController.print_user(current_user)
    return


def login():
    global current_user
    email = user_email_input.get()
    result = UserController.retrieve_user(UserFields.email.name, email)
    if result == Errors.MISSING.name:
        add_output("No user with such credential exists. \n")
        UserController.print_user(current_user)
        return
    elif result == Errors.FAILURE.name:
        add_output("Failed to login. Please try again. \n")
        UserController.print_user(current_user)
        return
    add_output("You logged in with email " + email + ". \n")
    current_user = UserController.retrieve_user(UserFields.email.name, email)
    UserController.print_user(current_user)
    return


def log_out():
    global current_user
    current_user = None
    text.set(value="This is the first iteration demo for JoinMe. \n")


def group_email():
    return


def invite_friend():
    return


def add_output(line: str):
    global text
    text.set(text.get() + line)


def return_failure():
    add_output("Connection failed. Please try again. \n")


def join_event():
    global current_event
    global current_user
    event_id = event_id_input.get()
    current_event = EventController.retrieve_event(event_id)
    if current_event == Errors.MISSING.name:
        add_output('Event not found. \n')
        current_event = None
        return
    elif current_event == Errors.FAILURE.name:
        add_output('Failed to join event. \n')
        current_event = None
        return
    if not current_user:
        add_output('You have to login first to join events. \n')
        current_event = None
        return

    result = EventController.join_event(current_user, current_event)
    if result == Errors.DUPLICATE.name:
        add_output('You have already joined the event. \n')
    elif result == Errors.FAILURE.name:
        return_failure()
        current_event = None
        return
    else:
        add_output('You have joined event #' + current_event.eid + '. User ID: ' + current_user.uid + '. \n')

    EventController.print_event(current_event)
    return


window = Tk()
window.title('JoinMe')
window.geometry('1000x660')
title = Label(window, text='JoinMe',)
title.config(font='Helvetica -20 bold', fg='black')
title.place(x=375, y=20, anchor="center")

# ------------------------------------------- Event -------------------------------------------

Event_title = Label(window, text='Title:')
Event_title.place(x=90, y=30)
title_input = Entry(window, relief='ridge', width=50)
title_input.place(x=170, y=30)

Event_Description = Label(window, text='Description:')
Event_Description.place(x=90, y=60)
description_input = Entry(window, relief='ridge', width=50)
description_input.place(x=170, y=60)

Event_Tags = Label(window, text='Tags:')
Event_Tags.place(x=90, y=90)

tags_input = Entry(window, relief='ridge', width=50)
tags_input.place(x=170, y=90)

Event_image = Label(window, text='Image URL:')
Event_image.place(x=90, y=120)
image_input = Entry(window, relief='ridge', width=50)
image_input.place(x=170, y=120)

Event_event_date = Label(window, text='Event Date:')
Event_event_date.place(x=90, y=150)
event_date_input = Entry(window, relief='ridge', width=50)
event_date_input.place(x=170, y=150)

Event_location = Label(window, text='Location:')
Event_location.place(x=90, y=180)
location_input = Entry(window, relief='ridge', width=50)
location_input.place(x=170, y=180)

Event_period = Label(window, text='Time Period:')
Event_period.place(x=90, y=210)
period_input = Entry(window, relief='ridge', width=50)
period_input.place(x=170, y=210)

post_button = Button(window, text="Post Event", command=post_event)
post_button.place(x=90, y=242.5)

update_button = Button(window, text="Update Event", command=update_event)
update_button.place(x=170, y=242.5)


Event_id_join = Label(window, text='Event ID:')
Event_id_join.place(x=260, y=242.5)

event_id_input = Entry(window, relief='ridge', width=10)
event_id_input.place(x=320, y=240.5)

join_button = Button(window, text="Join Event", command=join_event)
join_button.place(x=420, y= 243.5)

Event_user = Label(window, text='User ID:')
Event_user.place(x=180, y=270)
user_id_input = Entry(window, relief='ridge', width=10)
user_id_input.place(x=240, y=270)

remove_button = Button(window, text="Remove User", command=remove_user)
remove_button.place(x=90, y=270)

label_user = Label(window,
                   text='------------------------------------------- User -------------------------------------------')
label_user.place(x=55, y=295)

# ------------------------------------------- User -------------------------------------------

User_Realname = Label(window, text='Real Name:')
User_Realname.place(x=90, y=315)
realname_input = Entry(window, relief='ridge', width=50)
realname_input.place(x=170, y=315)

User_Nickname = Label(window, text='Nickname:')
User_Nickname.place(x=90, y=345)
nickname_input = Entry(window, relief='ridge', width=50)
nickname_input.place(x=170, y=345)

User_Gender = Label(window, text='Gender:')
User_Gender.place(x=90, y=375)
gender_input = Entry(window, relief='ridge', width=50)
gender_input.place(x=170, y=375)

User_Location = Label(window, text='Location:')
User_Location.place(x=90, y=405)
user_location_input = Entry(window, relief='ridge', width=50)
user_location_input.place(x=170, y=405)

User_Email = Label(window, text='Email:')
User_Email.place(x=90, y=435)
email_input = Entry(window, relief='ridge', width=50)
email_input.place(x=170, y=435)

User_UserTags = Label(window, text='Tags:')
User_UserTags.place(x=90, y=465)
user_tags_input = Entry(window, relief='ridge', width=50)
user_tags_input.place(x=170, y=465)

User_Description = Label(window, text='Description:')
User_Description.place(x=90, y=495)
user_description_input = Entry(window, relief='ridge', width=50)
user_description_input.place(x=170, y=495)

register_button = Button(window, text="Register", command=register)
register_button.place(x=90, y=525)

updateProfile_button = Button(window, text="Update Profile", command=update_profile)
updateProfile_button.place(x=155, y=525)

user_email_input = Entry(window, relief='ridge', width=30)
user_email_input.place(x=200, y=555)

search_button = Button(window, text="Login with Email", command=login)
search_button.place(x=90, y=557.5)

logout_button = Button(window, text="Logout", command=log_out)
logout_button.place(x=490, y=557.5)

# ------------------------------------------- Email -------------------------------------------

invite_friend_button = Button(window, text="Invite Friend", command=invite_friend)
invite_friend_button.place(x=90, y=587.5)

Email_User_Nickname = Label(window, text='User Nickname:')
Email_User_Nickname.place(x=180, y=587.5)
email_nickname_input = Entry(window, relief='ridge', width=10)
email_nickname_input.place(x=290, y=585)

group_email_button = Button(window, text="Group Email", command=group_email)
group_email_button.place(x=90, y=615)

email_message_input = Entry(window, relief='ridge', width=50)
email_message_input.place(x=170, y=610)

# ------------------------------------------- Output -------------------------------------------

output = Label(window, text='Output')
output.place(x=800, y=20)
text = StringVar(output)
output_value = Label(window, textvariable=text)
text.set(value="This is the first iteration demo for JoinMe. \n")
output_value.pack()
output_value.place(x=700, y=40)
window.mainloop()
