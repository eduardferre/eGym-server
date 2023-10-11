import uuid


def is_valid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


print(uuid.uuid4())
print(is_valid(uuid.uuid4()))
