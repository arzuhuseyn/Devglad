from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class SayHiMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Hi, I'm middleware")

    def process_response(self, request, response):
        q = request.GET.get('midq')
        return HttpResponse('Response stopped') if q else response