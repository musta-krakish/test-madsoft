from pydantic import BaseModel

class MemeBase(BaseModel):
    title: str
    description: str 

class MemeCreate(MemeBase):
    image_url: str

class MemeUpdate(MemeBase):
    image_url: str 

class Meme(MemeBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True
