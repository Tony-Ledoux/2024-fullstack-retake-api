from pydantic import BaseModel


class Question(BaseModel):
    name: str
    email: str
    subject: str
    message: str
