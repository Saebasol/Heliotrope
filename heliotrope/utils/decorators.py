from functools import wraps
from inspect import getfullargspec
from typing import Literal, get_args

from heliotrope.utils.response import forbidden
from heliotrope.utils.typed import HeliotropeRequest


def hiyobot_only(f):
    @wraps(f)
    async def decorator_function(self, request: HeliotropeRequest, *args, **kwargs):
        if hiyobot_secret := request.headers.get("hiyobot"):
            if request.app.config.HIYOBOT_SECRET == hiyobot_secret:
                response = await f(self, request, *args, **kwargs)
                return response

        return forbidden

    return decorator_function


# def authorized(f):
#     @wraps(f)
#     async def decorated_function(request, *args, **kwargs):

#         is_authorized = True

#         if is_authorized:
#             response = await f(request, *args, **kwargs)
#             return response
#         return json({"status": 403, "message": "not_authorized"}, 403)

#     return decorated_function


def strict_literal(argument_name: str):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # First get about func args
            full_arg_spec = getfullargspec(f)
            # Get annotation
            arg_annoration = full_arg_spec.annotations[argument_name]
            # Check annotation is Lireral
            if arg_annoration.__origin__ is Literal:
                # Literal -> Tuple
                literal_list = get_args(arg_annoration)
                # Get index
                arg_index = full_arg_spec.args.index(argument_name)
                # Handle arguments
                if arg_index < len(args) and args[arg_index] not in literal_list:
                    raise ValueError(
                        f"Arguments do not match. Expected: {literal_list}"
                    )
                # Handle keyword arguments
                elif recive_arg := kwargs.get(argument_name):
                    if recive_arg not in literal_list:
                        raise ValueError(
                            f"Arguments do not match. Expected: {literal_list}"
                        )

            return await f(*args, **kwargs)

        return decorated_function

    return decorator
