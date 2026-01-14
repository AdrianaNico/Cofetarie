# Register your models here.
from django.contrib import admin
# from .models import Organizator, Locatie
from .models import Tort, Optiuni_decoratiune, Optiuni_blat, Optiuni_crema, Ingrediente, Prajitura, User, Vizualizare, Promotie, LogareSuspecta

admin.site.site_header = "Panou de Administrare Site"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"

# admin.site.register(Organizator)
# admin.site.register(Locatie)

class OptiuniBlatAdmin(admin.ModelAdmin):
    list_display = ('nume_blat', 'calorii','pret',)  # afișează câmpurile în lista de obiecte
    list_filter = ('nume_blat', 'pret')  # adaugă filtre laterale
    search_fields = ('nume_blat', 'pret', )  # permite căutarea după anumite câmpuri
    ordering = ['nume_blat', '-pret']
        # punem virgula ca sa il vada ca un tuplu
    list_per_page = 5 #nr de obiecte afisate pe pagina/ PAGINATOR
    
admin.site.register(Optiuni_blat, OptiuniBlatAdmin)

class TortAdmin(admin.ModelAdmin):
    list_display = ('nume_personalizat', 'pret_calculat', 'blat', 'crema', 'data_comanda')
    search_fields = ('nume_personalizat', 'descriere_tort') 
    ordering = ('-data_comanda',) 
    list_per_page = 5 
    fieldsets = (
        ('Detalii Esențiale', {
            'fields': ('nume_personalizat', 'gramaj', 'blat', 'crema', 'ingrediente')
        }),
        ('Opțiuni Suplimentare', {
            'fields': ('descriere_tort',),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Tort, TortAdmin)


# admin.site.register(Tort)
# admin.site.register(Optiuni_blat)
admin.site.register(Optiuni_crema)
admin.site.register(Optiuni_decoratiune)
admin.site.register(Ingrediente)
admin.site.register(Prajitura)
admin.site.register(User)
admin.site.register(Vizualizare)
admin.site.register(Promotie)
admin.site.register(LogareSuspecta)