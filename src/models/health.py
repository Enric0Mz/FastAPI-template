from pydantic import BaseModel

class HealthChekModel(BaseModel):
    opened_conns: int
    max_conns: int
    server_version: str

class HealthCheckResponseModel(BaseModel):
    api_status: str
    details: HealthChekModel
