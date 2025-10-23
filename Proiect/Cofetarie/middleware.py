from .models import Accesare

class Middleware:
    
    request_count=0
    #se va initializa o singură dată, când serverul pornește
    def __init__(self, get_response):
        self.get_response = get_response
        Middleware.request_count = 0
    #constructor

    def __call__(self, request):
        Middleware.request_count += 1
        #incrementam contorul la fiecare accesare, inainte de orice altcv
        request.session_request_count = Middleware.request_count
        
        ip_client=request.META.get('REMOTE_ADDR', '')
        url_text=request.build_absolute_uri()
        #obtinem ip ul si url ul pentru fiecare cerere
        #cream un obiect de tip Accesare și îl salvăm în baza de date
        
        acces= Accesare(ip_client=ip_client, url_text=url_text)
        acces.save()
        # cod de procesare a cererii ....      
        #putem trimite date către funcția de vizualizare; le setăm ca proprietăți în request     
        request.proprietate_noua=17       
        # se apelează (indirect) funcția de vizualizare (din views.py)
        response = self.get_response(request)      

        # putem adauga un header HTTP pentru toate răspunsurile
        response['header_nou'] = 'valoare'
                # aici putem modifica chiar conținutul răspunsului
        # verificăm tipul de conținut folosind headerul HTTP Content-Type
        # motivul fiind că putem transmite și alte resurse (imagini, css etc.), nu doar fișiere html
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            # obținem conținutul
            # (response.content este memorat ca bytes, deci îl transformăm în string)
            content = response.content.decode('utf-8')
            # Modificăm conținutul
            #new_content = content.replace(
            #    '</body>',
            #    '<div>Continut suplimentar</div></body>'
            #)
            # Suprascriem conținutul răspunsului
            #response.content = new_content.encode('utf-8')
            # Actualizăm lungimea conținutului (obligatoriu, fiind header HTTP)
            #response['Content-Length'] = len(response.content)
        return response