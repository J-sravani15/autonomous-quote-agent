from pydantic import BaseModel

class QuoteInput(BaseModel):

    Driver_Age: int
    Driving_Exp: int
    Prev_Accidents: int
    Prev_Citations: int
    Coverage: int
    Veh_Usage: int
    Annual_Miles_Range: int
    Vehicl_Cost_Range: int
    Sal_Range: int
    Quoted_Premium: float