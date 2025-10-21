from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class RiskCategory(PyEnum):
    CYBERSECURITY = "cybersecurity"
    NETWORK = "network"
    COMPLIANCE = "compliance"
    INFRASTRUCTURE = "infrastructure"
    HUMAN = "human"

class Probability(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Impact(PyEnum):
    MINOR = "minor"
    SIGNIFICANT = "significant"
    CRITICAL = "critical"

class Risk(Base):
    __tablename__ = "risks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(RiskCategory), nullable=False, index=True)
    probability = Column(Enum(Probability), nullable=False)
    impact = Column(Enum(Impact), nullable=False)
    score = Column(Float, nullable=False, default=0.0)  # Calculated automatically
    potential_loss_usd = Column(Float, nullable=True)  # Estimated loss in USD
    mitigation_measures = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False, index=True)
    delegate_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    history = Column(JSON, nullable=True)  # Revision History
    owner = relationship("Owner", foreign_keys=[owner_id])
    delegate = relationship("Owner", foreign_keys=[delegate_id])

class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)  # Ex: Admin, Auditor, RiskOwner
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    risk_id = Column(Integer, ForeignKey("risks.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("owners.id"), nullable=True, index=True)
    action = Column(String, nullable=False)  # Ex: CREATE, UPDATE, DELETE
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class BusinessImpactFactor(Base):
    __tablename__ = "business_impact_factors"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(RiskCategory), unique=True, nullable=False)
    cost_per_hour_usd = Column(Float, nullable=False)  
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())