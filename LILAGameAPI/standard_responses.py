from rest_framework import status
from rest_framework.response import Response


class StandardResponse(Response):

    def __init__(self, response_data, message=None, http_status=None, success=True, error=None):
        if not http_status:
            http_status = status.HTTP_200_OK
        else:
            success = False
        response = {"success": success, "message": message,
                    "data": response_data, "error": error}
        super(StandardResponse, self).__init__(response, status=http_status)
