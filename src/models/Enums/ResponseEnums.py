from enum import Enum


class ResponseEnums(Enum):
    AUTHENTICATION_FAILED = "Failed to Authenticate this user please enter valid User name and Password"
    AUTHENTICATION_SUCCESS = "Successfully Authenticated"
    