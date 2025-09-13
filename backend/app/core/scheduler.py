"""
Scheduled tasks for the application.
"""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import async_session_factory
from app.services.nnnnotification_service import NnnnotificationService

logger = logging.getLogger(__name__)

class Scheduler:
    """Scheduler for background tasks."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance._scheduler = AsyncIOScheduler()
            cls._instance._started = False
        return cls._instance
    
    async def start(self) -> None:
        """Start the scheduler."""
        if not self._started:
            await self._setup_jobs()
            self._scheduler.start()
            self._started = True
            logger.info("Scheduler started")
    
    def shutdown(self) -> None:
        """Shutdown the scheduler."""
        if self._started:
            self._scheduler.shutdown()
            self._started = False
            logger.info("Scheduler stopped")
    
    async def _setup_jobs(self) -> None:
        """Set up scheduled jobs."""
        # Check for expiring passwords daily at 9 AM
        self._scheduler.add_job(
            self._check_password_expirations,
            CronTrigger(hour=9, minute=0, timezone="UTC"),
            id="check_password_expirations",
            name="Check for expiring passwords and send notifications",
            replace_existing=True
        )
        
        # Clean up expired tokens daily at midnight
        self._scheduler.add_job(
            self._cleanup_expired_tokens,
            CronTrigger(hour=0, minute=0, timezone="UTC"),
            id="cleanup_expired_tokens",
            name="Clean up expired tokens",
            replace_existing=True
        )
        
        # Log scheduler status
        self._scheduler.add_listener(
            self._scheduler_event_listener,
            mask=(
                'EVENT_JOB_ADDED | '
                'EVENT_JOB_REMOVED | '
                'EVENT_JOB_MODIFIED | '
                'EVENT_JOB_EXECUTED | '
                'EVENT_JOB_ERROR | '
                'EVENT_JOB_MISSED'
            )
        )
    
    async def _check_password_expirations(self) -> None:
        """Check for users with expiring passwords and send notifications."""
        logger.info("Checking for expiring passwords...")
        async with async_session_factory() as session:
            try:
                await NnnnotificationService.check_and_notify_password_expiration(db=session)
                logger.info("Password expiration check completed")
            except Exception as e:
                logger.error(f"Error checking password expirations: {e}")
                # Re-raise to allow the scheduler to handle the error
                raise
    
    def _cleanup_expired_tokens(self) -> None:
        """Clean up expired tokens from the database."""
        logger.info("Cleaning up expired tokens...")
        # TODO: Implement token cleanup if using a token blacklist
        # This is a placeholder for future implementation
        logger.info("Token cleanup completed")
    
    def _scheduler_event_listener(self, event) -> None:
        """Log scheduler events."""
        if hasattr(event, 'exception') and event.exception:
            logger.error(
                f"Job {event.job_id} raised an exception: {event.exception}"
            )
            logger.error(event.traceback)
        elif hasattr(event, 'code') and event.code == 'EVENT_JOB_EXECUTED':
            logger.debug(f"Job {event.job_id} executed successfully")
        elif hasattr(event, 'code') and event.code == 'EVENT_JOB_ERROR':
            logger.error(f"Job {event.job_id} encountered an error")
            if hasattr(event, 'exception'):
                logger.error(str(event.exception))

async def init_scheduler() -> Scheduler:
    """Initialize and return the scheduler."""
    scheduler = Scheduler()
    await scheduler.start()
    return scheduler
