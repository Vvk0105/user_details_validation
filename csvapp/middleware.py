import time
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RateLimitMiddleware(MiddlewareMixin):
    RATE_LIMIT = 100
    TIME_WINDOW = 300

    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if not ip:
            return None
        
        key = f"rate_limit{ip}"
        request_times = cache.get(key, [])
        now = time.time()
        
        filtered_times = []
        for t in request_times:
            if now - t < self.TIME_WINDOW:
                filtered_times.append(t)
        request_times = filtered_times

        if len(request_times) >= self.RATE_LIMIT:
            return JsonResponse({"error": "Too Many Requests"}, status=429)
        
        request_times.append(now)
        cache.set(key, request_times, timeout=self.TIME_WINDOW)
        request.remaining_requests = self.RATE_LIMIT - len(request_times)
        return None
    
    def process_response(self, request, response):
        if hasattr(request, "remaining_requests"):
            response["X-RateLimit-Remaining"] = request.remaining_requests
        return response