from db.mongodb.schemas.set import sets_schema


def exercise_schema(exercise) -> dict:
    if "id" in exercise:
        exercise["_id"] = exercise["id"]
        del exercise["id"]

    return {
        "id": str(exercise["_id"]),
        "name": exercise["name"],
        "description": exercise["description"],
        "sets": sets_schema(exercise["sets"]),
        "liftedWeight": exercise["liftedWeight"],
        "highestWeight": exercise["highestWeight"],
    }


def exercises_schema(exercises) -> list:
    return [exercise_schema(exercise) for exercise in exercises]
