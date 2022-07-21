from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Union

import datetime
import uvicorn
import requests
import os

# local modules
import utils
import schema


app = FastAPI()

fastforex_api_key = os.getenv("FAST_FOREX_API_KEY")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

users_db = {}

# Credit fastapi documentation https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# The code from start is gotten form the Fast API docs and modified to perform the authentic task
# START
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schema.UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: Union[datetime.timedelta, None] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schema.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Create `JWT` for the user
@app.post("/gettoken", response_model=schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# STOP
# ======================================================

# Creates a new user account
@app.post("/createaccount", response_model=schema.User)
async def createaccount(
    username: str = Form(...),
    password: str = Form(...),
):
    users_db[f"{username}"] = {
        "username": f"{username}",
        "hashed_password": get_password_hash(password),
        "disabled": False,
    }
    return {"username": username, "disabled": "false"}


# list out all the supported currencies
@app.get("/v1/currency/all")
async def all_currencies(current_user: schema.User = Depends(get_current_active_user)):
    try:
        if current_user.disabled == False:
            url = f"https://api.fastforex.io/fetch-all?api_key={fastforex_api_key}"
            res = requests.request("POST", url)
            if res.status_code == status.HTTP_200_OK:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"currencies": list(res.json()["results"].keys())},
                )
            else:
                return JSONResponse(
                    status_code=res.status_code,
                    content={"error": "Authorization token invalid"},
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=res.json(),
            )
    except:
        # log the err in at text file
        utils.logs("/v1/currency/all")
        return JSONResponse(
            status_code=500,
            content="An error occured",
        )


# Perform currency convertion from on base currency to a given target currency
@app.get("/v1/convert")
async def convert_currency(
    base_currency: schema.Currency,
    target_currency: schema.Currency,
    amount: float,
    date: Union[str, None] = None,
    current_user: schema.User = Depends(get_current_active_user),
):
    try:
        base_currency = base_currency.upper()
        target_currency = target_currency.upper()
        if current_user.disabled == False:
            if date == None:
                url = f"https://api.fastforex.io/convert?from={base_currency}&to={target_currency}&amount=1000&api_key={fastforex_api_key}"
                res = requests.request("POST", url)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        f"{target_currency}": res.json()["result"][
                            f"{target_currency}"
                        ],
                    },
                )
            else:
                try:
                    _ = datetime.datetime.strptime(date, "%Y-%m-%d")
                except:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "message": f"The date {date} should be formated as yyyy-mm-dd"
                        },
                    )
                url = f"https://api.fastforex.io/historical?date={date}&from={base_currency}&to={target_currency}&api_key={fastforex_api_key}"
                res = requests.request("POST", url)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        f"{target_currency}": res.json()["results"][
                            f"{target_currency}"
                        ]
                        * amount,
                    },
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=res.json(),
            )
    except:
        # log the err in at text file
        utils.logs(
            f"/v1/convert?base_currency={base_currency}&target_currency={target_currency}&date={date}"
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="An error occured",
        )


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
