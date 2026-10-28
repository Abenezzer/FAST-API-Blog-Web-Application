from pydantic import BaseModel, ConfigDict, Field


class PersonBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    model_config = ConfigDict(from_attributes=True)
    id:int
    date: str
