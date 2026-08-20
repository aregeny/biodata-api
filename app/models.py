from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from app.database import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key=True, index=True)
    gene_symbol = Column(String(20), index=True, nullable=False) #unique=True removed
    gene_name = Column(String(255), nullable=False)
    organism = Column(String(100), nullable=False)
    chromosome = Column(String(10), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('gene_symbol', 'organism', name='uq_gene_symbol_organism'),
        )