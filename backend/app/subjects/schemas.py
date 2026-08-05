from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str
    description: str


class SubjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class SubjectResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True