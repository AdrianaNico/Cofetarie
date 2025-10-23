from django.contrib import admin
from .models import Organizator, Locatie

# Register your models here.
admin.site.register(Organizator)


class LocatieAdmin(admin.ModelAdmin):
    list_display = ('oras', 'judet')  # afișează câmpurile în lista de obiecte
    list_filter = ('oras', 'judet')  # adaugă filtre laterale
    search_fields = ('oras', )  # permite căutarea după anumite câmpuri
        # punem virgula ca sa il vada ca un tuplu
    
    fieldsets = (
    ('Date Generale', {
        'fields': ('oras', 'judet')
    }),
    ('Date Specifice', {
        'fields': ('adresa','cod_postal'),
        'classes': ('collapse',),  # secțiune pliabilă
    }),
)


admin.site.register(Locatie, LocatieAdmin)
# admin.site.register(Locatie)

admin.site.site_header = "Panou de Administrare Site"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"