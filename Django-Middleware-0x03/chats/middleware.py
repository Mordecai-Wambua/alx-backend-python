import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")

formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"User: {request.user} - Path: {request.path}")

        response = self.get_response(request)

        return response
