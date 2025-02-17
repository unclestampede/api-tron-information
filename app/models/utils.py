from humps import camelize
from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True, from_attributes=True)
