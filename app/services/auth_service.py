from sqlalchemy.orm import Session
from app.models.user import User,RefreshToken
from app.utils.hash_password import verify_password

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def revoke_refresh_token(db, jti: str):
    token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if token:
        token.is_revoked = True
        db.commit()

