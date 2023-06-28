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
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWSError, jwt

from database.database import engine, Base, get_db
from repositories.UserRepository import UserRepository
from schemas.UserSchema import UserRequest, UserResponse
from models.User import User

SECRET_KEY = "ed970259a19edfedf1010199c7002d183bd15bcaec612481b29bac1cb83d8137"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user_id(user_name: str, password: str, user: list):
    for u in user:
        if UserResponse.from_orm(u).name == user_name:
            if UserResponse.from_orm(u).password == password:
                return UserResponse.from_orm(u).id
    return 0


def update_user_token(id: int, token: str, db: Session):
    if not UserRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    try:
        UserRepository.save(db, User(id=id, token=token))
        return True
    except:
        return False


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


login = APIRouter(prefix="/api", tags=["addition"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="123")


@login.post("/login")
# 不同從API輸入取值的方式 postman form-data or x-xxx-form-urlencoded
# async def get_token(user_name: str = Form(...), password: str = Form(...)):
#     user_id = get_user_id(user_name, password)
#     data = {"user_id": user_id}
#     token = create_jwt_token(data)
#     return {"token": token}


def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # 驗證登入資訊

    user = UserRepository.find_all(db)
    user_id = get_user_id(form_data.username, form_data.password, user)
    if not user_id:
        return "incorrect username or password"
    else:
        data = {"user_id": user_id, "username": form_data.username}
        token = create_jwt_token(data)
        if update_user_token(user_id, token, db):
            return {"token": token}
        else:
            return "update token fail"


@login.get("/login")
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
