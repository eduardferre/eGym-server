# **eGym-server - BACKEND**
Welcome to my thesis degree project, this repository contains all the specifications related to the backend of the application.

In this README you can find some important information about the creation of the backend itself. Information such which databases have been used, which API structure has been chosen and the deployment of the API.

## **API**
The API is formed by the following endpoints with their respective methods.

### ***UsersTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | usersTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all users |
| GET       | usersTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get user by id |
| POST    | usersTO/ | -                     | 201_CREATED / 226_IM_USED | Add user |
| PUT       | usersTO/ | -                    | 201_CREATED / 404_NOT_FOUND | Update user info |
| DELETE | usersTO/ | {username}  | 200_OK / 404_NOT_FOUND | Delete a user by username |


### ***ExercisesTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | exercisesTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all exercises |
| GET       | exercisesTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get exercise by id |
| GET       | exercisesTO/ | {creator}                | 200_OK / 404_NOT_FOUND | Get exercises by creator |
| GET       | exercisesTO/ | {name}                | 200_OK / 404_NOT_FOUND | Get exercises by name |
| POST    | exercisesTO/ | -                     | 201_CREATED / 226_IM_USED | Add exercise |
| PUT       | exercisesTO/ | -                    | 201_CREATED / 404_NOT_FOUND | Update exercise info |
| DELETE | exercisesTO/ | {name}  | 200_OK / 404_NOT_FOUND | Delete an exercise by name |


### ***RoutinesTO (Transfer Object)** - SQL DATABASE*
| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | routinesTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all routines |
| GET       | routinesTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get routine by id |
| GET       | routinesTO/ | {creator}                | 200_OK / 404_NOT_FOUND | Get routines by creator |
| GET       | routinesTO/ | {name}                | 200_OK / 404_NOT_FOUND | Get routines by name |
| POST    | routinesTO/ | -                     | 201_CREATED | Add routine |
| PUT       | routinesTO/ | -                    | 201_CREATED / 404_NOT_FOUND | Update routine info |
| DELETE | routinesTO/ | {id}  | 200_OK / 404_NOT_FOUND | Delete a routine by id |
