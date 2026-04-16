"""
Pydantic and SQLAlchemy models for Task 1 & Task 2.
"""

from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

# Database base for SQLAlchemy models
Base = declarative_base()


# ============================================================================
# Task 1: API Key & Rate Limiting - SQLAlchemy Models
# ============================================================================


class APIKeyDB(Base):
    """SQLAlchemy model for API keys."""

    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    key = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    request_count = Column(Integer, default=0, nullable=False)
    last_reset = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)


# ============================================================================
# Task 2: Background Job Processing - SQLAlchemy Models
# ============================================================================


class JobDB(Base):
    """SQLAlchemy model for background jobs."""

    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    task = Column(String, nullable=False)
    status = Column(
        String,
        default="pending",
        nullable=False,
    )  # pending, in_progress, completed
    result = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    completed_at = Column(DateTime, nullable=True)


# ============================================================================
# Task 1: API Key & Rate Limiting - Pydantic Models
# ============================================================================


class APIKeyRequest(BaseModel):
    """Request model for API key generation."""

    pass


class APIKeyResponse(BaseModel):
    """Response model for API key generation."""

    api_key: str = Field(..., description="The generated API key")
    created_at: datetime = Field(..., description="Timestamp of key creation")

    model_config = {"from_attributes": True}


class SecureDataResponse(BaseModel):
    """Response model for secure data endpoint."""

    message: str = Field(..., description="The secure message")
    timestamp: datetime = Field(..., description="Timestamp of the response")

    model_config = {"from_attributes": True}


# ============================================================================
# Task 2: Background Job Processing - Pydantic Models
# ============================================================================


class JobSubmissionRequest(BaseModel):
    """Request model for job submission."""

    task: str = Field(..., min_length=1, description="The task to process")


class JobStatusResponse(BaseModel):
    """Response model for job status."""

    job_id: str = Field(..., description="The unique job ID")
    task: str = Field(..., description="The task description")
    status: Literal["pending", "in_progress", "completed"] = Field(
        ..., description="Current job status"
    )
    result: str | None = Field(None, description="Job result (if completed)")
    created_at: datetime = Field(..., description="Timestamp of job creation")
    completed_at: datetime | None = Field(
        None, description="Timestamp of job completion"
    )

    model_config = {"from_attributes": True}


class JobSubmissionResponse(BaseModel):
    """Response model for job submission."""

    job_id: str = Field(..., description="The unique job ID")
    task: str = Field(..., description="The task description")
    status: str = Field(default="pending", description="Initial job status")

    model_config = {"from_attributes": True}
