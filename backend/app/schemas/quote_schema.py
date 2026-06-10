from pydantic import BaseModel

class QuoteInput(BaseModel):
    accidents: int
    experience: int
    vehicle_age: int
    annual_miles: int