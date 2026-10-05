"""Shared response schemas."""
from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    env: str


class ModuleStatus(BaseModel):
    module: str
    ready: bool
    message: str
