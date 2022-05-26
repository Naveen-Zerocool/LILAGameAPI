import logging
import traceback

from rest_framework import status
from rest_framework.renderers import JSONRenderer

from LILAGameAPI.standard_responses import StandardResponse


logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        try:
            message = "Exception - URL: {url}\n\nMethod: {request_method}\n\nError: {error}\n\nTraceback: {tb}".format(
                url=request.build_absolute_uri(),
                request_method=request.method,
                error=repr(exception),
                tb=traceback.format_exc()
            )
            logger.exception(msg=message)
            response = StandardResponse(response_data={}, error={}, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message="Something went wrong at our side, Please check after sometime")
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response
        except Exception:
            pass
        return None
