from enum import Enum


class Error(Enum):
    EXIT = 1
    OK = 0
    INVALID_COMMAND = -1
    TIMEOUT = -2
    IP = -3
    STATUS_REQUEST = -4
    TRANSACTION = -5
    READ = -6
    WRITE = -7
    READ_ONLY = -8
    INVALID_REGISTER = -9
    INVALID_VALUE = -10
    EMPTY_LINE = -11