from db.mongodb.schemas.exercise import exercises_schema


def routine_schema(routine) -> dict:
    if "id" in routine:
        routine["_id"] = routine["id"]
        del routine["id"]

    return {
        "id": str(routine["_id"]),
        "creator": routine["creator"],
        "name": routine["name"],
        "description": routine["description"],
        "exercises": exercises_schema(routine["exercises"]),
        "liftedWeight": routine["liftedWeight"],
        "date": routine["date"],
    }


def routines_schema(routines) -> list:
    return [routine_schema(routine) for routine in routines]
