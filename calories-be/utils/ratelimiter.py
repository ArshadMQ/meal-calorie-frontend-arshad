from datetime import datetime, timedelta
<<<<<<< HEAD
from fastapi import Request, HTTPException
=======
from fastapi import Request
from fastapi.responses import JSONResponse
>>>>>>> 81f30e93aa55c0c603e83f968eab34f3b8ad08e9
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.schema import RateLimit

<<<<<<< HEAD
MAX_REQUESTS = 15
WINDOW_MINUTES = 1

class RateLimitMiddleware(BaseHTTPMiddleware):
    def dispatch(self, request: Request, call_next):
=======
MAX_REQUESTS = 100
WINDOW_MINUTES = 1

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
>>>>>>> 81f30e93aa55c0c603e83f968eab34f3b8ad08e9
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
<<<<<<< HEAD
                        return {}
=======
                        return JSONResponse(
                            status_code=429,
                            content={
                                "api_version": 1,
                                "response": {"code": 429, "msg": "Too Many Requests – Rate limit exceeded"},
                                "data": {},
                            }
                        )
>>>>>>> 81f30e93aa55c0c603e83f968eab34f3b8ad08e9
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

<<<<<<< HEAD
        response = call_next(request)
=======
        # Ensure you await this!
        response = await call_next(request)
>>>>>>> 81f30e93aa55c0c603e83f968eab34f3b8ad08e9
        return response