from django.db import models
from datetime import datetime
from urllib.parse import urlparse, parse_qsl

id_count=0
class Accesare(models.Model):
    
    ip_client = models.CharField(max_length=50)
    url_text = models.CharField(max_length=2048)
    data_accesare = models.DateTimeField(auto_now_add=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


    # def __init__(self, ip_client, url_text , data_accesare):
    #     self.ip_client = ip_client
    #     Accesare.id_count+=1
    #     self.url_text = url_text
    #     self.data_accesare = datetime.now()

        
    def lista_parametri(self):
        parsed=urlparse(self.url_text)
        if not parsed.query:
            return []
        pairs= parse_qsl(parsed.query, keep_blank_values=True)
        return [(k, None if v=="" else v) for k, v in pairs]

    def url(self):
        return self.url_text

    def data(self, format_str=None):
        if format_str:
            return self.data_accesare.strftime(format_str)
        else:
            return self.data_accesare
        
    def pagina(self):
        parsed=urlparse(self.url_text)
        path= parsed.path if parsed.path else "/"
        return path
    
class Organizator(models.Model):
    nume = models.CharField(max_length=100)
    email = models.EmailField()
def __str__(self):
    return self.nume


class Locatie(models.Model):
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    cod_postal = models.CharField(max_length=10)  
    # nr=models.CharField(max_length=10, default="bcd")
    

def __str__(self):
    return f"{self.adresa}, {self.oras}"

# ----------------------------------------entitatile pentru Cofetarie----------------------------------------

