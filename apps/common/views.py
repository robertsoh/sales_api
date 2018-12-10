from rest_framework import status
from rest_framework.response import Response


def server_error(request, *args, **kwargs):
    """
    Generic 500 error handler.
    """
    data = {
        'error': 'Server Error (500)'
    }
    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
