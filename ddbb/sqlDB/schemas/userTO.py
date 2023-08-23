from userTO import UserTO

def userTO_schema(userTO) -> dict(UserTO): #NOSONAR
    return { 
            "id": str(userTO["_id"]),
            "username": userTO["username"],
            "firstname": userTO["firstname"],
            "surname": userTO["surname"],
            "email": userTO["email"],
            "password": userTO["password"],
            "birthDate": userTO["birthDate"]
            }

def usersTO_schema(usersTO) -> list: #NOSONAR
    return [userTO_schema(userTO) for userTO in usersTO]