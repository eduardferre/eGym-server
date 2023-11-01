import os
import logging
import base64
import json
import jwt

from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import HTTPException, status
from passlib.context import CryptContext

from jwt.algorithms import ECAlgorithm


def load_ES256_from_jwk_env():
    load_dotenv(override=True)
    algorithm = ECAlgorithm("ES256")
    key = os.getenv("ES256_KEY")
    encode_key = base64.b64decode(key)
    json_key = json.loads(encode_key)
    ES256_key = algorithm.from_jwk(json_key.get("keys")[0])
    return ES256_key


class Auth:
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("JWT_SECRET_KEY")

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.hasher.verify(plain_password, hashed_password)

    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30, seconds=0),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username,
        }
        signing_key = load_ES256_from_jwk_env()
        return jwt.encode(
            payload,
            signing_key,
            algorithm=os.getenv("JWT_ALGORITHM"),
            headers={"kid": os.getenv("ES256_KID")},
        )

    def decode_token(self, token):
        try:
            pub_key = load_ES256_from_jwk_env().public_key()
            decoded = jwt.decode(token, pub_key, algorithms=os.getenv("JWT_ALGORITHM"))
            return decoded
        except jwt.ExpiredSignatureError:
            logging.info("The token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired"
            )
        except jwt.InvalidTokenError:
            logging.info("The token is invalid")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid"
            )

    def encode_refresh_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=10),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": username,
        }

        signing_key = load_ES256_from_jwk_env()
        return jwt.encode(
            payload,
            signing_key,
            algorithm=os.getenv("JWT_ALGORITHM"),
            headers={"kid": os.getenv("ES256_KID")},
        )

    def decode_refresh_token(self, refresh_token):
        try:
            pub_key = load_ES256_from_jwk_env().public_key()
            payload = jwt.decode(
                refresh_token, pub_key, algorithms=os.getenv("JWT_ALGORITHM")
            )

            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                new_token = self.encode_token(username)
                return new_token
            logging.info("Invalid scope for token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except jwt.ExpiredSignatureError:
            logging.info("The token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The refresh token has expired",
            )
        except jwt.InvalidTokenError:
            logging.info("The token is invalid")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The refresh token is invalid",
            )

    def encode_reset_password_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=10),
            "iat": datetime.utcnow(),
            "scope": "reset_password",
            "sub": username,
        }

        signing_key = load_ES256_from_jwk_env()
        # algo.sign(json.dumps(payload).encode("ascii"), signing_key)
        return jwt.encode(
            payload,
            signing_key,
            algorithm=os.getenv("JWT_ALGORITHM"),
            headers={"kid": os.getenv("ES256_KID")},
        )
