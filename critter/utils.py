from uuid import uuid4


def get_uuid(short: bool = False) -> str:
    """ Wrap the ugly call to get a UUID string """
    uuid = str(uuid4())
    if short:
        return uuid[:8]
    else:
        return uuid