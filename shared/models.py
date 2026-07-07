from pydantic import BaseModel

class Packet(BaseModel):
    type: int
    content: dict | None = None