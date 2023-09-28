# **eGym-server - BACKEND**
Welcome to my thesis degree project, this repository contains all the specifications related to the backend of the application.

In this README you can find some important information about the creation of the backend itself. Information such which databases have been used, which API structure has been chosen and the deployment of the API.

## **API ENDPOINTS**
The API is formed by the following endpoints with their respective methods.

### ***UsersTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | usersTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all users |
| GET       | usersTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get user by id |
| POST    | usersTO/ | -                     | 201_CREATED / 409_CONFLICT | Add user |
| PUT       | usersTO/ | -                    | 201_CREATED / 404_NOT_FOUND / 409_CONFLICT | Update user info |
| DELETE | usersTO/ | {username}  | 200_OK / 404_NOT_FOUND | Delete a user by username |


### ***ExercisesTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | exercisesTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all exercises |
| GET       | exercisesTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get exercise by id |
| GET       | exercisesTO/creator/ | {creator}                | 200_OK / 404_NOT_FOUND | Get exercises by creator |
| GET       | exercisesTO/exerciseName/ | {name}                | 200_OK / 404_NOT_FOUND | Get exercises by name |
| POST    | exercisesTO/ | -                     | 201_CREATED / 409_CONFLICT | Add exercise |
| PUT       | exercisesTO/ | -                    | 201_CREATED / 404_NOT_FOUND | Update exercise info |
| DELETE | exercisesTO/ | {name}  | 200_OK / 404_NOT_FOUND | Delete an exercise by name |


### ***RoutinesTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | routinesTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all routines |
| GET       | routinesTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get routine by id |
| GET       | routinesTO/creator/ | {creator}                | 200_OK / 404_NOT_FOUND | Get routines by creator |
| GET       | routinesTO/routineName/ | {name}                | 200_OK / 404_NOT_FOUND | Get routines by name |
| POST    | routinesTO/ | -                     | 201_CREATED | Add routine |
| POST    | routinesTO/ | {routineId}_{exerciseId}                     | 201_CREATED / 409_CONFLICT | Add exercise to routine |
| PUT       | routinesTO/ | -                    | 201_CREATED / 404_NOT_FOUND | Update routine info |
| DELETE | routinesTO/ | {id}  | 200_OK / 404_NOT_FOUND | Delete a routine by id |


### ***Users** - MONGODB DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | users/ | -                    | 200_OK / 204_NO_CONTENT | Get all users |
| GET       | users/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get user by id |
| GET       | users/username/ | {username}                | 200_OK / 404_NOT_FOUND | Get user by username |
| POST    | users/ | -                     | 201_CREATED / 409_CONFLICT | Add user |
| PUT       | users/ | -                    | 201_CREATED / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / HTTP_500_INTERNAL_SERVER_ERROR | Update user info |
| DELETE | users/ | {id}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Delete a user by id |
| DELETE | users/ | -     | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Delete all users |


### ***Posts** - MONGODB DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | posts/ | -                    | 200_OK / 204_NO_CONTENT | Get all posts |
| GET       | posts/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get post by id |
| GET       | posts/creator/ | {creator}    | 200_OK / 204_NO_CONTENT / 404_NOT_FOUND | Get posts by creator |
| POST    | posts/ | -                      | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / 500_INTERNAL_SERVER_ERROR | Add post |
| PUT       | posts/ | -                    | 201_CREATED / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / HTTP_500_INTERNAL_SERVER_ERROR | Update user info |
| DELETE | posts/ | {id}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Delete a post by id |
| DELETE | posts/creatorPosts/ | {creator}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Delete creator's posts |


### ***Comments** - MONGODB DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | comments/ | -                    | 200_OK / 204_NO_CONTENT | Get all comments |
| GET       | comments/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get post by id |
| GET       | comments/creator/ | {creator}    | 200_OK / 204_NO_CONTENT / 404_NOT_FOUND | Get comments by creator |
| GET       | comments/post/ | {postId}    | 200_OK / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND | Get comments by post |
| POST    | comments/post/ | {postId}      | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Add comment to post |
| PUT       | comments/post/ | {postId}    | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Update comment |
| DELETE | comments/post/ | {postId}/comment/{commentId}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Delete a comment from post by id |
| DELETE | comments/postComments/ | {postId}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / HTTP_500_INTERNAL_SERVER_ERROR | Delete post's comments |


### ***Routines** - MONGODB DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | routines/ | -                    | 200_OK / 204_NO_CONTENT | Get all routines |
| GET       | routines/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get post by id |
| GET       | routines/creator/ | {creator}    | 200_OK / 204_NO_CONTENT / 404_NOT_FOUND | Get routines by creator |
| POST    | routines/ | -                    | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / HTTP_500_INTERNAL_SERVER_ERROR | Add routine |
| PUT       | routines/ | -                  | 201_CREATED / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / HTTP_500_INTERNAL_SERVER_ERROR | Update routine |
| DELETE | routines/ | {id}                  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / HTTP_500_INTERNAL_SERVER_ERROR | Delete routine by id |
| DELETE | routines/creatorRoutines/ | {creator}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / HTTP_500_INTERNAL_SERVER_ERROR | Delete user's routines |

## **API UNIT TESTS**
The endpoints should be verified, this verification is done by using unit tests, developed with the `pytest` library and its pluggings. Using unit tests aims to check that all the cases are supported by the server, meaning that in front of any error or exception, the server is protected and the user experience won't be affected. The `pytest-cov` library has been used to ensure the coverage of the unit tests. It provides a wide report where the overall coverage can be checked. Furthermore, this add-on shows visually which classes are not covered pointing to the lines that should be revised by testing.

### **LAST PR COVERAGE REPORT *(src/tests/reports/index.html)* - `Coverage report: 64%`**

<details>
<summary>Check the last coverage report</summary>
<br>

The following table is generated from *index.html* in this <kbd>[website](http://johnbeech.github.io/html-table-to-markdown-converter/index.html)</kbd>.

| Module | statements | missing | excluded | coverage |
| --- | --- | --- | --- | --- |
| db/mongodb/models/comment.py | 8 | 0 | 0 | 100% |
| db/mongodb/models/exercise.py | 12 | 0 | 0 | 100% |
| db/mongodb/models/post.py | 12 | 0 | 0 | 100% |
| db/mongodb/models/routine.py | 14 | 0 | 0 | 100% |
| db/mongodb/models/set.py | 9 | 0 | 0 | 100% |
| db/mongodb/models/user.py | 24 | 0 | 0 | 100% |
| db/mongodb/schemas/post.py | 4 | 0 | 0 | 100% |
| db/mongodb/schemas/user.py | 4 | 0 | 0 | 100% |
| db/sqlDB/models/exerciseTO.py | 7 | 0 | 0 | 100% |
| db/sqlDB/models/routineTO.py | 9 | 0 | 0 | 100% |
| db/sqlDB/models/userTO.py | 9 | 0 | 0 | 100% |
| src/tests/__init__.py | 0 | 0 | 0 | 100% |
| src/tests/main_test.py | 13 | 0 | 0 | 100% |
| src/tests/routers/__init__.py | 0 | 0 | 0 | 100% |
| src/tests/routers/comments_test.py | 22 | 0 | 0 | 100% |
| src/tests/routers/posts_test.py | 156 | 0 | 0 | 100% |
| src/tests/routers/users_test.py | 125 | 0 | 0 | 100% |
| utils/logger.py | 20 | 0 | 0 | 100% |
| src/main/main.py | 22 | 1 | 0 | 95% |
| src/main/routers/posts.py | 172 | 19 | 0 | 89% |
| db/mongodb/client.py | 14 | 2 | 0 | 86% |
| db/sqlDB/client.py | 7 | 1 | 0 | 86% |
| src/main/routers/users.py | 148 | 22 | 0 | 85% |
| conftest.py | 23 | 5 | 0 | 78% |
| db/mongodb/schemas/comment.py | 4 | 1 | 0 | 75% |
| db/mongodb/schemas/routine.py | 4 | 2 | 0 | 50% |
| db/sqlDB/schemas/exerciseTO.py | 4 | 2 | 0 | 50% |
| db/sqlDB/schemas/routineTO.py | 4 | 2 | 0 | 50% |
| db/sqlDB/schemas/userTO.py | 4 | 2 | 0 | 50% |
| src/main/routers/comments.py | 185 | 127 | 0 | 31% |
| src/main/routers/usersTO.py | 72 | 52 | 0 | 28% |
| src/main/routers/exercisesTO.py | 86 | 64 | 0 | 26% |
| src/main/routers/routines.py | 174 | 135 | 0 | 22% |
| src/main/routers/routinesTO.py | 122 | 95 | 0 | 22% |
| Total | 1493 | 532 | 0 | 64% |
        
</details>

<details>
<summary>Check the last coverage logs</summary>
<br>

```
src/tests/routers/comments_test.py::test_getComments_NoContent PASSED ✅  [  2%]
src/tests/routers/comments_test.py::test_getCommentById_BadRequest PASSED ✅  [  5%]
src/tests/routers/posts_test.py::test_getPosts_NoContent PASSED ✅       [  7%]
src/tests/routers/posts_test.py::test_getPostById_BadRequest PASSED ✅   [ 10%]
src/tests/routers/posts_test.py::test_getPostById_NotFound PASSED ✅     [ 12%]
src/tests/routers/posts_test.py::test_getPostByCreator_NotFound PASSED ✅  [ 15%]
src/tests/routers/users_test.py::test_addUser_Created PASSED ✅          [ 17%]
src/tests/routers/posts_test.py::test_getPostByCreator_NoContent PASSED ✅  [ 20%]
src/tests/routers/posts_test.py::test_addPost_NotFound PASSED ✅         [ 22%]
src/tests/routers/posts_test.py::test_addPost_Created PASSED ✅          [ 25%]
src/tests/routers/posts_test.py::test_getPosts_Ok PASSED ✅              [ 27%]
src/tests/routers/posts_test.py::test_getPostById_Ok PASSED ✅           [ 30%]
src/tests/routers/posts_test.py::test_getPostByCreator_Ok PASSED ✅      [ 32%]
src/tests/routers/posts_test.py::test_updatePost_BadRequest PASSED ✅    [ 35%]
src/tests/routers/posts_test.py::test_updatePost_NotFound PASSED ✅      [ 37%]
src/tests/routers/posts_test.py::test_updatePost_NoContent PASSED ✅     [ 40%]
src/tests/routers/posts_test.py::test_updatePost_User_NotFound PASSED ✅  [ 42%]
src/tests/routers/posts_test.py::test_updatePost_Created PASSED ✅       [ 45%]
src/tests/routers/posts_test.py::test_deletePost_BadRequest PASSED ✅    [ 47%]
src/tests/routers/posts_test.py::test_deletePost_NotFound PASSED ✅      [ 50%]
src/tests/routers/posts_test.py::test_deletePost_Ok PASSED ✅            [ 52%]
src/tests/routers/posts_test.py::test_deleteAllCreatorPosts_NotFound PASSED ✅  [ 55%]
src/tests/routers/posts_test.py::test_deleteAllCreatorPosts_Ok PASSED ✅  [ 57%]
src/tests/routers/users_test.py::test_getUsers_Ok PASSED ✅              [ 60%]
src/tests/routers/users_test.py::test_addUser_Conflict PASSED ✅         [ 62%]
src/tests/routers/users_test.py::test_getUserById_Ok PASSED ✅           [ 65%]
src/tests/routers/users_test.py::test_getUserById_BadRequest PASSED ✅   [ 67%]
src/tests/routers/users_test.py::test_getUserById_NotFound PASSED ✅     [ 70%]
src/tests/routers/users_test.py::test_getUserByUsername_Ok PASSED ✅     [ 72%]
src/tests/routers/users_test.py::test_updateUser_NoContent PASSED ✅     [ 75%]
src/tests/routers/users_test.py::test_updateUser_Ok PASSED ✅            [ 77%]
src/tests/routers/users_test.py::test_getUserByUsername_NotFound PASSED ✅  [ 80%]
src/tests/routers/users_test.py::test_updateUser_BadRequest PASSED ✅    [ 82%]
src/tests/routers/users_test.py::test_updateUser_NotFound PASSED ✅      [ 85%]
src/tests/routers/users_test.py::test_updateUser_Conflict PASSED ✅      [ 87%]
src/tests/routers/users_test.py::test_deleteUser_Ok PASSED ✅            [ 90%]
src/tests/routers/users_test.py::test_deleteUser_BadRequest PASSED ✅    [ 92%]
src/tests/routers/users_test.py::test_deleteUser_NotFound PASSED ✅      [ 95%]
src/tests/routers/users_test.py::test_deleteAllUsers_Ok PASSED ✅        [ 97%]
src/tests/routers/users_test.py::test_getUsers_NoContent PASSED ✅       [100%]
```

</details>

### UNIT TESTS IMPLEMENTED
<details>
<summary>The following tests have been stated `//TODO: Reorder for proper testing`</summary>
<be>

| Test name                         | Description                                      | ✅ / ❌ |
| --------------------------------- | ------------------------------------------------ | :-----: |
| `test_getComments_NoContent`      | Test getting comments (204 - No Content).        |    ✅   |
| `test_getCommentById_BadRequest`  | Test getting a comment by ID (400 - Bad Request).|    ✅   |
| `test_getPosts_NoContent`         | Test getting posts (204 - No Content).           |    ✅   |
| `test_getPostById_BadRequest`     | Test getting a post by ID (400 - Bad Request).   |    ✅   |
| `test_getPostById_NotFound`       | Test getting a post by ID (404 - Not Found).     |    ✅   |
| `test_getPostByCreator_NotFound`  | Test getting a post by creator (404 - Not Found)|    ✅   |
| `test_addUser_Created`            | Test adding a user (201 - Created).              |    ✅   |
| `test_getPostByCreator_NoContent` | Test getting posts by creator (204 - No Content)|    ✅   |
| `test_addPost_NotFound`           | Test adding a post (404 - Not Found).           |    ✅   |
| `test_addPost_Created`            | Test adding a post (201 - Created).              |    ✅   |
| `test_getPosts_Ok`                | Test getting posts (200 - OK).                   |    ✅   |
| `test_getPostById_Ok`             | Test getting a post by ID (200 - OK).            |    ✅   |
| `test_getPostByCreator_Ok`        | Test getting posts by creator (200 - OK).       |    ✅   |
| `test_updatePost_BadRequest`      | Test updating a post (400 - Bad Request).        |    ✅   |
| `test_updatePost_NotFound`        | Test updating a post (404 - Not Found).          |    ✅   |
| `test_updatePost_NoContent`       | Test updating a post (204 - No Content).         |    ✅   |
| `test_updatePost_User_NotFound`   | Test updating a post (404 - User Not Found).     |    ✅   |
| `test_updatePost_Created`         | Test updating a post (201 - Created).            |    ✅   |
| `test_deletePost_BadRequest`      | Test deleting a post (400 - Bad Request).        |    ✅   |
| `test_deletePost_NotFound`        | Test deleting a post (404 - Not Found).          |    ✅   |
| `test_deletePost_Ok`              | Test deleting a post (200 - OK).                 |    ✅   |
| `test_deleteAllCreatorPosts_NotFound` | Test deleting all posts by creator (404 - Not Found)| ✅ |
| `test_deleteAllCreatorPosts_Ok`   | Test deleting all posts by creator (200 - OK).    | ✅ |
| `test_getUsers_Ok`                | Test getting users (200 - OK).                   |    ✅   |
| `test_addUser_Conflict`           | Test adding a user (409 - Conflict).             |    ✅   |
| `test_getUserById_Ok`             | Test getting a user by ID (200 - OK).            |    ✅   |
| `test_getUserById_BadRequest`     | Test getting a user by ID (400 - Bad Request).   |    ✅   |
| `test_getUserById_NotFound`       | Test getting a user by ID (404 - Not Found).     |    ✅   |
| `test_getUserByUsername_Ok`       | Test getting a user by Username (200 - OK).      |    ✅   |
| `test_updateUser_NoContent`       | Test updating a user (204 - No Content).         |    ✅   |
| `test_updateUser_Ok`              | Test updating a user (200 - OK).                 |    ✅   |
| `test_getUserByUsername_NotFound` | Test getting a user by Username (404 - Not Found)|    ✅   |
| `test_updateUser_BadRequest`      | Test updating a user (400 - Bad Request).        |    ✅   |
| `test_updateUser_NotFound`        | Test updating a user (404 - Not Found).          |    ✅   |
| `test_updateUser_Conflict`        | Test updating a user (409 - Conflict).           |    ✅   |
| `test_deleteUser_Ok`              | Test deleting a user (200 - OK).                 |    ✅   |
| `test_deleteUser_BadRequest`      | Test deleting a user (400 - Bad Request).        |    ✅   |
| `test_deleteUser_NotFound`        | Test deleting a user (404 - Not Found).          |    ✅   |
| `test_deleteAllUsers_Ok`          | Test deleting all users (200 - OK).              |    ✅   |
| `test_`       | description   | ✅ / ❌ |

</details>
