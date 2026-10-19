from django.http import Http404
from django.template.loader import render_to_string
from django.http import HttpResponse


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip error page rendering for static/media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
        
        try:
            response = self.get_response(request)
            # Check if response is a 404
            if response.status_code == 404:
                try:
                    content = render_to_string('errors/404.html', {})
                    return HttpResponse(content, status=404)
                except:
                    pass  # Fall back to original response
            return response
        except Http404:
            try:
                content = render_to_string('errors/404.html', {})
                return HttpResponse(content, status=404)
            except:
                return HttpResponse("<h1>404 Not Found</h1><p>Page not found.</p>", status=404)
        except Exception as e:
            try:
                content = render_to_string('errors/500.html', {})
                return HttpResponse(content, status=500)
            except:
                return HttpResponse("<h1>500 Server Error</h1><p>An error occurred.</p>", status=500)


