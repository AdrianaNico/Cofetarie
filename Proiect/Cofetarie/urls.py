from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import SchimbareParolaForm
urlpatterns = [
	# path("", views.index, name="index"),
    # path("info", views.info, name="info"),
    # path("cum_il_cheama_pe_coleg", views.cum_il_cheama, name="cum_il_cheama"),
    path("data", views.afis_data, name="afis_data"),
    # path("exemplu_template", views.afis_template, name="exemplu"),
    # path('log', views.log_view, name='pagina_log'),
    # path('produse', views.afis_produse, name='produse'),
    
    path('', views.pagina_principala, name='acasa'), 
    
    path('despre/', views.pagina_despre, name='despre'),
    path('produse/', views.pagina_produse, name='produse'),
    path('contact/', views.pagina_contact, name='contact'),
    path('cos/', views.pagina_cos_virtual, name='cos_virtual'),
    path('log/', views.pagina_log, name='log'),
    path('info/', views.pagina_info, name='info'),
    path('produse/<int:id_prajitura>/', views.detalii_prajitura, name='detalii_prajitura'),
    path('categorii/<str:cod_categorie>/', views.detalii_categorie, name='detalii_categorie'),
    path('inregistrare/', views.inregistrare_view, name='inregistrare'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profil/', views.profil_view, name='profil'),
    path('adauga_produs/', views.adauga_produs, name='adauga_produs'),
    path('confirmare_email/<str:cod>/', views.confirma_mail_view, name='confirma_mail'),
    path('promotii/', views.promotii_view, name='promotii'),
    
    path('schimbare-parola/', auth_views.PasswordChangeView.as_view(
        template_name='Cofetarie/schimbare_parola.html', 
        success_url='/Cofetarie/profil/',
        form_class = SchimbareParolaForm,
    ), name='schimbare_parola'),
]
#data= cum se scrie in adresa, view si name este numele functiei din views
