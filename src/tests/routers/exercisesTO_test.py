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

from db.sqlDB.models.exerciseTO import ExerciseTO
from src.main.routers import exercisesTO
from src.main.routers import exercisesTO

id_test_404 = str(uuid4())
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
async def test_getExercisesTO_NoContent():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExercisesTO()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExerciseTOById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExerciseTOById("id_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExerciseTOById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExerciseTOById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExercisesTOByCreator_NotFound():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExercisesTOByCreator("not_found_user")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExercisesTOByCreator_NoContent():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExercisesTOByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExerciseTOByName_NotFound():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExerciseTOByName("not_found")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTO_NotFoundUserTO():
    exercise_not_found_user = exerciseTO_add.model_copy()
    exercise_not_found_user.creator = "test21"

    with pytest.raises(HTTPException) as exception:
        await exercisesTO.addExerciseTO(exercise_not_found_user)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTO_Created():
    exercise_response = await exercisesTO.addExerciseTO(exerciseTO_add)
    exerciseTO_add.id = exercise_response.id
    assert isinstance(exercise_response, ExerciseTO)
    assert exercise_response.creator == "eduardferre"


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_addExerciseTO_Conflict():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.addExerciseTO(exerciseTO_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExerciseTO_Ok():
    exercises_list = await exercisesTO.getExercisesTO()
    assert isinstance(exercises_list, list)
    assert len(exercises_list) > 0


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExerciseTOById_Ok():
    exercise_response = await exercisesTO.getExerciseTOById(exerciseTO_add.id)
    assert isinstance(exercise_response, ExerciseTO)
    assert exercise_response.id == exerciseTO_add.id


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExercisesTOByCreator_Ok():
    exercises_list = await exercisesTO.getExercisesTOByCreator("eduardferre")
    assert isinstance(exercises_list, list)
    assert len(exercises_list) > 0


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_getExerciseTOByName_Ok():
    exercise_response = await exercisesTO.getExerciseTOByName("Dead Lift")
    assert isinstance(exercise_response, ExerciseTO)
    assert exercise_response.name == "Dead Lift"


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateExerciseTO_BadRequest():
    exercise_not_valid_id = exerciseTO_add.model_copy()
    exercise_not_valid_id.id = "not_valid_id"
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.updateExerciseTO(exercise_not_valid_id)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateExerciseTO_NotFound():
    exercise_not_found = exerciseTO_add.model_copy()
    exercise_not_found.id = id_test_404
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.updateExerciseTO(exercise_not_found)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateExerciseTO_Conflict():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.updateExerciseTO(exerciseTO_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_updateExerciseTO_Ok():
    exercise_update = exerciseTO_add.model_copy()
    exercise_update.name = "Squat"
    exercise_response = await exercisesTO.updateExerciseTO(exercise_update)
    assert isinstance(exercise_response, ExerciseTO)
    assert exercise_response.id == exercise_update.id
    assert exercise_response.description == exercise_update.description


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_deleteExerciseTO_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.deleteExerciseTO("not_valid_id")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_deleteExerciseTO_NotFound():
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.deleteExerciseTO(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="usersTO_test.py::test_addUserTO_Created")
@pytest.mark.asyncio
async def test_deleteExerciseTO_Ok():
    exercise_to_delete = await exercisesTO.getExercisesTOByCreator("eduardferre")
    exercise_response = await exercisesTO.deleteExerciseTO(exercise_to_delete[0].id)
    assert isinstance(exercise_response, ExerciseTO)
    with pytest.raises(HTTPException) as exception:
        await exercisesTO.getExercisesTOByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204
