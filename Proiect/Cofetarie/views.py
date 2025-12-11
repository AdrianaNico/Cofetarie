from django.shortcuts import render, redirect
from .models import Accesare, Locatie, Prajitura
from django.db.models import Count
from django.http import HttpResponse
from datetime import datetime
from .forms import FiltrePrajituraForm, ContactForm
from django.contrib import messages
from django.core.paginator import Paginator
from django import forms
import os #pentru operatii pe fisiere
import json
import time
from django.conf import settings #pentru a obtine calea radacina a proiectului


from .models import Tort, Optinuni_decoratiune, Optiuni_blat, Optiuni_crema, Prajitura


from django.core.mail import send_mail

# def trimite_email():
#     send_mail(
#         subject='Salutare! Gună Adriana Nicoleta',
#         message='Salut. Ce mai faci?',
#         html_message='<h1>Salut</h1><p>Ce mai faci?</p>',
#         from_email='django.adriana@gmail.com',
#         recipient_list=['test.tweb.node@gmail.com'],
#         fail_silently=False,
#     )

def get_ip(request):
    return request.META.get('REMOTE_ADDR')

def index(request):
    return HttpResponse(f"""
        <html>
        <p><b>Pe site-ul proiectului meu, utilizatorul va putea vizualiza si comanda diferite tipuri de prajituri si de torturi. Prajiturile si torturile vor fi de cateva tipuri prestabilite, insa torturile se pot si personaliza dupa preferinte, astfel: se poate alege din mai multe tipuri de blat, mai multe creme, diferite ornamente si mesaje scrise pe tort.
        </b></p>
        <p>{request.GET.get("mesaj")}</p>
        </html>
        """)
#http://127.0.0.1:8000/Cofetarie?mesaj=Bun venit!&a=1&a=20&a=30

# def info(request):
# 	return HttpResponse(f"""
#         <html>
#         <h1>Informatii despre server</h1>
#         <p>{request.GET.get("data")}</p>
#         <p>{int(request.GET.getlist("a")[-1])}</p>
#         </html>
#         """)
#http://127.0.0.1:8000/Cofetarie/info?data=Salut&a=1&a=20&a=30

def cum_il_cheama(request):
    lista_nume= request.GET.getlist('nume')
    lista_nume= ("si "+" si ".join(lista_nume)) if lista_nume else "anonim"
    return HttpResponse(f"Pe coleg îl cheama {lista_nume}")
#http://localhost:8000/aplicatie_exemplu/cum_il_cheama_pe_coleg/?nume=ionel&nume=gigel&nume=costel

def get_context_categorii(context_base={}):
    context_base['lista_categorii'] = Prajitura.CategoriePrajitura.choices
    return context_base 


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


def afis_produse(request):
    # facem acum pt locatie, dar trb modificat pt produsele mele
    locatii= Locatie.objects.all()
    return render(request, "Cofetarie/locatii.html", 
        {
            "locatii": locatii,
            "nr_locatii": len(locatii),
        }
    )
    
    
# -------------cofetarie

def pagina_principala(request):
    # trimite_email()
    context = get_context_categorii()
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/pagina_principala.html', context)

def pagina_despre(request):
    context = get_context_categorii()
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/despre.html', context)

def pagina_produse(request):
    sort_param = request.GET.get('sort', None)
    form_data = request.GET
    form = FiltrePrajituraForm(form_data)

    VALOARE_IMPLICITA = 5
    elemente_per_pagina_anterioare = request.session.get('elemente_per_pagina', VALOARE_IMPLICITA)
    elemente_per_pagina = elemente_per_pagina_anterioare

    toate_prajiturile = Prajitura.objects.all()
    mesaj_repaginare = None
# -----formular filtrare
    if form.is_valid():
        date_filtrate = form.cleaned_data
        
        ingrediente_selectate = date_filtrate.get('ingrediente')
        if ingrediente_selectate:
            for ingredient in ingrediente_selectate:
                toate_prajiturile = toate_prajiturile.filter(ingrediente=ingredient)

        if date_filtrate.get('categorie'):
            toate_prajiturile = toate_prajiturile.filter(categorie=date_filtrate['categorie'])
        if date_filtrate.get('pret_min') is not None:
            toate_prajiturile = toate_prajiturile.filter(pret__gte=date_filtrate['pret_min'])
        if date_filtrate.get('pret_max') is not None:
            toate_prajiturile = toate_prajiturile.filter(pret__lte=date_filtrate['pret_max'])
        if date_filtrate.get('gramaj_min') is not None:
            toate_prajiturile = toate_prajiturile.filter(gramaj__gte=date_filtrate['gramaj_min'])

        valoare_noua = date_filtrate.get('elemente_per_pagina')

        if valoare_noua is not None:
            valoare_noua = int(valoare_noua)
            if valoare_noua != elemente_per_pagina_anterioare:
                mesaj_repaginare = (
                    "Ați modificat numărul de elemente pe pagină. "
                    "Vă rugăm să rețineți că repaginarea poate schimba vizualizarea produselor deja văzute."
                )

            elemente_per_pagina = valoare_noua

            if valoare_noua == VALOARE_IMPLICITA:
                request.session.pop('elemente_per_pagina', None)
            else:
                request.session['elemente_per_pagina'] = valoare_noua

    if sort_param == 'a':
        toate_prajiturile = toate_prajiturile.order_by('pret')
    elif sort_param == 'd':
        toate_prajiturile = toate_prajiturile.order_by('-pret')
    else:
        toate_prajiturile = toate_prajiturile.order_by('nume_prajitura')

    paginator = Paginator(toate_prajiturile, elemente_per_pagina) #numara cate produse o sa fie in total si imparte la elemente_per_pagina pt a vedea nr de elem pe pagina
    page_number = request.GET.get('page') #extrage nr paginii curente din url: ?page=2
    page_obj = paginator.get_page(page_number) #cere obiectele de la indexul 5 la 10(in cazul paginii 2, daca sunt 5 elem pe pagina)--se face un sql care cere
# page list contine: DATE .object_list(lista cu prajiturile de la indexurile cerute)
#                    METADATE: .number(pagina curenta), .paginator.num_pages(nr total de pagini), .has_next(), .has_previous(), .next_page_number(), .previous_page_number()

    context = {
        'page_obj': page_obj,
        'titlu_pagina': 'Lista prajituri disponibile',
        'sort_param': sort_param,
        'form': form,
        'mesaj_repaginare': mesaj_repaginare,
    }
    context = get_context_categorii(context)
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/lista_produse.html', context)



def pagina_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            date_mesaj = form.cleaned_data
            date_mesaj.pop('confirmare_email', None)
            date_mesaj['user_ip'] = get_ip(request)
            date_mesaj['data_ora_sosire'] = str(datetime.now())
            
            timestamp = int(time.time()) #
            nume_fisier = f"mesaj_{timestamp}"
            if date_mesaj.get('urgent') is True:
                nume_fisier += "_urgent"
            nume_fisier += ".json"
            
            # cream calea catre folderul de mesaje
            # settings.BASE_DIR este radacina proiectului
            cale_folder = os.path.join(settings.BASE_DIR, 'Cofetarie', 'Mesaje') #creaza calea in functie de sistemul de operare
            os.makedirs(cale_folder, exist_ok=True)#cream folderul daca nu exista, mkdirS ca sa fie recursiv
            cale_fisier = os.path.join(cale_folder, nume_fisier)
            
            try:
                with open(cale_fisier, 'w', encoding='utf-8') as f: # f variabila temporara 
                    # indent=4 face fișierul ușor de citit de oameni
                    # default=str transformă obiectele Date/Datetime în text (altfel JSON dă eroare)
                    json.dump(date_mesaj, f, indent=4, default=str, ensure_ascii=False) #scrie in fisier
                    
                messages.success(request, '✅ Mesajul tău a fost trimis cu succes! Te vom contacta în curând.')
                    
            except Exception as e:
                print(f"Eroare la salvarea fișierului: {e}")
                messages.error(request, 'A apărut o eroare la salvarea mesajului.')

            return redirect('contact')

    else:
        form = ContactForm()
    
    context = get_context_categorii()
    context['form'] = form
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/contact.html', context)


def pagina_cos_virtual(request):
    context = get_context_categorii()
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/in_lucru.html', context)


def pagina_info(request):
    
    ip = request.META.get('REMOTE_ADDR')
    
    nr_param = len(request.GET)
    nume_param = list(request.GET.keys())
    
    context = {
        "user_ip": ip,
        "numar_parametri": nr_param,
        "nume_parametri": nume_param,
    }
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/info.html', context)

def pagina_log(request):
    
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
    
        # filtram dublurile
        if not dubluri:
            for id_str in iduri_procesate:
                if id_str not in iduri_vazute:
                    lista_iduri_finale.append(id_str)
                    iduri_vazute.add(id_str)
        else:
            lista_iduri_finale = iduri_procesate   

        
        try:
            iduri_int = [int(id_str.strip()) for id_str in lista_iduri_finale]
            # luam obiectele din bd
            accesari_gasite = {acc.id: acc for acc in Accesare.objects.filter(id__in=iduri_int)}
            accesari = [
                accesari_gasite[id_int]
                for id_int in iduri_int
                if id_int in accesari_gasite
            ]
        
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
            text_final+="<thead style='background-color: #ecd4ea;'><tr>"
            for col in coloane:
                text_final += f"<th>{col.replace('_', ' ').capitalize()}</th>"
            text_final += "</tr></thead>"
                
            #corpul tabelului
            text_final += "<tbody>"
            for acc in accesari:
                text_final += "<tr>"
                for col in coloane:
                    valoare = getattr(acc, col, "N/A") # din acc(care contine adresa pt fiecare adresa) luam ce este in col pe rand(col este o lista care contine numele capetelor de tabel)
                    text_final += f"<td style='padding: 8px; text-align: left;'>{valoare}</td>"
                text_final += "</tr>"
            text_final += "</tbody>"    
            
            text_final += "</table>"

        # else:
        #     text_final += "<ul>"
        #     for acc in accesari:
        #         text_final += f"<li>ID: {acc.id}, Data: {acc.data_accesare}, IP: {acc.ip_client}, URL: {acc.url_text}</li>"
        #     text_final += "</ul>"
            
    elif not mesaj_eroare:
        text_final += "<p>Nu există accesări de afișat conform filtrelor aplicate.</p>"
        

        
    if accesari:
        text_final += "<ul>"
        for acc in accesari:
            text_final += f"<li>ID: {acc.id}, URL: {acc.url_text}</li>"
        text_final += "</ul>"
    elif not mesaj_eroare:
        text_final += "<p>Nu există accesări de afișat conform filtrelor aplicate.</p>" 
        

#------------statistici de accesare
    statistici=list(Accesare.objects.values('url_text').annotate(numar=Count('url_text'))) #agregare
    #dictionar cu url_text si numar de aparitii pt fiecare url_text
    
    if statistici:
        cel_mai_putin=min(statistici, key=lambda x: x['numar'])
        cel_mai_mult=max(statistici, key=lambda x: x['numar'])
            
        text_final += "<hr>"
        text_final += f"<p><b>Pagina cea mai putin accesata:</b> {cel_mai_putin['url_text']} ({cel_mai_putin['numar']} accesari)</p>"
        text_final += f"<p><b>Pagina cea mai accesata:</b> {cel_mai_mult['url_text']} ({cel_mai_mult['numar']} accesari)</p>"
    else:
        text_final += "<p>Nu exista accesari inregistrate.</p>"    
    
    ip = request.META.get('REMOTE_ADDR')
    context['user_ip'] = ip
    context['log_data_html'] = text_final
    context = get_context_categorii(context)
    return render(request, 'Cofetarie/log.html', context)


# detalii prajitura

def detalii_prajitura(request, id_prajitura):
    try:
        
        prajitura = Prajitura.objects.get(id=id_prajitura)
    except Prajitura.DoesNotExist:
        messages.error(request, f"Ne pare rău, prăjitura {id_prajitura} nu există.")
        return redirect('produse')
    context ={
        'prajitura': prajitura,
        'titlu_pagina': f"Detalii {prajitura.nume_prajitura}",
    }
    context = get_context_categorii(context)
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/detalii_prajitura.html', context)

def detalii_categorie(request, cod_categorie):
    choices_dict = dict(Prajitura.CategoriePrajitura.choices)
    if cod_categorie not in choices_dict:
        messages.error(request, f"Codul de categorie '{cod_categorie}' este invalid. Vă rugăm să alegeți o categorie validă din meniu.")
        return redirect('produse')
    nume_categorie = choices_dict[cod_categorie]

    form_data = request.GET.copy()
    
    categoria_din_url_params = request.GET.get('categorie')
    if categoria_din_url_params and categoria_din_url_params != cod_categorie:
        messages.error(request, "⛔ Eroare de securitate: Nu aveți voie să modificați categoria manual pe această pagină! Filtrele au fost resetate la categoria curentă.")

    form_data['categorie'] = cod_categorie #adaugam fortat parametrul pt categorie

    form = FiltrePrajituraForm(form_data)
    
    VALOARE_IMPLICITA = 5 #incearca sa preia valoarea din sesiunea anterioara. daca nu exista, o foloseste pe cea implicita
    elemente_per_pagina_anterioare = request.session.get('elemente_per_pagina', VALOARE_IMPLICITA)
    elemente_per_pagina = elemente_per_pagina_anterioare
    mesaj_repaginare = None
    
    produse_categorie = Prajitura.objects.filter(categorie=cod_categorie).order_by('nume_prajitura')
    
    if form.is_valid():
        date_filtrate = form.cleaned_data
        
        ingrediente_selectate = date_filtrate.get('ingrediente')
        if ingrediente_selectate:
            for ingredient in ingrediente_selectate:
                produse_categorie = produse_categorie.filter(ingrediente=ingredient)
                
        if date_filtrate.get('pret_min') is not None:
            produse_categorie = produse_categorie.filter(pret__gte=date_filtrate['pret_min'])
        if date_filtrate.get('pret_max') is not None:
            produse_categorie = produse_categorie.filter(pret__lte=date_filtrate['pret_max'])
        if date_filtrate.get('gramaj_min') is not None:
            produse_categorie = produse_categorie.filter(gramaj__gte=date_filtrate['gramaj_min'])
        
        valoare_noua = date_filtrate.get('elemente_per_pagina')
        
        if valoare_noua is not None:
            valoare_noua = int(valoare_noua)
            if valoare_noua != elemente_per_pagina_anterioare:
                mesaj_repaginare = (
                    "Ați modificat numărul de elemente pe pagină. "
                    "Vă rugăm să rețineți că repaginarea poate schimba vizualizarea produselor deja văzute."
                )
            
            elemente_per_pagina = valoare_noua
            
            if valoare_noua == VALOARE_IMPLICITA:
                request.session.pop('elemente_per_pagina', None)
            else:
                request.session['elemente_per_pagina'] = valoare_noua
    
    form.fields['categorie'].widget = forms.HiddenInput(attrs={'readonly': 'readonly'})
    
    # Paginare
    paginator = Paginator(produse_categorie, elemente_per_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'titlu_pagina': f'Categoria: {nume_categorie}',
        'cod_categorie': cod_categorie,
        'nume_categorie': nume_categorie,
        'form': form,
        'mesaj_repaginare': mesaj_repaginare,
        'este_pagina_categorie': True,
    }
    context = get_context_categorii(context)
    context['user_ip'] = get_ip(request)
    return render(request, 'Cofetarie/lista_produse.html', context)




# from .forms import ContactForm

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():  
#             nume = form.cleaned_data['nume'] #dictionar
#             email = form.cleaned_data['email']
#             mesaj = form.cleaned_data['mesaj']
#             # procesarea datelor
            
#             return redirect('mesaj_trimis')
#     else:
#         form = ContactForm()
#     return render(request, 'aplicatie_exemplu/contact.html', {'form': form})


# ----formular
# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():  
#             nume = form.cleaned_data['nume']
#             email = form.cleaned_data['email']
#             mesaj = form.cleaned_data['mesaj']
#             return redirect('mesaj_trimis')
#     else:
#         form = ContactForm()
#     return render(request, 'aplicatie_exemplu/contact.html', {'form': form})


# def clean(self):
#     cleaned_data = super().clean()
#     email = cleaned_data.get("email")
#     confirm_email = cleaned_data.get("confirm_email")
#     if email and confirm_email and email != confirm_email:
#         raise forms.ValidationError("Adresele de email nu coincid.")


