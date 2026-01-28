from fastapi import APIRouter, Response, Request, Depends
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token,decode_token,get_current_user
from app.services.auth_service import authenticate_user,revoke_refresh_token
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import LoginSchema
from app.utils.response import GetResponse

router = APIRouter()

settings = get_settings()


@router.post("/login")
def login(response: Response, payload:LoginSchema= Depends(LoginSchema.as_form),db: Session = Depends(get_db)):
    email = payload.email
    password = payload.password
    user = authenticate_user(db,email, password)
    
    if not user:
        return GetResponse(
        response,
        message="User Not Found",
        status=404)
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id),db)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,   
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,   
    )

    return GetResponse(
        response,
        message="Login successful",
        data={"email": user.email, "name": user.name, "id": user.id},
        status=200
    )

 

@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        return GetResponse(response, message="Refresh token not found", status=400)
    user_id, jti = verify_refresh_token(db, token)
 
    revoke_refresh_token(db, jti)
 
    new_refresh = create_refresh_token(user_id,db)
    new_access = create_access_token(user_id)

    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,   
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,   
    )

    return GetResponse(
        response,
        message="Token Refreshed",
        status=200
    )


@router.post("/logout")
def logout(request: Request,response: Response,user=Depends(get_current_user),db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("refresh_token")

        payload = decode_token(token, "refresh")
        revoke_refresh_token(db, payload["jti"])

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return GetResponse(
            response,
            message="Logout successful",
            status=200
        )
    except Exception as e:
        return GetResponse(
            response,
            error=True,
            message=str(e),
            status=400
        )
