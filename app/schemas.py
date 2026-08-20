from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class GeneBase(BaseModel):
    gene_symbol: str = Field(..., max_length = 20,description="The unique symbol for the gene")
    gene_name: str = Field(..., max_length = 255,description="The name of the gene")
    organism: str = Field(..., max_length = 100,description="The organism of the gene")
    chromosome: Optional[str] = Field(None, max_length = 10,description="The chromosome of the gene")
    description: Optional[str] = None

class GeneCreate(GeneBase):
    pass

class GeneUpdate(BaseModel):
    gene_symbol: Optional[str] = None
    gene_name: Optional[str] = None
    organism: Optional[str] = None
    chromosome: Optional[str] = None
    description: Optional[str] = None

class GeneResponse(GeneBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)