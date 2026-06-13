import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Log unhandled exceptions and return a clean JSON error response."""
    response = exception_handler(exc, context)
    if response is None:
        logger.exception("Unhandled API exception in %s", context.get("view", "unknown"))
        return Response(
            {"detail": "An internal server error occurred. Please try again later."},
            status=500,
        )
    return response
