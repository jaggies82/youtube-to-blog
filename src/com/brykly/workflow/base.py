"""Base workflow module with status tracking capabilities."""

import asyncio
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional

class WorkflowStatus(Enum):
    """Enumeration of possible workflow statuses."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowStep:
    """Class to represent a workflow step with status tracking."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = WorkflowStatus.PENDING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[Exception] = None
    
    def start(self) -> None:
        """Start the step execution."""
        self.status = WorkflowStatus.RUNNING
        self.start_time = datetime.now()
    
    def complete(self, result: Optional[Dict[str, Any]] = None) -> None:
        """Complete the step execution successfully."""
        self.status = WorkflowStatus.COMPLETED
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.result = result
    
    def fail(self, error: Exception) -> None:
        """Mark the step as failed."""
        self.status = WorkflowStatus.FAILED
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.error = error
    
    def cancel(self) -> None:
        """Cancel the step execution."""
        self.status = WorkflowStatus.CANCELLED
        if self.start_time:
            self.end_time = datetime.now()
            self.duration = (self.end_time - self.start_time).total_seconds()

class BaseWorkflow:
    """Base class for all workflows with status tracking."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        self.config_path = config_path
        self.steps: List[WorkflowStep] = []
        self.status = WorkflowStatus.PENDING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
        self.error: Optional[Exception] = None
    
    def add_step(self, name: str, description: str) -> WorkflowStep:
        """Add a new step to the workflow."""
        step = WorkflowStep(name, description)
        self.steps.append(step)
        return step
    
    async def start(self) -> None:
        """Start the workflow execution."""
        self.status = WorkflowStatus.RUNNING
        self.start_time = datetime.now()
    
    async def complete(self) -> None:
        """Complete the workflow execution successfully."""
        self.status = WorkflowStatus.COMPLETED
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
    
    async def fail(self, error: Exception) -> None:
        """Mark the workflow as failed."""
        self.status = WorkflowStatus.FAILED
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.error = error
    
    async def cancel(self) -> None:
        """Cancel the workflow execution."""
        self.status = WorkflowStatus.CANCELLED
        if self.start_time:
            self.end_time = datetime.now()
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate a status report for the workflow."""
        return {
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'error': str(self.error) if self.error else None,
            'steps': [
                {
                    'name': step.name,
                    'description': step.description,
                    'status': step.status.value,
                    'duration': step.duration,
                    'error': str(step.error) if step.error else None
                }
                for step in self.steps
            ]
        } 