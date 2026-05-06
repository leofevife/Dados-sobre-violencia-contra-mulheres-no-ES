from pydantic import BaseModel, Field

class SqlQuery(BaseModel):
    statement: str = Field(..., description="SQL statement to execute on Cloudflare D1")

class ReceivedData(BaseModel):
    data: dict = Field(..., description="Payload data sent from the source")
