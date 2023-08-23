def exerciseTO_schema(exerciseTO) -> dict: #NOSONAR
    return { 
            "id": str(exerciseTO["_id"]),
            "name": exerciseTO["name"],
            "description": exerciseTO["description"]
            }

def exercisesTO_schema(exercisesTO) -> list: #NOSONAR
    return [exerciseTO_schema(exercisesTO) for exercisesTO in exercisesTO]