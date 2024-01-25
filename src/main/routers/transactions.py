from utils.logger import logging

from db.sqlDB.models.userTO import UserTO
from db.mongodb.models.user import User
from db.sqlDB.schemas.userTO import userTO_schema
from db.mongodb.schemas.user import user_schema

from src.main.models.user_register import UserRegister
from src.main.services.auth import Auth
import src.main.routers.usersTO as usersTO
import src.main.routers.users as users

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer("/transactions/login")
auth_handler = Auth()


async def authenticate_user(username, password):
    logging.info(f"The user {username} is being authenticate")
    try:
        user_auth = await usersTO.getUserTOByUsernameRequest(username)
    except HTTPException as e:
        if e.status_code == 404:
            logging.info("The credentials are not valid to continue the authentication")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            logging.info("Failed to login user - Error message: " + str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to login user",
            )
    if not auth_handler.verify_password(password, user_auth.password):
        logging.info("The credentials are not valid to continue the authentication")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_auth


# @router.get("/root")
# def root(token: str = Depends(oauth2_scheme)):
#     if auth_handler.decode_token(token) != None:
#         return "Welcome to eGym! This is your token --> " + token


@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # !REQUIREMENTS: To satisfy ASE2E login data should be encoded in client-side, decoded in server-side and then treated as plain text
    # !REQUIREMENTS: I think that a good idea is to encode the passwordin client-side and then encode the whole message again { user / password }
    # TODO: Should be fine returning the User model, so the application should not do another petition to get that information
    logging.info(f"The user {form_data.username} is trying to access")
    user_auth = await authenticate_user(form_data.username, form_data.password)
    try:
        # * form_data_decoded = await decode_form_data(form_data) -> In "decode_form_data" method the whole message should be decoded and then the password should be decoded aswell
        logging.info(f"The user {user_auth.username} has been authenticated")
        access_token = auth_handler.encode_token(user_auth.username)
        refresh_token = auth_handler.encode_refresh_token(user_auth.username)
        logging.info(f"The user {user_auth.username} has been authorized")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except BaseException as e:
        logging.info("Failed to login user - Error message: " + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login user",
        )


@router.post(
    "/register", response_model=UserRegister, status_code=status.HTTP_201_CREATED
)
async def register(input_user_registered: UserRegister):
    # !REQUIREMENTS: The data should be send encoded and then should be decoded by the server to satisfy end-to-end encryption to accomplish security requirements
    # ?IMPLEMENTATION: Should return the token so the user can be logged in?
    # TODO: Input parameters { UserTO } -> addUserTO verifies if exists and adds it into database -> Should return to the application the response and the UserTO
    # * userTO_decoded = await decode_userTO(userTO) -> It should return the JSON object decoded, which will remain encrypted is the password, which have a double encryption
    input_user_registered.password = auth_handler.encode_password(
        input_user_registered.password
    )
    input_user_registered.fullname = (
        input_user_registered.firstname + " " + input_user_registered.lastname
    )
    user_dict = dict(input_user_registered)
    user_dict["_id"] = "to_be_defined"

    userTO = UserTO(**userTO_schema(user_dict))
    userTO_registered = await usersTO.addUserTO(userTO)

    user = User(**user_schema(user_dict))
    user_registered = await users.addUser(user)

    return input_user_registered
