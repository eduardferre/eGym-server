# eGym-server - BACKEND
Welcome to my thesis degree project, this repository contains all the specifications related to the backend of the application.

In this README you can find some important information about the creation of the backend itself. Information such which databases have been used, which API structure has been chosen and the deployment of the API.

## API
The API is formed by the following endpoints with their respective methods

| Method | Path        | Subpath       | Codes | Description |
|---------|----------|-------------|--------|--------|
| GET       | usersTO/ | -                    | 200_OK / 204_NO_CONTENT | Get all users |
| GET       | usersTO/ | {id}                | 200_OK / 404_NOT_FOUND | Get user by id |
| POST    | usersTO/ | -                     | 201_CREATED / 226_IM_USED | Add user |
| PUT       | usersTO/ | -                    | 201_CREATED / 404_NOT_FOUND | Update user info |
| DELETE | usersTO/ | {username}  | 200_OK / 404_NOT_FOUND | Delete a user by username |
