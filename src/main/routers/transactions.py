from utils.logger import logging

from src.main.services.auth import Auth
import src.main.routers.usersTO as usersTO

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer("/transactions")
auth_handler = Auth()


async def authenticate_user(username, password):
    logging.info(f"The user {username} is being authenticate")
    user_auth = await usersTO.getUserTOByUsername(username)
    if not auth_handler.verify_password(password, user_auth.password):
        logging.info("The credentials are not valid to continue the authentication")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_auth


@router.get("/root")
def root(token: str = Depends(oauth2_scheme)):
    return "Welcome to eGym! This is your token --> " + token


@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logging.info(f"The user {form_data.username} is trying to access")
    try:
        user_auth = await authenticate_user(form_data.username, form_data.password)
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
