from exercise import Exercise

def exercise_schema(exercise) -> dict(Exercise):
    return { 
            "id": str(exercise["_id"]),
            "name": exercise["name"],
            "description": exercise["description"],
            "sets": exercise["sets"],
            "liftedWeight": exercise["liftedWeight"],
            "highestWeight": exercise["highestWeight"]
            }

def exercises_schema(exercises) -> list:
    return [exercise_schema(exercise) for exercise in exercises]