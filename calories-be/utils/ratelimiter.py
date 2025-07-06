from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.schema import RateLimit

MAX_REQUESTS = 15
WINDOW_MINUTES = 1

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = datetime.utcnow()

        db: Session = SessionLocal()
        try:
            rate_limit = db.query(RateLimit).filter(RateLimit.ip_address == ip).first()

            if rate_limit:
                time_diff = now - rate_limit.last_request

                if time_diff > timedelta(minutes=WINDOW_MINUTES):
                    # Reset counter
                    rate_limit.request_count = 1
                    rate_limit.last_request = now
                else:
                    if rate_limit.request_count >= MAX_REQUESTS:
                        db.close()
                        return JSONResponse(
                            status_code=429,
                            content={
                                "api_version": 1,
                                "response": {"code": 429, "msg": "Too Many Requests – Rate limit exceeded"},
                                "data": {},
                            }
                        )
                    rate_limit.request_count += 1
                    rate_limit.last_request = now

                db.add(rate_limit)
            else:
                new_limit = RateLimit(
                    ip_address=ip,
                    request_count=1,
                    last_request=now
                )
                db.add(new_limit)

            db.commit()
        finally:
            db.close()

        response = await call_next(request)
        return response