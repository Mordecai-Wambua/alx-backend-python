import logging
from datetime import datetime
from django.http import JsonResponse

logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")

formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Logs each user’s requests to a file, including the timestamp, user and the request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        logger.info(f"User: {request.user} - Path: {request.path}")
        return response


class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the messaging up during certain hours of the day.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        if not (18 <= current_hour <= 21):
            return JsonResponse({"message": "Sorry, API is closed."}, status=403)

        return self.get_response(request)
