from routineTO import RoutineTO

def routineTO_schema(routineTO) -> dict(RoutineTO): #NOSONAR
    return { 
            "id": str(routineTO["_id"]),
            "creator": routineTO["creator"],
            "name": routineTO["name"],
            "description": routineTO["description"],
            "exercises": routineTO["exercises"]
            }

def routinesTO_schema(exercisesTO) -> list: #NOSONAR
    return [routineTO_schema(exercisesTO) for exercisesTO in exercisesTO]