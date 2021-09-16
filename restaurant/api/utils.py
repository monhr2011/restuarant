import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_framework_exception_handler

logger = logging.getLogger('django.request')


def exception_handler(exc, context):
    response = rest_framework_exception_handler(exc, context)
    if response:
        return Response({"error": response.data}, status=response.status_code)
    else:
        if isinstance(exc, ValueError):
            return Response({"error": {"message": exc.__str__()}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if settings.DEBUG:
                return Response({'error': {"message": exc.__str__()}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                logger.exception(exc)
                return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)