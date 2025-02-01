# middleware.py
from django.shortcuts import redirect

class AnoLectivoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and 'ano_lectivo_id' not in request.session:
            if request.path not in ['/signin/', '/signout/']:
                return redirect('signin')
        return self.get_response(request)