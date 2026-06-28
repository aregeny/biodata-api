from pydantic import BaseModel, ConfigDict
from typing import Optional

class GeneBase(BaseModel):
    gene_symbol: str
    gene_name: str
    organism: str
    chromosome: Optional[str] = None
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
    model_config = ConfigDict(from_attributes=True)