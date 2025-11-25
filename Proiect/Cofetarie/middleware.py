from .models import Accesare
# proceseaza cererile si raspunsurile
class Middleware:
    
    request_count=0
    def __init__(self, get_response):
        self.get_response = get_response
        Middleware.request_count = 0
        #constructor

    def __call__(self, request):
        Middleware.request_count += 1
        request.session_request_count = Middleware.request_count
        
        ip_client=request.META.get('REMOTE_ADDR', '')
        url_text=request.build_absolute_uri()
        
        acces= Accesare(ip_client=ip_client, url_text=url_text)
        acces.save() 
        request.proprietate_noua=17       
        response = self.get_response(request)      

        response['header_nou'] = 'valoare'

        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            content = response.content.decode('utf-8')

        return response