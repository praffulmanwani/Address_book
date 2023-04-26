from pydantic import BaseModel

class AddressAdd(BaseModel):
    name: str
    latitude: float
    longitude: float


class CalculateDistance(BaseModel):
    distance: int
    latitude: float
    longitude: float



