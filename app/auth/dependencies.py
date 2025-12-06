from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_token
from app.db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)) -> User:
    decoded = decode_token(token)['sub']
    user = await db.execute(select(User).where(User.id == decoded))
    if not decoded or not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user.scalars().first()
