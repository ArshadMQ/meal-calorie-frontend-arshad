"""
BaseService module providing a reusable service class for handling
responses and error logging in application services.

This module defines the BaseService class, which tracks errors,
response messages, and HTTP status codes, and logs errors using
a common logging utility.

Dependencies:
    - typing: For type annotations (List, Union)
    - common_package.config: For the log_error function
"""
from typing import List, Union


class BaseController:
    """
        A base service class that provides common functionality for handling
        responses and error reporting in service classes.

        Attributes:
            errors (List[str]): A list of error messages encountered during processing.
            response (Any): A generic placeholder for the response object or data.
            response_msg (str): A message describing the response or result.
            code_ (Union[str, None]): A general-purpose code, possibly representing response status.
        """
    def __init__(self):
        self.errors: str = ""
        self.response = None
        self.response_msg = ""
        self.code_: Union[str, None] = None

    async def _set_error(self, msg: str, code_: str):
        """Helper method to set error message and HTTP status"""
        self.errors = msg
        self.code_ = code_

    async def _set_response(self, res, message: str, code_: str):
        """Helper method to set response message and HTTP status"""
        self.response_msg = message
        self.code_ = code_
        self.response = res
