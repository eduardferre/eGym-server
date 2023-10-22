from db.mongodb.schemas.routine import routines_schema


def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "fullname": user["fullname"],
        "email": user["email"],
        "phone": user["phone"],
        "age": user["age"],
        "height": user["height"],
        "weight": user["weight"],
        "physicalActivity": user["physicalActivity"],
        "role": user["role"],
        "followers": user["followers"],
        "following": user["following"],
        "postsLog": user["postsLog"],
        "routinesLog": routines_schema(user["routinesLog"]),
        "routines": user["routines"],
        "profilePicture": user["profilePicture"],
        "backgroundPicture": user["backgroundPicture"],
        "public": user["public"],
    }


def users_schema(users) -> list:
    return [user_schema(user) for user in users]
