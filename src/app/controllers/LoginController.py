# from fastapi import APIRouter, Depends, Body
# from datetime import datetime, timedelta
# from typing import Optional
# from fastapi.security import OAuth2PasswordBearer

# login = APIRouter(prefix="/api/login", tags=["addition"])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="123")


# @login.get("/")
# async def test(s: str = Depends(oauth2_scheme)):
#     return {"hello": s}

from fastapi import APIRouter, Depends, Body, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
from jose import JWSError, jwt

SECRET_KEY = "ed970259a19edfedf1010199c7002d183bd15bcaec612481b29bac1cb83d8137"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user_id(user_name: str, password: str):
    return 123


def create_jwt_token(data: dict, expire_delta: Optional[timedelta] = None):
    # token有效時間
    expire = (
        datetime.utcnow() + expire_delta
        if expire_delta
        else datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # exp是規範寫法
    data.update({"exp": expire})
    # jwt加密
    token = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)

    return token


login = APIRouter(prefix="/api/login", tags=["addition"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="123")


@login.post("/")
# 不同從API取值的方式 postman form-data or x-xxx-form-urlencoded
# async def get_token(user_name: str = Form(...), password: str = Form(...)):
#     user_id = get_user_id(user_name, password)
#     data = {"user_id": user_id}
#     token = create_jwt_token(data)
#     return {"token": token}


async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 驗證登入資訊
    user_id = get_user_id(form_data.username, form_data.password)
    data = {"user_id": user_id}
    token = create_jwt_token(data)
    return {"token": token}


@login.get("/")
async def verify_token(token: str = Depends(oauth2_scheme)):
    # 定義一個異常返回
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="verify fail",
        # OAuth2規範 要加入下列key value
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 驗證token
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        print(f"paload: {payload}")
        user_id = payload.get("user_id")
        print(f"user_id: {user_id}")
        if not user_id:
            raise credentials_exception
    except JWSError as e:
        print(f"verify error: {e}")
        raise credentials_exception
    return {"hello": user_id}
