from pydantic import BaseModel
from datetime import datetime  


class UserResponse(BaseModel):
    id: int
    email: str
    password_hash: str
    created_at: datetime

    class Config:
        # SQLAlchemy 객체를 Pydantic 모델로 변환하기 위해 필수입니다.
        from_attributes = True 
