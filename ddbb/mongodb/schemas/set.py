def set_schema(set) -> dict:
    return { 
            "id": str(set["_id"]),
            "exerciseName": set["exerciseName"],
            "weight": set["weight"],
            "reps": set["reps"],
            "rpe": set["rpe"],
            "rir": set["rir"],
            "restTime": set["restTime"]
            }

def sets_schema(sets) -> list:
    return [set_schema(set) for set in sets]