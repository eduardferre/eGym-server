def userTO_schema(userTO) -> dict: #NOSONAR
    return { 
            "id": str(userTO["_id"]),
            "username": userTO["username"],
            "firstname": userTO["firstname"],
            "lastname": userTO["lastname"],
            "email": userTO["email"],
            "password": userTO["password"],
            "birthDate": userTO["birthDate"]
            }

def usersTO_schema(usersTO) -> list: #NOSONAR
    return [userTO_schema(userTO) for userTO in usersTO]