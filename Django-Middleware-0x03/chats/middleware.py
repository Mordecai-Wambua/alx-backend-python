import logging
from datetime import datetime, timedelta
from django.http import JsonResponse
from collections import defaultdict

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
            return JsonResponse({"detail": "Sorry, API is closed."}, status=403)

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Limits the number of chat messages a user can send within a certain time window, based on their IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)
        self.limit = 5
        self.time_window = 60

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = request.META.get("REMOTE_ADDR")
            now = datetime.now()

            self.request_log[ip] = [
                ts
                for ts in self.request_log[ip]
                if now - ts < timedelta(seconds=self.time_window)
            ]

            if len(self.request_log[ip]) >= self.limit:
                return JsonResponse(
                    {
                        "detail": "Message rate limit exceeded. Only 5 messages per minute allowed."
                    },
                    status=429,
                )

            self.request_log[ip].append(now)

        return self.get_response(request)


class RolepermissionMiddleware:
    """
    Checks the user’s role before allowing access to specific actions
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ["/messages", "/admin"]
        if any(path in request.path for path in protected_paths):
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({"detail": "Authentication required"}, status=401)

            role = getattr(user, "role", None)
            if role not in ["admin", "moderator"]:
                return JsonResponse(
                    {
                        "detail": "Forbidden: You do not have permission to perform this action."
                    },
                    status=403,
                )

        return self.get_response(request)
