from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key=True, index=True)
    gene_symbol = Column(String(20), unique=True, index=True, nullable=False)
    gene_name = Column(String(255), nullable=False)
    organism = Column(String(100), nullable=False)
    chromosome = Column(String(10), nullable=True)
    description = Column(Text, nullable=True)