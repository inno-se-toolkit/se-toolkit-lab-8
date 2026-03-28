# Lab 8 Report

## Task 4A — Multi-step investigation

**Question:** What went wrong?
**Response:** After stopping PostgreSQL, the agent was asked "What went wrong?". It used observability tools to search recent error logs and found a trace indicating a database connection failure. The logs showed repeated `ConnectionRefusedError` from the backend when trying to query the database. The trace confirmed that the failure originated in the database access layer. The backend incorrectly returned a 404 "Items not found" instead of exposing the real connection error. The agent summarized that the root cause was PostgreSQL being down, and the backend was masking the failure.

## Task 4B — Proactive health check

**Scheduled job:** A cron job was created to check for LMS backend errors every 2 minutes. The job was listed successfully.

**Proactive health report:** After triggering another request while PostgreSQL was stopped, the cron job reported: "Detected database connection errors in the last 2 minutes. Trace ID ... shows the failure in the database layer. The backend returned 404 but the real error is a connection refusal. System is unhealthy."

## Task 4C — Bug fix and recovery

**Root cause:** In `backend/app/routers/items.py`, there was a broad exception handler that caught all exceptions and returned a 404 status with "Items not found". This masked the underlying database connection error.

**Fix:** The exception handler was modified to properly log the error and return a 500 status with the actual error message. The relevant code was changed from:
```python
except Exception:
    raise HTTPException(status_code=404, detail="Items not found")
