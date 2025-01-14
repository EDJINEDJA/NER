from pydantic import BaseModel
from typing import List, Tuple,Dict

class ResponseModel(BaseModel):
    PER : List[str]
    LOC : List[str]
    ORG : List[str]
    MISC : List[str]
