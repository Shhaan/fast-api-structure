from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Request, status
from app.core.config import get_settings
import uuid
from app.models.user import RefreshToken
from fastapi import   Request, Depends   
from sqlalchemy.orm import Session
from app.db.session import get_db 
from app.models.user import User
settings = get_settings()


def create_token(subject: str, expires_delta: timedelta, token_type: str):
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: str):
    return create_token(
        subject=user_id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )



def create_refresh_token(user_id: int, db: Session) -> str:
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "exp": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    db_token = RefreshToken(
        jti=jti,
        user_id=user_id,
        is_revoked=False
    )

    db.add(db_token)
    db.commit()

    return token



def decode_token(token: str, token_type: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def verify_refresh_token(db, token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    jti = payload.get("jti")

    db_token = db.query(RefreshToken).filter(
        RefreshToken.jti == jti,
        RefreshToken.is_revoked == False
    ).first()

    if not db_token:
        raise HTTPException(status_code=401 , detail="Invalid or expired token")

    return payload["sub"], jti



def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = decode_token(token, token_type="access")
   
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user