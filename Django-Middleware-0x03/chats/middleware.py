import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden, JsonResponse
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = time(21, 0)
        end_time = time(18, 0)

        # If current time is after 9PM or before 6PM=> restrict access
        if now >= start_time and now < end_time:
            return HttpResponseForbidden("Access to messaging app is restricted during this time.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)

    def __call__(self, request):
        ip = self.get_ip_address(request)
        now = datetime.now()

        # Apply only on POST requests to message endpoint
        if request.method == "POST" and "/messages" in request.path:
            timestamps = self.message_log[ip]

            # Filter out timestamps older than 1 minute
            self.message_log[ip] = [
                ts for ts in timestamps if now - ts < timedelta(minutes=1)
            ]

            if len(self.message_log[ip]) >= 5:
                return JsonResponse({
                    "detail": "Rate limit exceeded: Maximum 5 messages per minute allowed."
                }, status=429)

            # Record this message
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_ip_address(self, request):
        """Handles proxy headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            "/admin/",
        ]

        if any(request.path.startswith(path) for path in protected_paths):
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"detail": "Authentication required."}, status=401)

            # Check if role is not admin
            if getattr(user, "role", None) not in ["admin", "moderator"]:
                return JsonResponse({
                    "detail": "Permission denied. Only admins or moderators can access this route."
                }, status=403)

        return self.get_response(request)
