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

class Optiuni_blat(models.Model):
    nume_blat = models.CharField(max_length=100, unique=True)
    pret = models.DecimalField(max_digits=8, default=0.00, decimal_places=2)
    calorii = models.IntegerField(default=0)

    def __str__(self):
        return self.nume_blat
    
    class Meta:
        verbose_name_plural = "Opțiuni Blaturi"



class Optiuni_crema(models.Model):
    nume_crema = models.CharField(max_length=100, unique=True)
    insertie_fructe = models.BooleanField(default=False)
    pret = models.DecimalField(max_digits=8, default=0.00, decimal_places=2)
    calorii = models.IntegerField(default=0)

    def __str__(self):
        return self.nume_crema

    class Meta:
        verbose_name_plural = "Opțiuni Creme"



class Optinuni_decoratiune(models.Model):
    nume_decoratiune = models.CharField(max_length=100, unique=True)
    detalii = models.TextField(null=True, blank=True)
    pret = pret = models.DecimalField(max_digits=8, default=0.00, decimal_places=2)
# --FK
    tort = models.ForeignKey("Tort", on_delete=models.CASCADE, related_name="decoratiuniunile_tortului")

    def __str__(self):
        return f"{self.nume_decoratiune} (pentru {self.tort})"
        
    class Meta:
        verbose_name = "Opțiune Decorațiune"
        verbose_name_plural = "Opțiuni Decorațiuni"




class Ingrediente(models.Model):
    nume_ingredient = models.CharField(max_length=100, unique=True)
    este_alergen = models.BooleanField(default=False)
    detalii_alergen = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nume_ingredient

    class Meta:
        verbose_name_plural = "Ingrediente"




class Tort(models.Model):
    nume_personalizat = models.CharField(max_length=255)
    pret_calculat = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Pretul va fi calculat automat la salvare")
    data_comanda = models.DateTimeField(auto_now_add=True) #data si ora creari obiectului tort
    descriere_tort = models.TextField(null=True, blank=True)
    gramaj = models.IntegerField()
    calorii = models.IntegerField(default=0, help_text="Numarul de calorii va fi calculat automat la salvare")
# ---FK
    blat = models.ForeignKey('Optiuni_blat', on_delete=models.PROTECT, related_name="torturi_cu_acest_blat")
    crema = models.ForeignKey('Optiuni_crema', on_delete=models.PROTECT, related_name="torturi_cu_aceasta_crema")
    
    ingrediente = models.ManyToManyField('Ingrediente', blank=True, related_name="ingrediente_in_torturi")
    
# ---calcul automat pt pret si calorii
    def save(self, *args, **kwargs):
        total_pret=0
        total_calorii=0
        
        if self.blat:
            total_pret +=self.blat.pret
            total_calorii +=self.blat.calorii
            
        if self.crema:
            total_pret +=self.crema.pret
            total_calorii +=self.crema.calorii
            
        self.pret_calculat = total_pret
        self.calorii = total_calorii
        
    # salvam in baza de date
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        if self.nume_personalizat:
            return f"Tort: {self.nume_personalizat}"
        return f"Tort #{self.id}" 
    
    class Meta:
        verbose_name = "Tort"
        verbose_name_plural = "Torturi"




class Prajitura(models.Model):
    
    class CategoriePrajitura(models.TextChoices):
        RED_VELVET = 'RV', 'Red Velvet'
        CHEESECAKE = 'CS', 'Cheesecake'
        CINNAMON_ROLLS = 'CR', 'Cinnamon Rolls'
        NEGRESA = 'NG', 'Negresa'
        ECLER = 'EC', 'Ecler'
        ALTUL = 'AL', 'Altul'
    
    nume_prajitura = models.CharField(max_length=255)
    descriere_prajitura = models.TextField(null=True, blank=True)
    gramaj = models.IntegerField()
    pret = models.DecimalField(max_digits=6, decimal_places=2)
    
    categorie = models.CharField(max_length=2, choices=CategoriePrajitura.choices, default=CategoriePrajitura.ALTUL)
    
    ingrediente = models. ManyToManyField("Ingrediente")
    
    imagine = models.ImageField(upload_to='media/prajituri', null=True, blank=True)
    def __str__(self):
        return self.nume_prajitura
    
    
    class Meta:
        verbose_name_plural = "Prajituri"
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!de pus poze la praji
    
    
    
    
    
    