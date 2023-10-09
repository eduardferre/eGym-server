def set_schema(set) -> dict:
    if "id" in set:
        set["_id"] = set["id"]
        del set["id"]

    return {
        "id": str(set["_id"]),
        "weight": set["weight"],
        "reps": set["reps"],
        "rpe": set["rpe"],
        "rir": set["rir"],
        "restTime": set["restTime"],
    }


def sets_schema(sets) -> list:
    return [set_schema(set) for set in sets]
