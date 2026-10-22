from pydantic import BaseModel, Field, ConfigDict, field_validator
from tools import SIGNALS


class Renewal_Validation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    days_to_expiry:int = Field(ge=-3650, le=3650)

class Signal_Validation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    signal:str

    @field_validator("signal")
    @classmethod
    def validate_signal(cls, v):
        if v not in SIGNALS:
            raise ValueError(f"Invalid signal: {v}")
        return v


class Search_Validation(BaseModel):
    model_config = ConfigDict(extra="forbid",str_strip_whitespace=True)
    query:str = Field(min_length=2,max_length=200)



ARG_M0DELS = {
    "check_online_renewal_eligibility": Renewal_Validation,
    "get_signal_meaning": Signal_Validation,
    "search_handbook": Search_Validation
}
