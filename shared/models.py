from pydantic import BaseModel

class Packet(BaseModel):
    type: str
    content: dict | None = None