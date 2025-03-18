class QRAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add `qr_access` to session if present in the GET parameter
        if request.GET.get('qr_access') == '1':
            request.session['qr_access'] = '1'
        
        response = self.get_response(request)
        return response
