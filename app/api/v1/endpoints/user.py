from fastapi import APIRouter  , Depends, status
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import UserSchema
from app.utils.response import GetResponse
from app.models.user import User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from app.utils.hash_password import  hash_password



router = APIRouter()

settings = get_settings()

from fastapi import Response, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@router.post("/create-user")
def create_user(
    response: Response,
    data: UserSchema = Depends(UserSchema.as_form),
    db: Session = Depends(get_db)
):
    try:
        new_user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            name=data.name or ''
        )

        db.add(new_user)
        db.commit()

        response.status_code = status.HTTP_201_CREATED
        return GetResponse(
            message="User Created Successfully",
            data={"email": new_user.email}
        )

    except IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_409_CONFLICT
        return GetResponse(
            error=True,
            message="Email already Registered "
        )

    except ValueError as e:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return GetResponse(
            error=True,
            message=str(e)
        )

    except SQLAlchemyError:
        db.rollback()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return GetResponse(
            error=True,
            message="Database error"
        )

    except Exception:
        db.rollback()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return GetResponse(
            error=True,
            message="Unexpected server error"
        )

