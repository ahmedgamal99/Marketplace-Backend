from pydantic import BaseModel, validator, EmailStr


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class LoginUser(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    email: str
    name: str
