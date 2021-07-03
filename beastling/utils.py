""" Utility functions """

from uuid import uuid4


def get_uuid() -> str:
    """ Get a unique identifier as string (because otherwise ugly to write) """
    return str(uuid4())