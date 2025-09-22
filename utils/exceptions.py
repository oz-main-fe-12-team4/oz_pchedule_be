from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return Response(
            {"error": "로그인이 필요합니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    elif isinstance(exc, AuthenticationFailed):
        return Response(
            {"error": "토큰 인증에 실패했습니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
