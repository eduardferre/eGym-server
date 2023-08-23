def routine_schema(routine) -> dict:
    return { 
            "id": str(routine["_id"]),
            "creator": routine["creator"],
            "name": routine["name"],
            "description": routine["description"],
            "exercises": routine["exercises"],
            "liftedWeight": routine["liftedWeight"],
            "date": routine["date"]
            }

def routines_schema(routines) -> list:
    return [routine_schema(routine) for routine in routines]