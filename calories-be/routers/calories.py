"""
This module sets up the API routes for user sign-in and token refresh functionality.

It includes:
- User authentication via credentials (sign-in)
- Token refresh for renewing access tokens
- Dependency injection for logging, database access, and request handling
- Integration with business logic services for authentication and token management

Router:
- Prefix: /auth
- Tag: "SignIn"
"""
from controller.calories.get.controller import ListCaloriesController
from controller.calories.post.controller import FetchCaloriesController
from database.connection import db_session_connection
from domain.calories.dao import CalorieResponse, CalorieRequest
from utils.common import success_response, failure_response, current_user
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.schema import User
from typing import List

router = APIRouter(tags=["Calories Calculator"])


@router.post("/get-calories", response_model=CalorieResponse)
async def get_calories(
        params: CalorieRequest,
        user: User = Depends(current_user),
        db_session: Session = Depends(db_session_connection)
):
    svc = FetchCaloriesController(params=params, login_user=user, db_session=db_session)
    svc_response = await svc()
    if await svc_response.success:
        return JSONResponse(
            status_code=svc_response.code_,
            content=success_response(
                payload=svc_response.response,
                code=svc_response.code_,
                msg=svc_response.response_msg,
            ),
        )
    return JSONResponse(
        status_code=svc_response.code_,
        content=failure_response(
            code_=svc_response.code_,
            message=svc_response.errors,
            payload={}
        ),
    )


@router.get("/list-calories", response_model=List[CalorieResponse])
async def list_dishes(
        user: User = Depends(current_user),
        db_session: Session = Depends(db_session_connection)
):
    svc = ListCaloriesController(login_user=user, db_session=db_session)
    svc_response = await svc()
    if await svc_response.success:
        return JSONResponse(
            status_code=svc_response.code_,
            content=success_response(
                payload=svc_response.response,
                code=svc_response.code_,
                msg=svc_response.response_msg,
            ),
        )
    return JSONResponse(
        status_code=svc_response.code_,
        content=failure_response(
            code_=svc_response.code_,
            message=svc_response.errors,
            payload={}
        ),
    )
