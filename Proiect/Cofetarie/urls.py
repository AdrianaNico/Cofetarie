from django.urls import path
from . import views
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
]
#data= cum se scrie in adresa, view si name este numele functiei din views
