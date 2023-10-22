import sys
import os

# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest
from datetime import datetime, date

from bson import ObjectId
from utils.logger import logging
from fastapi import APIRouter, HTTPException, status
from uuid import uuid4

from db.sqlDB.models.routineTO import RoutineTO
from db.sqlDB.models.exerciseTO import ExerciseTO
from src.main.routers import routinesTO
from src.main.routers import exercisesTO

id_test_404 = str(uuid4())
routineTO_add = RoutineTO(
    **{
        "id": "string",
        "creator": "eduardferre",
        "name": "LegDay",
        "description": "string",
        "exercises": [],
    }
)
exerciseTO_add = ExerciseTO(
    **{
        "id": "string",
        "creator": "eduardferre",
        "name": "Dead Lift",
        "description": "string",
    }
)


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutinesTO_NoContent():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutinesTO()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutineTOById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutineTOById("id_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutineTOById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutineTOById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutinesTOByCreator_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutinesTOByCreator("not_found_user")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutinesTOByCreator_NoContent():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutinesTOByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutinesTOByName_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutinesTOByName("not_found")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addRoutineTO_NotFoundUserTO():
    routine_not_found_user = routineTO_add.model_copy()
    routine_not_found_user.creator = "test21"

    with pytest.raises(HTTPException) as exception:
        await routinesTO.addRoutineTO(routine_not_found_user)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addRoutineTO_Created():
    routine_response = await routinesTO.addRoutineTO(routineTO_add)
    routineTO_add.id = routine_response.id
    assert isinstance(routine_response, RoutineTO)
    assert routine_response.creator == "eduardferre"


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutineTO_Ok():
    routines_list = await routinesTO.getRoutinesTO()
    assert isinstance(routines_list, list)
    assert len(routines_list) > 0


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutineTOById_Ok():
    routine_response = await routinesTO.getRoutineTOById(routineTO_add.id)
    assert isinstance(routine_response, RoutineTO)
    assert routine_response.id == routineTO_add.id


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutinesTOByCreator_Ok():
    routines_list = await routinesTO.getRoutinesTOByCreator("eduardferre")
    assert isinstance(routines_list, list)
    assert len(routines_list) > 0


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getRoutinesTOByName_Ok():
    routines_list = await routinesTO.getRoutinesTOByName("LegDay")
    assert isinstance(routines_list, list)
    assert len(routines_list) > 0


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTOToRoutineTO_BadRequestRoutineId():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.addExerciseTOToRoutineTO("id_not_valid", "id_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTOToRoutineTO_BadRequestExerciseId():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.addExerciseTOToRoutineTO(id_test_404, "id_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTOToRoutineTO_NotFoundRoutineId():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.addExerciseTOToRoutineTO(id_test_404, id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTOToRoutineTO_NotFoundExerciseId():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.addExerciseTOToRoutineTO(routineTO_add.id, id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTOToRoutineTO_Ok():
    exercise_response = await exercisesTO.addExerciseTO(exerciseTO_add)
    assert isinstance(exercise_response, ExerciseTO)
    exerciseTO_add.id = exercise_response.id
    logging.critical(await routinesTO.getRoutineTOById(routineTO_add.id))
    routine_response = await routinesTO.addExerciseTOToRoutineTO(
        routineTO_add.id, exerciseTO_add.id
    )
    assert isinstance(routine_response, RoutineTO)
    assert len(routine_response.exercises) > 0


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTOToRoutineTO_Conflict():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.addExerciseTOToRoutineTO(routineTO_add.id, exerciseTO_add.id)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateRoutineTO_BadRequest():
    routine_not_valid_id = routineTO_add.model_copy()
    routine_not_valid_id.id = "not_valid_id"
    with pytest.raises(HTTPException) as exception:
        await routinesTO.updateRoutineTO(routine_not_valid_id)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateRoutineTO_NotFound():
    routine_not_found = routineTO_add.model_copy()
    routine_not_found.id = id_test_404
    with pytest.raises(HTTPException) as exception:
        await routinesTO.updateRoutineTO(routine_not_found)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateRoutineTO_Ok():
    routine_update = routineTO_add.model_copy()
    routine_update.description = "eduardfer"
    routine_response = await routinesTO.updateRoutineTO(routine_update)
    assert isinstance(routine_response, RoutineTO)
    assert routine_response.id == routine_update.id
    assert routine_response.description == routine_update.description


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_deleteRoutineTO_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.deleteRoutineTO("not_valid_id")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_deleteRoutineTO_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routinesTO.deleteRoutineTO(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_deleteRoutineTO_Ok():
    routine_to_delete = await routinesTO.getRoutinesTOByCreator("eduardferre")
    routine_response = await routinesTO.deleteRoutineTO(routine_to_delete[0].id)
    assert isinstance(routine_response, RoutineTO)
    with pytest.raises(HTTPException) as exception:
        await routinesTO.getRoutinesTOByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204
