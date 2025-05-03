from django.utils import timezone
from .models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track home page visits
        if request.path == '/' and not request.path.startswith('/admin/'):
            ip_address = request.META.get('REMOTE_ADDR')
            
            # Check if this IP has visited before
            has_visited = Visitor.objects.filter(ip_address=ip_address).exists()
            
            # Only create record if it's a new visitor
            if not has_visited:
                Visitor.objects.create(
                    ip_address=ip_address,
                    page_visited=request.path,
                    user_agent=request.META.get('HTTP_USER_AGENT'),
                    unique_visitor=True
                )
        
        response = self.get_response(request)
        return response 