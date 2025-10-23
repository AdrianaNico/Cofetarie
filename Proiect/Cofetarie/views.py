from django.shortcuts import render
from .models import Accesare
from .models import Locatie
from django.db.models import Count
from django.http import HttpResponse
from datetime import datetime


def index(request):
	return HttpResponse(f"""
        <html>
        <p><b>Pe site-ul proiectului meu, utilizatorul va putea vizualiza si comanda diferite tipuri de prajituri si de torturi. Prajiturile si torturile vor fi de cateva tipuri prestabilite, insa torturile se pot si personaliza dupa preferinte, astfel: se poate alege din mai multe tipuri de blat, mai multe creme, diferite ornamente si mesaje scrise pe tort.
        </b></p>
        <p>{request.GET.get("mesaj")}</p>
        </html>
        """)
#http://127.0.0.1:8000/Cofetarie?mesaj=Bun venit!&a=1&a=20&a=30

def info(request):
	return HttpResponse(f"""
        <html>
        <h1>Informatii despre server</h1>
        <p>{request.GET.get("data")}</p>
        <p>{int(request.GET.getlist("a")[-1])}</p>
        </html>
        """)
#http://127.0.0.1:8000/Cofetarie/info?data=Salut&a=1&a=20&a=30

def cum_il_cheama(request):
    lista_nume= request.GET.getlist('nume')
    lista_nume= ("si "+" si ".join(lista_nume)) if lista_nume else "anonim"
    return HttpResponse(f"Pe coleg îl cheama {lista_nume}")
#http://localhost:8000/aplicatie_exemplu/cum_il_cheama_pe_coleg/?nume=ionel&nume=gigel&nume=costel


def afis_data(request):
    d=request.GET.get("param")
    
    zile_saptamana = ["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"]
    luni = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie","Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
    now=datetime.now()
    zi_sapt=zile_saptamana[now.weekday()]
    zi=now.day
    luna=luni[now.month-1]
    an=now.year
    ora=now.strftime("%H:%M:%S")
    
    if d =="data":
        afis=f"{zi_sapt}, {zi}, {luna}, {an}"
    elif d =="zi":
        afis=f"{zi}, {luna}, {an}"
    elif d =="timp":
        afis=f"{ora}"
        
    return HttpResponse(f"""
                        <h1>Data si ora</h1>
                        <p>{afis}</p>
                        """)
    
#http://127.0.0.1:8000/Cofetarie/data?param=zi sau timp sau data

def afis_template(request):
    return render(request,"Cofetarie/exemplu.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )


def log_view(request):
    
    ultimele= request.GET.get("ultimele", None)
    accesari_param = request.GET.get("accesari", None)
    iduri_brute = request.GET.getlist("iduri") # getlist pentru parametri multipli
    dubluri = request.GET.get("dubluri", "false").lower() == "true"
    tabel_param = request.GET.get("tabel", None)
    
    context={}
    #pregatim dictionarul pt template
    mesaj_eroare=None
    accesari = []
    numar_accesari_sesiune = None
    
    text_final = "<h1>Jurnal accesari</h1>"
#-----------accesari=nr 
    if accesari_param == "nr":
        numar_accesari_sesiune = request.session_request_count
        text_final += f"<h3>Numar de accesari in sesiunea curenta: {numar_accesari_sesiune}</h3>"
#------------accesari=detalii
    elif accesari_param=="detalii":
        accesari= Accesare.objects.all()
        if accesari.exists():
            text_final += "<h3>Detalii accesari:</h3><ul>"
            for acc in accesari:
                text_final+=f"<li>{acc.data_accesare}</li>"
            text_final += "</ul>"    
        else:
            text_final += "<p>Nu exista accesari inregistrate</p>"

#----filtrare dupa iduri        
    if iduri_brute:
        lista_iduri_finale = []
        iduri_vazute = set()
        
        iduri_procesate = []
        for id in iduri_brute:
            iduri_procesate.extend(id.split(','))
    
        # Filtrăm dublurile dacă este necesar
        if not dubluri:
            for id_str in iduri_procesate:
                if id_str not in iduri_vazute:
                    lista_iduri_finale.append(id_str)
                    iduri_vazute.add(id_str)
        else:
            lista_iduri_finale = iduri_procesate   

        
        try:
            iduri_int = [int(id_str.strip()) for id_str in lista_iduri_finale]
            # Mai întâi, luăm toate obiectele din BD într-un dicționar.
            accesari_gasite = {acc.id: acc for acc in Accesare.objects.filter(id__in=iduri_int)}
            accesari = list(accesari_gasite.values())
        
        except ValueError:
                mesaj_eroare = "Eroare: unul dintre ID-urile specificate nu este un număr valid."   
#------ultimele=n        
    elif ultimele is not None:
        try:
            n = int(ultimele)
            if n < 0:
                mesaj_eroare = "Valoarea pentru 'ultimele' nu poate fi negativă."
            else:
                total_accesari = Accesare.objects.count()
                if n > total_accesari:
                    mesaj_eroare = f"Exista doar {total_accesari} accesari fata de {n} accesari cerute."
                accesari = Accesare.objects.all().order_by("-data_accesare")[:n]
        except ValueError:
            mesaj_eroare = "Eroare: valoarea pentru 'ultimele' trebuie să fie un număr întreg."
            
    # Dacă nu s-a specificat niciun filtru, le afișăm pe toate
    elif not iduri_brute:
        accesari = Accesare.objects.all().order_by("-data_accesare")


    if mesaj_eroare:
        text_final += f"<p style='color:red'><b>{mesaj_eroare}</b></p>"
        
        
#-----------tabel
    if accesari:
        if tabel_param:
            #----------tabel=tot
            if tabel_param.lower()=="tot":
                coloane=[field.name for field in Accesare._meta.get_fields()]
            #-------tabel=id, url...
            else:
                coloane = [col.strip() for col in tabel_param.split(',')]

            text_final += "<table border='1' style='border-collapse: collapse; width: 80%; margin-top: 20px;'>"

            #antetul tabelului
            text_final+="<thead style='background-color: #f2f2f2;'><tr>"
            for col in coloane:
                text_final += f"<th>{col.replace('_', ' ').capitalize()}</th>"
                text_final += "</tr></thead>"
                
            #corpul tabelului
            text_final += "<tbody>"
            for acc in accesari:
                text_final += "<tr>"
                for col in coloane:
                    valoare = getattr(acc, col, "N/A")
                    text_final += f"<td style='padding: 8px; text-align: left;'>{valoare}</td>"
                text_final += "</tr>"
            text_final += "</tbody>"    
            
            text_final += "</table>"

        else:
            text_final += "<ul>"
            for acc in accesari:
                text_final += f"<li>ID: {acc.id}, Data: {acc.data_accesare}, IP: {acc.ip_client}, URL: {acc.url_text}</li>"
            text_final += "</ul>"
            
    elif not mesaj_eroare:
        text_final += "<p>Nu există accesări de afișat conform filtrelor aplicate.</p>"
        

        
    if accesari:
        text_final += "<ul>"
        for acc in accesari:
            text_final += f"<li>ID: {acc.id}, Data: {acc.data_accesare}, IP: {acc.ip_client}, URL: {acc.url_text}</li>"
        text_final += "</ul>"
    elif not mesaj_eroare:
        text_final += "<p>Nu există accesări de afișat conform filtrelor aplicate.</p>" 
        

#------------statistici de accesare
    statistici=list(Accesare.objects.values('url_text').annotate(numar=Count('url_text')))
    
    if statistici:
        cel_mai_putin=min(statistici, key=lambda x: x['numar'])
        cel_mai_mult=max(statistici, key=lambda x: x['numar'])
            
        text_final += "<hr>"
        text_final += f"<p><b>Pagina cea mai putin accesata:</b> {cel_mai_putin['url_text']} ({cel_mai_putin['numar']} accesari)</p>"
        text_final += f"<p><b>Pagina cea mai accesata:</b> {cel_mai_mult['url_text']} ({cel_mai_mult['numar']} accesari)</p>"
    else:
        text_final += "<p>Nu exista accesari inregistrate.</p>"    
    
    return HttpResponse(text_final)

def afis_produse(request):
    # facem acum pt locatie, dar trb modificat pt produsele mele
    locatii= Locatie.objects.all()
    return render(request, "Cofetarie/locatii.html", 
        {
            "locatii": locatii,
            "nr_locatii": len(locatii),
        }
    )