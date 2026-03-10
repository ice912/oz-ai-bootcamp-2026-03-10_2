import re
from pydantic import BaseModel, EmailStr, field_validator, Field

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        json_schema_extra={"example": "Password123"}
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password는 8자리 이상이어야 합니다.")
        
        if not re.search(r"[A-Z]", v):
            raise ValueError("비밀번호에는 반드시 대문자가 포함되어야 합니다.")

        if not re.search(r"[0-9]", v):
            raise ValueError("비밀번호에는 반드시 숫자가 포함되어야 합니다.")

        return v

class LogInRequest(BaseModel):
    # email과 password의 시작 지점(공백 4칸)을 똑같이 맞춰야 합니다.
    email: EmailStr
    password: str = Field(..., json_schema_extra={"example": "Password123"})

#전체 사용자 -> 비밀번호 재설정(26년까지)
