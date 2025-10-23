from enum import Enum


class ResponseEnums(Enum):
    AUTHENTICATION_FAILED = "Failed to Authenticate this user please enter valid User name and Password"
    AUTHENTICATION_SUCCESS = "Successfully Authenticated"
    ADDED_TO_DATA_BASE = "Chunks Successfully added to DataBase"
    FAILED_TO_ADD_TO_DATA_BASE = "Error while adding chunks to DataBase"
    