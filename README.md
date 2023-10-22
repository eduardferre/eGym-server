# **eGym-server - BACKEND**
Welcome to my thesis degree project, this repository contains all the specifications related to the application's backend.

In this README you can find some important information about the creation of the backend itself. Information includes which databases have been used, which API structure has been chosen and the API deployment.

## **API ENDPOINTS**
The API is formed by the following endpoints with their respective methods.

### ***UsersTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | usersTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all users |
| GET       | usersTO/ | {id}                 | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get user by id |
| GET       | usersTO/ | {username}           | 200_OK / 404_NOT_FOUND | Get user by username |
| POST    | usersTO/ | -                      | 201_CREATED / 409_CONFLICT / 500_INTERNAL_SERVER_ERROR | Add user |
| PUT       | usersTO/ | -                    | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / 500_INTERNAL_SEVER_ERROR | Update user info |
| DELETE | usersTO/ | {username}              | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Delete a user by username |


### ***ExercisesTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | exercisesTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all exercises |
| GET       | exercisesTO/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get exercise by id |
| GET       | exercisesTO/creator/ | {creator}                | 200_OK / 204_NO_CONTENT / 404_NOT_FOUND | Get exercises by creator |
| GET       | exercisesTO/exerciseName/ | {name}                | 200_OK / 404_NOT_FOUND | Get exercises by name |
| POST    | exercisesTO/ | -                     | 201_CREATED / 404_NOT_FOUND / 409_CONFLICT | Add exercise |
| PUT       | exercisesTO/ | -                    | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT | Update exercise info |
| DELETE | exercisesTO/ | {name}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Delete an exercise by name |


### ***RoutinesTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | routinesTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all routines |
| GET       | routinesTO/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get routine by id |
| GET       | routinesTO/creator/ | {creator}                | 200_OK / 404_NOT_FOUND / 204_NO_CONTENT | Get routines by creator |
| GET       | routinesTO/routineName/ | {name}                | 200_OK / 404_NOT_FOUND | Get routines by name |
| POST    | routinesTO/ | -                     | 201_CREATED / 404_NOT_FOUND | Add routine |
| POST    | routinesTO/ | {routineId}_{exerciseId}                     | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT | Add exercise to routine |
| PUT       | routinesTO/ | -                    | 201_CREATED / 400_BAD_REQUEST / 404_NOT_FOUND | Update routine info |
| DELETE | routinesTO/ | {id}  | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Delete a routine by id |


### ***Users** - MONGODB DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | users/{attribute}/{value} | -                    | 200_OK / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND | Get public users |
| GET       | users/ | -                    | 200_OK / 204_NO_CONTENT | Get all users |
| GET       | users/ | {id}                | 200_OK / 400_BAD_REQUEST / 404_NOT_FOUND | Get user by id |
| GET       | users/username/ | {username}                | 200_OK / 404_NOT_FOUND | Get user by username |
| POST    | users/ | -                     | 201_CREATED / 409_CONFLICT | Add user |
| PUT    | users/ | {follower}/{followed}                     | 201_CREATED / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / 500_INTERNAL_SERVER_ERROR | Follow user |
| PUT    | users/ | {follower}/{followed}                     | 201_CREATED / 204_NO_CONTENT / 400_BAD_REQUEST / 404_NOT_FOUND / 409_CONFLICT / 500_INTERNAL_SERVER_ERROR | Unfollow user |
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
| GET       | comments/creator/ | {creator}    | 200_OK / 404_NOT_FOUND | Get comments by creator |
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

### **LAST COVERAGE REPORT *(src/tests/reports/index.html)* - `Coverage report: 97%`**

<details>
<summary>Check the last coverage report</summary>
<br>

The following table is generated from *index.html* in this <kbd>[website](http://johnbeech.github.io/html-table-to-markdown-converter/index.html)</kbd>.

| Module | statements | missing | excluded | coverage |
| --- | --- | --- | --- | --- |
| conftest.py | 23 | 5 | 0 | 78% |
| db/mongodb/client.py | 14 | 2 | 0 | 86% |
| db/mongodb/models/comment.py | 8 | 0 | 0 | 100% |
| db/mongodb/models/exercise.py | 12 | 0 | 0 | 100% |
| db/mongodb/models/post.py | 18 | 1 | 0 | 94% |
| db/mongodb/models/routine.py | 18 | 0 | 0 | 100% |
| db/mongodb/models/set.py | 9 | 0 | 0 | 100% |
| db/mongodb/models/user.py | 26 | 0 | 0 | 100% |
| db/mongodb/schemas/comment.py | 4 | 0 | 0 | 100% |
| db/mongodb/schemas/exercise.py | 8 | 0 | 0 | 100% |
| db/mongodb/schemas/post.py | 4 | 0 | 0 | 100% |
| db/mongodb/schemas/routine.py | 8 | 0 | 0 | 100% |
| db/mongodb/schemas/set.py | 7 | 0 | 0 | 100% |
| db/mongodb/schemas/user.py | 5 | 0 | 0 | 100% |
| db/sqlDB/client.py | 7 | 1 | 0 | 86% |
| db/sqlDB/models/exerciseTO.py | 7 | 0 | 0 | 100% |
| db/sqlDB/models/routineTO.py | 9 | 0 | 0 | 100% |
| db/sqlDB/models/userTO.py | 10 | 0 | 0 | 100% |
| db/sqlDB/schemas/exerciseTO.py | 4 | 1 | 0 | 75% |
| db/sqlDB/schemas/routineTO.py | 4 | 1 | 0 | 75% |
| db/sqlDB/schemas/userTO.py | 4 | 1 | 0 | 75% |
| src/main/main.py | 22 | 1 | 0 | 95% |
| src/main/routers/comments.py | 200 | 29 | 0 | 86% |
| src/main/routers/exercisesTO.py | 146 | 0 | 0 | 100% |
| src/main/routers/posts.py | 174 | 18 | 0 | 90% |
| src/main/routers/routines.py | 184 | 10 | 0 | 95% |
| src/main/routers/routinesTO.py | 200 | 0 | 0 | 100% |
| src/main/routers/users.py | 219 | 19 | 0 | 91% |
| src/main/routers/usersTO.py | 134 | 6 | 0 | 96% |
| src/tests/__init__.py | 0 | 0 | 0 | 100% |
| src/tests/main_test.py | 13 | 0 | 0 | 100% |
| src/tests/routers/__init__.py | 0 | 0 | 0 | 100% |
| src/tests/routers/comments_test.py | 256 | 0 | 0 | 100% |
| src/tests/routers/exercisesTO_test.py | 163 | 0 | 0 | 100% |
| src/tests/routers/posts_test.py | 166 | 0 | 0 | 100% |
| src/tests/routers/routinesTO_test.py | 196 | 0 | 0 | 100% |
| src/tests/routers/routines_test.py | 162 | 0 | 0 | 100% |
| src/tests/routers/usersTO_test.py | 122 | 0 | 0 | 100% |
| src/tests/routers/users_test.py | 181 | 0 | 0 | 100% |
| utils/logger.py | 20 | 0 | 0 | 100% |
| **Total** | **2767** | **95** | **0** | **97%** |
        
</details>

<details>
<summary>Check the last coverage logs</summary>
<br>

```                                                       
1      src/tests/routers/posts_test.py::test_getPosts_NoContent PASSED ✅                                  [  0%]
2      src/tests/routers/posts_test.py::test_getPostById_BadRequest PASSED ✅                              [  1%]
3      src/tests/routers/posts_test.py::test_getPostById_NotFound PASSED ✅                                [  1%]
4      src/tests/routers/posts_test.py::test_getPostByCreator_NotFound PASSED ✅                           [  2%]
5      src/tests/routers/routines_test.py::test_getRoutines_NoContent PASSED ✅                            [  3%]
6      src/tests/routers/routines_test.py::test_getRoutineById_BadRequest PASSED ✅                        [  3%]
7      src/tests/routers/routines_test.py::test_getRoutineById_NotFound PASSED ✅                          [  4%]
8      src/tests/routers/routines_test.py::test_getRoutineByCreator_NotFound PASSED ✅                     [  5%]
9      src/tests/routers/usersTO_test.py::test_getUsersTO_NoContent PASSED ✅                              [  5%]
10      src/tests/routers/usersTO_test.py::test_getUserTOById_BadRequest PASSED ✅                          [  6%]
11      src/tests/routers/usersTO_test.py::test_getUserTOById_NotFound PASSED ✅                            [  7%]
12      src/tests/routers/usersTO_test.py::test_getUserTOByUsername_NotFound PASSED ✅                      [  7%]
13      src/tests/routers/usersTO_test.py::test_addUserTO_Created PASSED ✅                                 [  8%]
14      src/tests/routers/exercisesTO_test.py::test_getExercisesTO_NoContent PASSED ✅                      [  9%]
15      src/tests/routers/exercisesTO_test.py::test_getExerciseTOById_BadRequest PASSED ✅                  [  9%]
16      src/tests/routers/exercisesTO_test.py::test_getExerciseTOById_NotFound PASSED ✅                    [ 10%]
17      src/tests/routers/exercisesTO_test.py::test_getExercisesTOByCreator_NotFound PASSED ✅              [ 11%]
18      src/tests/routers/exercisesTO_test.py::test_getExercisesTOByCreator_NoContent PASSED ✅             [ 11%]
19      src/tests/routers/exercisesTO_test.py::test_getExerciseTOByName_NotFound PASSED ✅                  [ 12%]
20      src/tests/routers/exercisesTO_test.py::test_addExerciseTO_NotFoundUserTO PASSED ✅                  [ 12%]
21      src/tests/routers/exercisesTO_test.py::test_addExerciseTO_Created PASSED ✅                         [ 13%]
22      src/tests/routers/exercisesTO_test.py::test_addExerciseTO_Conflict PASSED ✅                        [ 14%]
23      src/tests/routers/exercisesTO_test.py::test_getExerciseTO_Ok PASSED ✅                              [ 14%]
24      src/tests/routers/exercisesTO_test.py::test_getExerciseTOById_Ok PASSED ✅                          [ 15%]
25      src/tests/routers/exercisesTO_test.py::test_getExercisesTOByCreator_Ok PASSED ✅                    [ 16%]
26      src/tests/routers/exercisesTO_test.py::test_getExerciseTOByName_Ok PASSED ✅                        [ 16%]
27      src/tests/routers/exercisesTO_test.py::test_updateExerciseTO_BadRequest PASSED ✅                   [ 17%]
28      src/tests/routers/exercisesTO_test.py::test_updateExerciseTO_NotFound PASSED ✅                     [ 18%]
29      src/tests/routers/exercisesTO_test.py::test_updateExerciseTO_Conflict PASSED ✅                     [ 18%]
30      src/tests/routers/exercisesTO_test.py::test_updateExerciseTO_Ok PASSED ✅                           [ 19%]
31      src/tests/routers/exercisesTO_test.py::test_deleteExerciseTO_BadRequest PASSED ✅                   [ 20%]
32      src/tests/routers/exercisesTO_test.py::test_deleteExerciseTO_NotFound PASSED ✅                     [ 20%]
33      src/tests/routers/exercisesTO_test.py::test_deleteExerciseTO_Ok PASSED ✅                           [ 21%]
34      src/tests/routers/routinesTO_test.py::test_getRoutinesTO_NoContent PASSED ✅                        [ 22%]
35      src/tests/routers/routinesTO_test.py::test_getRoutineTOById_BadRequest PASSED ✅                    [ 22%]
36      src/tests/routers/routinesTO_test.py::test_getRoutineTOById_NotFound PASSED ✅                      [ 23%]
37      src/tests/routers/routinesTO_test.py::test_getRoutinesTOByCreator_NotFound PASSED ✅                [ 24%]
38      src/tests/routers/routinesTO_test.py::test_getRoutinesTOByCreator_NoContent PASSED ✅               [ 24%]
39      src/tests/routers/routinesTO_test.py::test_getRoutinesTOByName_NotFound PASSED ✅                   [ 25%]
40      src/tests/routers/routinesTO_test.py::test_addRoutineTO_NotFoundUserTO PASSED ✅                    [ 25%]
41      src/tests/routers/routinesTO_test.py::test_addRoutineTO_Created PASSED ✅                           [ 26%]
42      src/tests/routers/routinesTO_test.py::test_getRoutineTO_Ok PASSED ✅                                [ 27%]
43      src/tests/routers/routinesTO_test.py::test_getRoutineTOById_Ok PASSED ✅                            [ 27%]
44      src/tests/routers/routinesTO_test.py::test_getRoutinesTOByCreator_Ok PASSED ✅                      [ 28%]
45      src/tests/routers/routinesTO_test.py::test_getRoutinesTOByName_Ok PASSED ✅                         [ 29%]
46      src/tests/routers/routinesTO_test.py::test_addExerciseTOToRoutineTO_BadRequestRoutineId PASSED ✅   [ 29%]
47      src/tests/routers/routinesTO_test.py::test_addExerciseTOToRoutineTO_BadRequestExerciseId PASSED ✅  [ 30%]
48      src/tests/routers/routinesTO_test.py::test_addExerciseTOToRoutineTO_NotFoundRoutineId PASSED ✅     [ 31%]
49      src/tests/routers/routinesTO_test.py::test_addExerciseTOToRoutineTO_NotFoundExerciseId PASSED ✅    [ 31%]
50      src/tests/routers/routinesTO_test.py::test_addExerciseTOToRoutineTO_Ok PASSED ✅                    [ 32%]
51      src/tests/routers/routinesTO_test.py::test_addExerciseTOToRoutineTO_Conflict PASSED ✅              [ 33%]
52      src/tests/routers/routinesTO_test.py::test_updateRoutineTO_BadRequest PASSED ✅                     [ 33%]
53      src/tests/routers/routinesTO_test.py::test_updateRoutineTO_NotFound PASSED ✅                       [ 34%]
54      src/tests/routers/routinesTO_test.py::test_updateRoutineTO_Ok PASSED ✅                             [ 35%]
55      src/tests/routers/routinesTO_test.py::test_deleteRoutineTO_BadRequest PASSED ✅                     [ 35%]
56      src/tests/routers/routinesTO_test.py::test_deleteRoutineTO_NotFound PASSED ✅                       [ 36%]
57      src/tests/routers/routinesTO_test.py::test_deleteRoutineTO_Ok PASSED ✅                             [ 37%]
58      src/tests/routers/usersTO_test.py::test_addUserTO_Conflict PASSED ✅                                [ 37%]
59      src/tests/routers/usersTO_test.py::test_getUserTO_Ok PASSED ✅                                      [ 38%]
60      src/tests/routers/usersTO_test.py::test_getUserTOById_Ok PASSED ✅                                  [ 38%]
61      src/tests/routers/usersTO_test.py::test_getUserTOByUsername_Ok PASSED ✅                            [ 39%]
62      src/tests/routers/usersTO_test.py::test_updateUserTO_BadRequest PASSED ✅                           [ 40%]
63      src/tests/routers/usersTO_test.py::test_updateUserTO_NotFound PASSED ✅                             [ 40%]
64      src/tests/routers/usersTO_test.py::test_updateUserTO_Conflict PASSED ✅                             [ 41%]
65      src/tests/routers/usersTO_test.py::test_updateUserTO_Ok PASSED ✅                                   [ 42%]
66      src/tests/routers/usersTO_test.py::test_deleteUserTO_BadRequest PASSED ✅                           [ 42%]
67      src/tests/routers/usersTO_test.py::test_deleteUserTO_NotFound PASSED ✅                             [ 43%]
68      src/tests/routers/usersTO_test.py::test_deleteUserTO_Ok PASSED ✅                                   [ 44%]
69      src/tests/routers/users_test.py::test_addUser_Created PASSED ✅                                     [ 44%]
70      src/tests/routers/posts_test.py::test_getPostByCreator_NoContent PASSED ✅                          [ 45%]
71      src/tests/routers/posts_test.py::test_addPost_NotFound PASSED ✅                                    [ 46%]
72      src/tests/routers/posts_test.py::test_addPost_Created PASSED ✅                                     [ 46%]
73      src/tests/routers/comments_test.py::test_getComments_NoContent PASSED ✅                            [ 47%]
74      src/tests/routers/comments_test.py::test_getCommentById_BadRequest PASSED ✅                        [ 48%]
75      src/tests/routers/comments_test.py::test_getCommentById_NotFound PASSED ✅                          [ 48%]
76      src/tests/routers/comments_test.py::test_getCommentsByCreator_NotFound PASSED ✅                    [ 49%]
77      src/tests/routers/comments_test.py::test_getCommentsByCreator_NoContent PASSED ✅                   [ 50%]
78      src/tests/routers/comments_test.py::test_getPostComments_BadRequest PASSED ✅                       [ 50%]
79      src/tests/routers/comments_test.py::test_getPostComments_NotFound PASSED ✅                         [ 51%]
80      src/tests/routers/comments_test.py::test_getPostComments_NoContent PASSED ✅                        [ 51%]
81      src/tests/routers/comments_test.py::test_addCommentToPost_PostIdBadRequest PASSED ✅                [ 52%]
82      src/tests/routers/comments_test.py::test_addCommentToPost_PostNotFound PASSED ✅                    [ 53%]
83      src/tests/routers/comments_test.py::test_addCommentToPost_UserNotFound PASSED ✅                    [ 53%]
84      src/tests/routers/comments_test.py::test_addCommentToPost_Ok PASSED ✅                              [ 54%]
85      src/tests/routers/comments_test.py::test_getComments_Ok PASSED ✅                                   [ 55%]
86      src/tests/routers/comments_test.py::test_getCommentById_Ok PASSED ✅                                [ 55%]
87      src/tests/routers/comments_test.py::test_getCommentsByCreator_Ok PASSED ✅                          [ 56%]
88      src/tests/routers/comments_test.py::test_getPostComments_Ok PASSED ✅                               [ 57%]
89      src/tests/routers/comments_test.py::test_udpateCommentFromPost_BadRequest PASSED ✅                 [ 57%]
90      src/tests/routers/comments_test.py::test_udpateCommentFromPost_CommentNotFound PASSED ✅            [ 58%]
91      src/tests/routers/comments_test.py::test_udpateCommentFromPost_PostNotFound PASSED ✅               [ 59%]
92      src/tests/routers/comments_test.py::test_udpateCommentFromPost_UserNotFound PASSED ✅               [ 59%]
93      src/tests/routers/comments_test.py::test_udpateCommentFromPost_Ok PASSED ✅                         [ 60%]
94      src/tests/routers/comments_test.py::test_deleteCommentFromPost_BadRequest PASSED ✅                 [ 61%]
95      src/tests/routers/comments_test.py::test_deleteCommentFromPost_CommentNotFound PASSED ✅            [ 61%]
96      src/tests/routers/comments_test.py::test_deleteCommentFromPost_Ok PASSED ✅                         [ 62%]
97      src/tests/routers/comments_test.py::test_deleteAllPostComments_BadRequest PASSED ✅                 [ 62%]
98      src/tests/routers/comments_test.py::test_deleteAllPostComments_NotFound PASSED ✅                   [ 63%]
99      src/tests/routers/comments_test.py::test_deleteAllPostComments_Ok PASSED ✅                         [ 64%]
100      src/tests/routers/comments_test.py::test_deleteAllPostComments_NoContent PASSED ✅                  [ 64%]
101      src/tests/routers/posts_test.py::test_getPosts_Ok PASSED ✅                                         [ 65%]
102      src/tests/routers/posts_test.py::test_getPostById_Ok PASSED ✅                                      [ 66%]
103      src/tests/routers/posts_test.py::test_getPostsByCreator_Ok PASSED ✅                                [ 66%]
104      src/tests/routers/posts_test.py::test_updatePost_BadRequest PASSED ✅                               [ 67%]
105      src/tests/routers/posts_test.py::test_updatePost_NotFound PASSED ✅                                 [ 68%]
106      src/tests/routers/posts_test.py::test_updatePost_NoContent PASSED ✅                                [ 68%]
107      src/tests/routers/posts_test.py::test_updatePost_User_NotFound PASSED ✅                            [ 69%]
108      src/tests/routers/posts_test.py::test_updatePost_Created PASSED ✅                                  [ 70%]
109      src/tests/routers/posts_test.py::test_deletePost_BadRequest PASSED ✅                               [ 70%]
110      src/tests/routers/posts_test.py::test_deletePost_NotFound PASSED ✅                                 [ 71%]
111      src/tests/routers/posts_test.py::test_deletePost_Ok PASSED ✅                                       [ 72%]
112      src/tests/routers/posts_test.py::test_deleteAllCreatorPosts_NotFound PASSED ✅                      [ 72%]
113      src/tests/routers/posts_test.py::test_deleteAllCreatorPosts_Ok PASSED ✅                            [ 73%]
114      src/tests/routers/routines_test.py::test_getRoutineByCreator_NoContent PASSED ✅                    [ 74%]
115      src/tests/routers/routines_test.py::test_addRoutine_NotFound PASSED ✅                              [ 74%]
116      src/tests/routers/routines_test.py::test_addRoutine_Created PASSED ✅                               [ 75%]
117      src/tests/routers/routines_test.py::test_getRoutines_Ok PASSED ✅                                   [ 75%]
118      src/tests/routers/routines_test.py::test_getRoutineById_Ok PASSED ✅                                [ 76%]
119      src/tests/routers/routines_test.py::test_getRoutinesByCreator_Ok PASSED ✅                          [ 77%]
120      src/tests/routers/routines_test.py::test_updateRoutine_BadRequest PASSED ✅                         [ 77%]
121      src/tests/routers/routines_test.py::test_updateRoutine_NotFound PASSED ✅                           [ 78%]
122      src/tests/routers/routines_test.py::test_updateRoutine_NoContent PASSED ✅                          [ 79%]
123      src/tests/routers/routines_test.py::test_updateRoutine_UserNotFound PASSED ✅                       [ 79%]
124      src/tests/routers/routines_test.py::test_updateRoutine_Created PASSED ✅                            [ 80%]
125      src/tests/routers/routines_test.py::test_deleteRoutine_BadRequest PASSED ✅                         [ 81%]
126      src/tests/routers/routines_test.py::test_deleteRoutine_NotFound PASSED ✅                           [ 81%]
127      src/tests/routers/routines_test.py::test_deleteRoutine_Ok PASSED ✅                                 [ 82%]
128      src/tests/routers/routines_test.py::test_deleteAllCreatorRoutines_NotFound PASSED ✅                [ 83%]
129      src/tests/routers/routines_test.py::test_deleteAllCreatorRoutines_Ok PASSED ✅                      [ 83%]
130      src/tests/routers/users_test.py::test_getPublicUsers_BadRequest PASSED ✅                           [ 84%]
131      src/tests/routers/users_test.py::test_getPublicUsers_All_Ok PASSED ✅                               [ 85%]
132      src/tests/routers/users_test.py::test_getPublicUsers_ById_Ok PASSED ✅                              [ 85%]
133      src/tests/routers/users_test.py::test_getPublicUsers_ByUsername_Ok PASSED ✅                        [ 86%]
134      src/tests/routers/users_test.py::test_followUser_Ok PASSED ✅                                       [ 87%]
135      src/tests/routers/users_test.py::test_followUser_NoContent PASSED ✅                                [ 87%]
136      src/tests/routers/users_test.py::test_unfollowUser_Ok PASSED ✅                                     [ 88%]
137      src/tests/routers/users_test.py::test_unfollowUser_NoContent PASSED ✅                              [ 88%]
138      src/tests/routers/users_test.py::test_getUsers_Ok PASSED ✅                                         [ 89%]
139      src/tests/routers/users_test.py::test_addUser_Conflict PASSED ✅                                    [ 90%]
140      src/tests/routers/users_test.py::test_getUserById_Ok PASSED ✅                                      [ 90%]
141      src/tests/routers/users_test.py::test_getUserById_BadRequest PASSED ✅                              [ 91%]
142      src/tests/routers/users_test.py::test_getUserById_NotFound PASSED ✅                                [ 92%]
143      src/tests/routers/users_test.py::test_getUserByUsername_Ok PASSED ✅                                [ 92%]
144      src/tests/routers/users_test.py::test_updateUser_NoContent PASSED ✅                                [ 93%]
145      src/tests/routers/users_test.py::test_updateUser_Ok PASSED ✅                                       [ 94%]
146      src/tests/routers/users_test.py::test_getUserByUsername_NotFound PASSED ✅                          [ 94%]
147      src/tests/routers/users_test.py::test_updateUser_BadRequest PASSED ✅                               [ 95%]
148      src/tests/routers/users_test.py::test_updateUser_NotFound PASSED ✅                                 [ 96%]
149      src/tests/routers/users_test.py::test_updateUser_Conflict PASSED ✅                                 [ 96%]
150      src/tests/routers/users_test.py::test_deleteUser_Ok PASSED ✅                                       [ 97%]
151      src/tests/routers/users_test.py::test_deleteUser_BadRequest PASSED ✅                               [ 98%]
152      src/tests/routers/users_test.py::test_deleteUser_NotFound PASSED ✅                                 [ 98%]
153      src/tests/routers/users_test.py::test_deleteAllUsers_Ok PASSED ✅                                   [ 99%]
154      src/tests/routers/users_test.py::test_getUsers_NoContent PASSED ✅                                  [100%]
```

</details>

### UNIT TESTS IMPLEMENTED
<details>
<summary>The following tests have been stated</summary>
<br>
        
| # | Test Name | Description | Status |
| --- | --- | --- | --- |
| 1  | `test_getPosts_NoContent`                   | Test getting posts (204 - No Content)           | ✅     |
| 2  | `test_getPostById_BadRequest`               | Test getting post by ID (400 - Bad Request)     | ✅     |
| 3  | `test_getPostById_NotFound`                 | Test getting post by ID (404 - Not Found)       | ✅     |
| 4  | `test_getPostByCreator_NotFound`            | Test getting post by creator (404 - Not Found)  | ✅     |
| 5  | `test_getRoutines_NoContent`                | Test getting routines (204 - No Content)        | ✅     |
| 6  | `test_getRoutineById_BadRequest`            | Test getting routine by ID (400 - Bad Request)  | ✅     |
| 7  | `test_getRoutineById_NotFound`              | Test getting routine by ID (404 - Not Found)    | ✅     |
| 8  | `test_getRoutineByCreator_NotFound`         | Test getting routine by creator (404 - Not Found)| ✅     |
| 9  | `test_getUsersTO_NoContent`                 | Test getting users (204 - No Content)           | ✅     |
| 10 | `test_getUserTOById_BadRequest`             | Test getting user by ID (400 - Bad Request)     | ✅     |
| 11 | `test_getUserTOById_NotFound`               | Test getting user by ID (404 - Not Found)       | ✅     |
| 12 | `test_getUserTOByUsername_NotFound`         | Test getting user by username (404 - Not Found) | ✅     |
| 13 | `test_addUserTO_Created`                    | Test adding user (201 - Created)                | ✅     |
| 14 | `test_getExercisesTO_NoContent`             | Test getting exercises (204 - No Content)       | ✅     |
| 15 | `test_getExerciseTOById_BadRequest`         | Test getting exercise by ID (400 - Bad Request) | ✅     |
| 16 | `test_getExerciseTOById_NotFound`           | Test getting exercise by ID (404 - Not Found)   | ✅     |
| 17 | `test_getExercisesTOByCreator_NotFound`     | Test getting exercises by creator (404 - Not Found) | ✅  |
| 18 | `test_getExercisesTOByCreator_NoContent`    | Test getting exercises by creator (204 - No Content) | ✅ |
| 19 | `test_getExerciseTOByName_NotFound`         | Test getting exercise by name (404 - Not Found) | ✅    |
| 20 | `test_addExerciseTO_NotFoundUserTO`         | Test adding exercise with not found user (404 - Not Found) | ✅ |
| 21 | `test_addExerciseTO_Created`                | Test adding exercise (201 - Created)            | ✅     |
| 22 | `test_addExerciseTO_Conflict`               | Test adding exercise with conflict (409 - Conflict) | ✅  |
| 23 | `test_getExerciseTO_Ok`                     | Test getting exercise (200 - OK)                | ✅     |
| 24 | `test_getExerciseTOById_Ok`                 | Test getting exercise by ID (200 - OK)           | ✅     |
| 25 | `test_getExercisesTOByCreator_Ok`           | Test getting exercises by creator (200 - OK)     | ✅     |
| 26 | `test_getExerciseTOByName_Ok`               | Test getting exercise by name (200 - OK)         | ✅     |
| 27 | `test_updateExerciseTO_BadRequest`          | Test updating exercise (400 - Bad Request)       | ✅     |
| 28 | `test_updateExerciseTO_NotFound`            | Test updating exercise (404 - Not Found)         | ✅     |
| 29 | `test_updateExerciseTO_Conflict`            | Test updating exercise with conflict (409 - Conflict) | ✅ |
| 30 | `test_updateExerciseTO_Ok`                  | Test updating exercise (200 - OK)                | ✅     |
| 31 | `test_deleteExerciseTO_BadRequest`          | Test deleting exercise (400 - Bad Request)       | ✅     |
| 32 | `test_deleteExerciseTO_NotFound`            | Test deleting exercise (404 - Not Found)         | ✅     |
| 33 | `test_deleteExerciseTO_Ok`                  | Test deleting exercise (200 - OK)                | ✅     |
| 34 | `test_getRoutinesTO_NoContent`              | Test getting routines (204 - No Content)         | ✅     |
| 35 | `test_getRoutineTOById_BadRequest`          | Test getting routine by ID (400 - Bad Request)   | ✅     |
| 36 | `test_getRoutineTOById_NotFound`            | Test getting routine by ID (404 - Not Found)     | ✅     |
| 37 | `test_getRoutinesTOByCreator_NotFound`      | Test getting routines by creator (404 - Not Found) | ✅ |
| 38 | `test_getRoutinesTOByCreator_NoContent`     | Test getting routines by creator (204 - No Content) | ✅ |
| 39 | `test_getRoutinesTOByName_NotFound`         | Test getting routines by name (404 - Not Found) | ✅   |
| 40 | `test_addRoutineTO_NotFoundUserTO`          | Test adding routine with not found user (404 - Not Found) | ✅ |
| 41 | `test_addRoutineTO_Created`                 | Test adding routine (201 - Created)              | ✅     |
| 42 | `test_getRoutineTO_Ok`                      | Test getting routine (200 - OK)                  | ✅     |
| 43 | `test_getRoutineTOById_Ok`                  | Test getting routine by ID (200 - OK)            | ✅     |
| 44 | `test_getRoutinesTOByCreator_Ok`            | Test getting routines by creator (200 - OK)      | ✅     |
| 45 | `test_getRoutinesTOByName_Ok`               | Test getting routines by name (200 - OK)         | ✅     |
| 46 | `test_addExerciseTOToRoutineTO_BadRequestRoutineId` | Test adding exercise to routine (400 - Bad Request - Routine ID) | ✅ |
| 47 | `test_addExerciseTOToRoutineTO_BadRequestExerciseId` | Test adding exercise to routine (400 - Bad Request - Exercise ID) | ✅ |
| 48 | `test_addExerciseTOToRoutineTO_NotFoundRoutineId` | Test adding exercise to routine (404 - Not Found - Routine ID) | ✅ |
| 49 | `test_addExerciseTOToRoutineTO_NotFoundExerciseId` | Test adding exercise to routine (404 - Not Found - Exercise ID) | ✅ |
| 50 | `test_addExerciseTOToRoutineTO_Ok`          | Test adding exercise to routine (200 - OK)       | ✅     |
| 51 | `test_addExerciseTOToRoutineTO_Conflict`     | Test adding exercise to routine (409 - Conflict) | ✅     |
| 52 | `test_updateRoutineTO_BadRequest`           | Test updating routine (400 - Bad Request)        | ✅     |
| 53 | `test_updateRoutineTO_NotFound`             | Test updating routine (404 - Not Found)          | ✅     |
| 54 | `test_updateRoutineTO_Ok`                   | Test updating routine (200 - OK)                 | ✅     |
| 55 | `test_deleteRoutineTO_BadRequest`           | Test deleting routine (400 - Bad Request)        | ✅     |
| 56 | `test_deleteRoutineTO_NotFound`             | Test deleting routine (404 - Not Found)          | ✅     |
| 57 | `test_deleteRoutineTO_Ok`                   | Test deleting routine (200 - OK)                 | ✅     |
| 58 | `test_addUserTO_Conflict`                   | Test adding user (409 - Conflict)                | ✅     |
| 59 | `test_getUserTO_Ok`                         | Test getting user (200 - OK)                    | ✅     |
| 60 | `test_getUserTOById_Ok`                     | Test getting user by ID (200 - OK)              | ✅     |
| 61 | `test_getUserTOByUsername_Ok`               | Test getting user by username (200 - OK)        | ✅     |
| 62 | `test_updateUserTO_BadRequest`              | Test updating user (400 - Bad Request)          | ✅     |
| 63 | `test_updateUserTO_NotFound`                | Test updating user (404 - Not Found)            | ✅     |
| 64 | `test_updateUserTO_Conflict`                | Test updating user (409 - Conflict)              | ✅     |
| 65 | `test_updateUserTO_Ok`                      | Test updating user (200 - OK)                   | ✅     |
| 66 | `test_deleteUserTO_BadRequest`              | Test deleting user (400 - Bad Request)          | ✅     |
| 67 | `test_deleteUserTO_NotFound`                | Test deleting user (404 - Not Found)            | ✅     |
| 68 | `test_deleteUserTO_Ok`                      | Test deleting user (200 - OK)                   | ✅     |
| 69 | `test_addUser_Created`                      | Test adding user (201 - Created)                | ✅     |
| 70 | `test_getPostByCreator_NoContent`           | Test getting post by creator (204 - No Content)  | ✅     |
| 71 | `test_addPost_NotFound`                     | Test adding post (404 - Not Found)              | ✅     |
| 72 | `test_addPost_Created`                      | Test adding post (201 - Created)                | ✅     |
| 73 | `test_getComments_NoContent`                | Test getting comments (204 - No Content)        | ✅     |
| 74 | `test_getCommentById_BadRequest`            | Test getting comment by ID (400 - Bad Request)  | ✅     |
| 75 | `test_getCommentById_NotFound`              | Test getting comment by ID (404 - Not Found)    | ✅     |
| 76 | `test_getCommentsByCreator_NotFound`        | Test getting comments by creator (404 - Not Found) | ✅ |
| 77 | `test_getCommentsByCreator_NoContent`       | Test getting comments by creator (204 - No Content) | ✅ |
| 78 | `test_getPostComments_BadRequest`           | Test getting post comments (400 - Bad Request)  | ✅     |
| 79 | `test_getPostComments_NotFound`             | Test getting post comments (404 - Not Found)    | ✅     |
| 80 | `test_getPostComments_NoContent`            | Test getting post comments (204 - No Content)   | ✅     |
| 81 | `test_addCommentToPost_PostIdBadRequest`    | Test adding comment to post (400 - Bad Request - Post ID) | ✅ |
| 82 | `test_addCommentToPost_PostNotFound`        | Test adding comment to post (404 - Not Found - Post) | ✅ |
| 83 | `test_addCommentToPost_UserNotFound`        | Test adding comment to post (404 - Not Found - User) | ✅ |
| 84 | `test_addCommentToPost_Ok`                  | Test adding comment to post (200 - OK)           | ✅     |
| 85 | `test_getComments_Ok`                       | Test getting comments (200 - OK)                | ✅     |
| 86 | `test_getCommentById_Ok`                    | Test getting comment by ID (200 - OK)           | ✅     |
| 87 | `test_getCommentsByCreator_Ok`              | Test getting comments by creator (200 - OK)     | ✅     |
| 88 | `test_getPostComments_Ok`                   | Test getting post comments (200 - OK)           | ✅     |
| 89 | `test_udpateCommentFromPost_BadRequest`     | Test updating comment (400 - Bad Request)       | ✅     |
| 90 | `test_udpateCommentFromPost_CommentNotFound`| Test updating comment (404 - Not Found - Comment) | ✅ |
| 91 | `test_udpateCommentFromPost_PostNotFound`   | Test updating comment (404 - Not Found - Post)   | ✅     |
| 92 | `test_udpateCommentFromPost_UserNotFound`   | Test updating comment (404 - Not Found - User)   | ✅     |
| 93 | `test_udpateCommentFromPost_Ok`             | Test updating comment (200 - OK)                | ✅     |
| 94 | `test_deleteCommentFromPost_BadRequest`     | Test deleting comment (400 - Bad Request)       | ✅     |
| 95 | `test_deleteCommentFromPost_CommentNotFound`| Test deleting comment (404 - Not Found - Comment) | ✅ |
| 96 | `test_deleteCommentFromPost_Ok`             | Test deleting comment (200 - OK)                | ✅     |
| 97 | `test_deleteAllPostComments_BadRequest`     | Test deleting all post comments (400 - Bad Request) | ✅ |
| 98 | `test_deleteAllPostComments_NotFound`       | Test deleting all post comments (404 - Not Found) | ✅ |
| 99 | `test_deleteAllPostComments_Ok`             | Test deleting all post comments (200 - OK)      | ✅     |
| 100| `test_deleteAllPostComments_NoContent`      | Test deleting all post comments (204 - No Content) | ✅ |
| 101| `test_getPosts_Ok`                          | Test getting posts (200 - OK)                   | ✅     |
| 102| `test_getPostById_Ok`                       | Test getting post by ID (200 - OK)              | ✅     |
| 103| `test_getPostsByCreator_Ok`                 | Test getting posts by creator (200 - OK)        | ✅     |
| 104| `test_updatePost_BadRequest`                | Test updating post (400 - Bad Request)          | ✅     |
| 105| `test_updatePost_NotFound`                  | Test updating post (404 - Not Found)            | ✅     |
| 106| `test_updatePost_NoContent`                 | Test updating post (204 - No Content)           | ✅     |
| 107| `test_updatePost_User_NotFound`             | Test updating post (404 - Not Found - User)     | ✅     |
| 108| `test_updatePost_Created`                   | Test updating post (201 - Created)              | ✅     |
| 109| `test_deletePost_BadRequest`                | Test deleting post (400 - Bad Request)          | ✅     |
| 110| `test_deletePost_NotFound`                  | Test deleting post (404 - Not Found)            | ✅     |
| 111| `test_deletePost_Ok`                        | Test deleting post (200 - OK)                   | ✅     |
| 112| `test_deleteAllCreatorPosts_NotFound`       | Test deleting all posts by creator (404 - Not Found) | ✅ |
| 113| `test_deleteAllCreatorPosts_Ok`             | Test deleting all posts by creator (200 - OK)   | ✅     |
| 114| `test_getRoutineByCreator_NoContent`        | Test getting routine by creator (204 - No Content) | ✅ |
| 115| `test_addRoutine_NotFound`                  | Test adding routine (404 - Not Found)           | ✅     |
| 116| `test_addRoutine_Created`                   | Test adding routine (201 - Created)              | ✅     |
| 117| `test_getRoutines_Ok`                       | Test getting routines (200 - OK)                | ✅     |
| 118| `test_getRoutineById_Ok`                    | Test getting routine by ID (200 - OK)           | ✅     |
| 119| `test_getRoutinesByCreator_Ok`              | Test getting routines by creator (200 - OK)     | ✅     |
| 120| `test_updateRoutine_BadRequest`             | Test updating routine (400 - Bad Request)       | ✅     |
| 121| `test_updateRoutine_NotFound`               | Test updating routine (404 - Not Found)         | ✅     |
| 122| `test_updateRoutine_NoContent`              | Test updating routine (204 - No Content)        | ✅     |
| 123| `test_updateRoutine_UserNotFound`           | Test updating routine (404 - Not Found - User)  | ✅     |
| 124| `test_updateRoutine_Created`                | Test updating routine (201 - Created)           | ✅     |
| 125| `test_deleteRoutine_BadRequest`             | Test deleting routine (400 - Bad Request)       | ✅     |
| 126| `test_deleteRoutine_NotFound`               | Test deleting routine (404 - Not Found)         | ✅     |
| 127| `test_deleteRoutine_Ok`                     | Test deleting routine (200 - OK)                | ✅     |
| 128| `test_deleteAllCreatorRoutines_NotFound` | Test deleting all routines of creator with not found user (404 - Not Found) | ✅ |
| 129| `test_deleteAllCreatorRoutines_Ok` | Test deleting all routines of creator (200 - OK) | ✅ |
| 130| `test_getPublicUsers_BadRequest`     | Test getting public users with bad request (400 - Bad Request)       | ✅ |
| 131| `test_getPublicUsers_All_Ok`         | Test getting all public users (200 - OK)                              | ✅ |
| 132| `test_getPublicUsers_ById_Ok`       | Test getting public user by ID (200 - OK)                             | ✅ |
| 133| `test_getPublicUsers_ByUsername_Ok` | Test getting public user by username (200 - OK)                       | ✅ |
| 134| `test_followUser_Ok`                 | Test following a user (200 - OK)                                      | ✅ |
| 135| `test_followUser_NoContent`          | Test following a user with no content (204 - No Content)              | ✅ |
| 136| `test_unfollowUser_Ok`               | Test unfollowing a user (200 - OK)                                    | ✅ |
| 137| `test_unfollowUser_NoContent`        | Test unfollowing a user with no content (204 - No Content)            | ✅ |
| 138| `test_getUsers_Ok`                   | Test getting users (200 - OK)                                         | ✅ |
| 139| `test_addUser_Conflict`             | Test adding a user with conflict (409 - Conflict)                     | ✅ |
| 140| `test_getUserById_Ok`                | Test getting user by ID (200 - OK)                                    | ✅ |
| 141| `test_getUserById_BadRequest`        | Test getting user by ID with bad request (400 - Bad Request)          | ✅ |
| 142| `test_getUserById_NotFound`          | Test getting user by ID not found (404 - Not Found)                   | ✅ |
| 143| `test_getUserByUsername_Ok`          | Test getting user by username (200 - OK)                               | ✅ |
| 144| `test_updateUser_NoContent`          | Test updating user with no content (204 - No Content)                  | ✅ |
| 145| `test_updateUser_Ok`                 | Test updating user (200 - OK)                                         | ✅ |
| 146| `test_getUserByUsername_NotFound`    | Test getting user by username not found (404 - Not Found)              | ✅ |
| 147| `test_updateUser_BadRequest`         | Test updating user with bad request (400 - Bad Request)                | ✅ |
| 148| `test_updateUser_NotFound`           | Test updating user not found (404 - Not Found)                         | ✅ |
| 149| `test_updateUser_Conflict`           | Test updating user with conflict (409 - Conflict)                       | ✅ |
| 150| `test_deleteUser_Ok`                 | Test deleting user (200 - OK)                                         | ✅ |
| 151| `test_deleteUser_BadRequest`         | Test deleting user with bad request (400 - Bad Request)                | ✅ |
| 152| `test_deleteUser_NotFound`           | Test deleting user not found (404 - Not Found)                         | ✅ |
| 153| `test_deleteAllUsers_Ok`             | Test deleting all users (200 - OK)                                     | ✅ |
| 154| `test_getUsers_NoContent`            | Test getting users with no content (204 - No Content)                   | ✅ |

</details>
