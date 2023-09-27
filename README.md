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

### **LAST PR COVERAGE REPORT *(src/tests/reports/index.html)* - `Coverage report: 50%`**

<details open>
<summary>Check the coverage report</summary>
<br>
<table class="index" data-sortable="">
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left" aria-sort="descending" data-shortcut="n">Module</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="x">excluded</th>
                <th class="right" aria-sort="none" data-shortcut="c">coverage</th>
            </tr>
        </thead>
        <tbody>
        <tr class="file">
                <td class="name left"><a href="d_c810615cce0f7acb_logger_py.html">utils/logger.py</a></td>
                <td>20</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="20 20">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_4cb59d3976f21776_users_test_py.html">src/tests/routers/users_test.py</a></td>
                <td>124</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="124 124">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_4cb59d3976f21776_comments_test_py.html">src/tests/routers/comments_test.py</a></td>
                <td>23</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="23 23">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_4cb59d3976f21776___init___py.html">src/tests/routers/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_08b4cb1648a15a99_main_test_py.html">src/tests/main_test.py</a></td>
                <td>13</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="13 13">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_08b4cb1648a15a99___init___py.html">src/tests/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_usersTO_py.html">src/main/routers/usersTO.py</a></td>
                <td>72</td>
                <td>52</td>
                <td>0</td>
                <td class="right" data-ratio="20 72">28%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_users_py.html">src/main/routers/users.py</a></td>
                <td>148</td>
                <td>30</td>
                <td>0</td>
                <td class="right" data-ratio="118 148">80%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_routinesTO_py.html">src/main/routers/routinesTO.py</a></td>
                <td>122</td>
                <td>95</td>
                <td>0</td>
                <td class="right" data-ratio="27 122">22%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_routines_py.html">src/main/routers/routines.py</a></td>
                <td>174</td>
                <td>135</td>
                <td>0</td>
                <td class="right" data-ratio="39 174">22%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_posts_py.html">src/main/routers/posts.py</a></td>
                <td>166</td>
                <td>126</td>
                <td>0</td>
                <td class="right" data-ratio="40 166">24%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_exercisesTO_py.html">src/main/routers/exercisesTO.py</a></td>
                <td>86</td>
                <td>64</td>
                <td>0</td>
                <td class="right" data-ratio="22 86">26%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_0967d60ec74c5f34_comments_py.html">src/main/routers/comments.py</a></td>
                <td>186</td>
                <td>136</td>
                <td>0</td>
                <td class="right" data-ratio="50 186">27%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_5f1512723eddbe79_main_py.html">src/main/main.py</a></td>
                <td>22</td>
                <td>1</td>
                <td>0</td>
                <td class="right" data-ratio="21 22">95%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_3facd73e22d9d899_userTO_py.html">db/sqlDB/schemas/userTO.py</a></td>
                <td>4</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="2 4">50%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_3facd73e22d9d899_routineTO_py.html">db/sqlDB/schemas/routineTO.py</a></td>
                <td>4</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="2 4">50%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_3facd73e22d9d899_exerciseTO_py.html">db/sqlDB/schemas/exerciseTO.py</a></td>
                <td>4</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="2 4">50%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_098731541c99038c_userTO_py.html">db/sqlDB/models/userTO.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_098731541c99038c_routineTO_py.html">db/sqlDB/models/routineTO.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_098731541c99038c_exerciseTO_py.html">db/sqlDB/models/exerciseTO.py</a></td>
                <td>7</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="7 7">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_8bd27d18406d48c9_client_py.html">db/sqlDB/client.py</a></td>
                <td>7</td>
                <td>1</td>
                <td>0</td>
                <td class="right" data-ratio="6 7">86%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_44ec700dd9da9519_user_py.html">db/mongodb/schemas/user.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_44ec700dd9da9519_routine_py.html">db/mongodb/schemas/routine.py</a></td>
                <td>4</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="2 4">50%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_44ec700dd9da9519_post_py.html">db/mongodb/schemas/post.py</a></td>
                <td>4</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="2 4">50%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_44ec700dd9da9519_comment_py.html">db/mongodb/schemas/comment.py</a></td>
                <td>4</td>
                <td>1</td>
                <td>0</td>
                <td class="right" data-ratio="3 4">75%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c86a4e7de3c3b4b2_user_py.html">db/mongodb/models/user.py</a></td>
                <td>24</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="24 24">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c86a4e7de3c3b4b2_set_py.html">db/mongodb/models/set.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c86a4e7de3c3b4b2_routine_py.html">db/mongodb/models/routine.py</a></td>
                <td>14</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="14 14">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c86a4e7de3c3b4b2_post_py.html">db/mongodb/models/post.py</a></td>
                <td>12</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="12 12">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c86a4e7de3c3b4b2_exercise_py.html">db/mongodb/models/exercise.py</a></td>
                <td>12</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="12 12">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c86a4e7de3c3b4b2_comment_py.html">db/mongodb/models/comment.py</a></td>
                <td>8</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="8 8">100%</td>
            </tr><tr class="file">
                <td class="name left"><a href="d_c88e774a1055ac67_client_py.html">db/mongodb/client.py</a></td>
                <td>14</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="12 14">86%</td>
            </tr><tr class="file">
                <td class="name left"><a href="conftest_py.html">conftest.py</a></td>
                <td>10</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="10 10">100%</td>
            </tr></tbody>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>1319</td>
                <td>653</td>
                <td>0</td>
                <td class="right" data-ratio="666 1319">50%</td>
            </tr>
        </tfoot>
    </table>
</details>
