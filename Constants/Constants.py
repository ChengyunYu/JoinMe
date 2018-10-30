from enum import Enum


class ConnectConstants:
    USER = "admin"
    PASSWORD = "joinme4156"
    HOST = "joinme.czodqmkcwniq.us-east-1.rds.amazonaws.com"
    DATABASE = "joinme_db"


class UserFields(Enum):
    uid = 1
    name = 2
    nickname = 3
    gender = 4
    email = 5
    location = 6
    tags = 7
    description = 8


class Tags(Enum):
    sports = 1
    social = 2
    outdoors = 3
    indoors = 4
    sightseeing = 5
    exhibitions = 6
    entertaining = 7
    charity = 8
    business = 9

class Errors(Enum):
    SUCCESS = 1
    FAILURE = 2
    DUPLICATE = 3
    MISSING = 4
