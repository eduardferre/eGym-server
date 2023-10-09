import sys
import os

# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest

from bson import ObjectId
from utils.logger import logging
from fastapi import APIRouter, HTTPException, status

from db.mongodb.models.routine import Routine
from db.mongodb.models.exercise import Exercise
from db.mongodb.models.set import Set
from src.main.routers import routines, users

id_test_404 = "507f1f77bcf86cd799439011"
routine_add = Routine(
    **{
        "id": "507f1f77bcf86cd799439211",
        "creator": "eduardferre",
        "name": "Leg Day",
        "description": "leg day",
        "exercises": [
            Exercise(
                **{
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "sets": [
                        Set(
                            **{
                                "id": "string",
                                "weight": 0,
                                "reps": 0,
                                "rpe": 0,
                                "rir": 0,
                                "restTime": 0,
                            }
                        )
                    ],
                    "liftedWeight": 0,
                    "highestWeight": 0,
                }
            )
        ],
        "liftedWeight": 200.5,
        "date": "2023-08-23 15:30:45.123456",
    }
)
routine_to_delete = routine_add.copy()


@pytest.mark.asyncio
async def test_getRoutines_NoContent():
    with pytest.raises(HTTPException) as exception:
        await routines.getRoutines()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_getRoutineById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await routines.getRoutineById("id_is_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_getRoutineById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routines.getRoutineById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_getRoutineByCreator_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routines.getRoutinesByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getRoutineByCreator_NoContent():
    with pytest.raises(HTTPException) as exception:
        await routines.getRoutinesByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_addRoutine_NotFound():
    routine_add.creator = "not_found"
    with pytest.raises(HTTPException) as exception:
        await routines.addRoutine(routine_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_addRoutine_Created():
    routine_add.creator = "eduardferre"
    routine_response = await routines.addRoutine(routine_add)
    global id_test_Ok
    id_test_Ok = routine_response.id
    assert isinstance(routine_response, Routine)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getRoutines_Ok():
    routines_list = await routines.getRoutines()
    assert isinstance(routines_list, list)
    assert len(routines_list) > 0


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getRoutineById_Ok():
    routine_response = await routines.getRoutineById(id_test_Ok)
    assert isinstance(routine_response, Routine)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getRoutinesByCreator_Ok():
    routines_list = await routines.getRoutinesByCreator("eduardferre")
    for routine in routines_list:
        routines_list[routines_list.index(routine)] = Routine(**routine)
    assert isinstance(routines_list, list)
    assert len(routines_list) > 0
    user_update = await users.getUserByUsername("eduardferre")
    assert user_update.routinesLog == routines_list


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updateRoutine_BadRequest():
    routine_add.id = "id_is_not_valid"
    with pytest.raises(HTTPException) as exception:
        await routines.updateRoutine(routine_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updateRoutine_NotFound():
    routine_add.id = id_test_404
    with pytest.raises(HTTPException) as exception:
        await routines.updateRoutine(routine_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updateRoutine_NoContent():
    routine_add.creator = "eduardferre"
    routine_add.id = id_test_Ok
    with pytest.raises(HTTPException) as exception:
        await routines.updateRoutine(routine_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updateRoutine_UserNotFound():
    routine_add.id = id_test_Ok
    routine_add.creator = "not_found"
    with pytest.raises(HTTPException) as exception:
        await routines.updateRoutine(routine_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updateRoutine_Created():
    routine_add.creator = "eduardferre"
    routine_add.id = id_test_Ok
    routine_add.description = "new_description"
    routine_response = await routines.updateRoutine(routine_add)
    assert isinstance(routine_response, Routine)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteRoutine_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await routines.deleteRoutine("id_is_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteRoutine_NotFound():
    with pytest.raises(HTTPException) as exception:
        await routines.deleteRoutine(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteRoutine_Ok():
    routine_response = await routines.deleteRoutine(id_test_Ok)
    assert isinstance(routine_response, Routine)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteAllCreatorRoutines_NotFound():
    routine_response = await routines.addRoutine(routine_to_delete)
    assert isinstance(routine_response, Routine)

    with pytest.raises(HTTPException) as exception:
        await routines.deleteAllCreatorRoutines("not_found")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteAllCreatorRoutines_Ok():
    routines_list = await routines.deleteAllCreatorRoutines("eduardferre")
    assert isinstance(routines_list, list)
    assert len(routines_list) > 0

    routines_list = await routines.deleteAllCreatorRoutines("eduardferre")
    assert isinstance(routines_list, list)
    assert len(routines_list) == 0
