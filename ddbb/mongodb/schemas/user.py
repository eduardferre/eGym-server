from user import User

def user_schema(user) -> dict(User):
    return { 
            "id": str(user["_id"]),
            "username": user["username"],
            "fullname": user["fullname"],
            "email": user["email"],
            "age": user["age"],
            "height": user["height"],
            "weight": user["weight"],
            "physicalActivity": user["physicalActivity"],
            "role": user["role"],
            "followers": user["followers"],
            "postsLog": user["postsLog"],
            "routinesLog": user["routinesLog"],
            "profilePicture": user["profilePicture"],
            "backgroundPicture": user["backgroundPicture"]
            }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]