import os
from django.http import JsonResponse


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path.startswith('/api/'):
            expected = os.getenv("API_KEY")
            if not expected:
                return JsonResponse(
                    {"detail": "Server misconfiguration: API key not set."},
                    status=500
                )

            provided = request.headers.get('X-API-KEY') or request.META.get('HTTP_X_API_KEY')
            if not provided or provided != expected:
                return JsonResponse({"detail": "Invalid or missing API key."}, status=401)

        return self.get_response(request)
