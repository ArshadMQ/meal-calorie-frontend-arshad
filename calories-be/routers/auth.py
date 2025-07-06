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
from controller.signin.controller import SignInController
from controller.signup.controller import SignUpController
from controller.users.controller import UserMeController
from database.connection import db_session_connection
from database.schema import User
from domain.signin.dao import SignInResponseDAO, SignInRequestDAO, UserInfoDAO
from domain.signup.dao import SignUpRequestDAO
from utils.common import success_response, failure_response, current_user
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=SignInResponseDAO)
async def sign_in_router(
        params: SignInRequestDAO, db_session: Session = Depends(db_session_connection)
):
    """
       Authenticates a user and returns an access token if the credentials are valid.

       This function uses the SignInAppService to validate the provided credentials
       and generate a response, typically including authentication tokens or session info.

       Parameters:
       ----------
       params : SignInDAO
           Data Access Object containing user login credentials (e.g., username and password).
       db_session : Session, optional
           Database session injected via dependency for user lookup and credential validation.

       Returns:
       -------
       JSONResponse
           A JSON response with HTTP 200 and token data on success, or an error response
           with appropriate status code and details on failure.
       """
    svc = SignInController(params=params, db_session=db_session)
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


@router.post("/register")
async def signup_in_router(params: SignUpRequestDAO,
                           db_session: Session = Depends(db_session_connection)):
    """
    ### Authorized Role:
        Client Admin and Root: Client admin and Root User can create client users.
    ### Request Body:
        ClientUsersAPIParamsDAO: Parameters required to create a new user.
    ### Response:
        200 OK: Success, returns the user verification details.
        Error Response: Returns error code and error messages if the operation fails.
    """
    svc = SignUpController(params=params, db_session=db_session)
    svc_response = await svc()
    if await svc_response.success:
        return JSONResponse(
            status_code=svc_response.code_,
            content=success_response(
                payload=jsonable_encoder(svc_response.response),
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


@router.get("/me", response_model=UserInfoDAO)
async def sign_in_router(user: User = Depends(current_user),
                         db_session: Session = Depends(db_session_connection)
                         ):
    svc = UserMeController(user=user, db_session=db_session)
    svc_response = await svc()
    if await svc_response.success:
        return JSONResponse(
            status_code=svc_response.code_,
            content=success_response(
                payload=jsonable_encoder(svc_response.response),
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
