from fastapi import APIRouter, Response, Request, Depends
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token,decode_token
from app.services.auth_service import authenticate_user,revoke_refresh_token
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.db.session import get_db
router = APIRouter()

settings = get_settings()


@router.post("/login")
def login(response: Response, email: str, password: str):
    user = authenticate_user(email, password)

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,    
        samesite="none",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {"message": "login successful"}

 

@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    user_id, jti = verify_refresh_token(db, token)
 
    revoke_refresh_token(db, jti)
 
    new_refresh = create_refresh_token(user_id)
    new_access = create_access_token(user_id)

    response.set_cookie("refresh_token", new_refresh, httponly=True)
    response.set_cookie("access_token", new_access, httponly=True)

    return {"message": "refreshed"}


@router.post("/logout")
def logout(request: Request,response: Response,db: Session = Depends(get_db)):

    token = request.cookies.get("refresh_token")

    payload = decode_token(token, "refresh")
    revoke_refresh_token(db, payload["jti"])

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "logged out"}
