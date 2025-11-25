from django import forms
from .models import Prajitura
from datetime import date
import re


class FiltrePrajituraForm(forms.Form):
    categorie = forms.ChoiceField(
    choices=[('', 'Toate categoriile')] + list(Prajitura.CategoriePrajitura.choices),
    required=False,
    label='Categorie'
    )


    pret_min = forms.DecimalField(
        required=False,
        label='Pret minim',
        max_digits=8,
        decimal_places=2,
        initial=0.00,
        widget=forms.NumberInput(attrs={'placeholder':'0.00'})
    )
    
    pret_max = forms.DecimalField(
        required=False,
        label='Pret maxim',
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder':'999.99'})
    )
    
    gramaj_min = forms.DecimalField(
        required=False,
        label='Gramaj minim',
        widget=forms.NumberInput(attrs={'placeholder':'50'})
    )
    
    gramaj_max = forms.IntegerField(
        required=False,
        label='Gramaj maxim',
        widget=forms.NumberInput(attrs={'placeholder': '500'})
    )
    
    elemente_per_pagina = forms.IntegerField(
        required=False,
        label='Elemente per pagină',
        initial=5,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={'placeholder': '5'})
    )
    
    def clean_pret_max(self):
        pret_min = self.cleaned_data.get('pret_min')
        pret_max = self.cleaned_data.get('pret_max')
        if pret_min is not None and pret_max is not None and pret_max < pret_min:
            raise forms.ValidationError(
                "Eroare: Pretul maxim nu poate fi mai mic decat cel minim."
            )
        return pret_max
    
    def clean_gramaj_min(self):
        gramaj_min = self.cleaned_data.get('gramaj_min')
        if gramaj_min is not None and gramaj_min < 0:
            raise forms.ValidationError(
                "Gramajul minim nu poate fi o valoare negativă."
            )
        return gramaj_min
    
class ContactForm(forms.Form):
    TIP_MESAJ_CHOICES = [
        ('N', '--- Neselectat ---'),
        ('R', 'Reclamație'),
        ('I', 'Întrebare'),
        ('V', 'Review'),
        ('C', 'Cerere'),
        ('P', 'Programare'),
    ]
    
    nume = forms.CharField(
        max_length=10,
        required=True,
        label='Nume',
        widget=forms.TextInput(attrs={'placeholder': "Numele:"})
    )
    
    prenume = forms.CharField(
        max_length=10,
        required=True,
        label='Prenume',
        widget=forms.TextInput(attrs={'placeholder': "Prenumele:"})
    )
    
    cnp = forms.CharField(
        max_length=13,
        min_length=13,
        required=False,
        label="CNP",
        widget=forms.TextInput(attrs={'placeholder':'CNP(13 cifre)'})
    )
    
    
    data_nasterii = forms.DateTimeField(
        required=True,
        label='Data Nasterii',
        widget=forms.DateInput(attrs={'type':'date'})
    )
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'Adresa de Email'})
    )

    confirmare_email = forms.EmailField(
        required=True,
        label='Confirmare E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'Reintroduceți adresa de Email'})
    )
    
    tip_mesaj = forms.ChoiceField(
        choices=TIP_MESAJ_CHOICES,
        required=True,
        label='Tip mesaj',
        initial='N',
        widget=forms.Select()
    )

    subiect = forms.CharField(
        max_length=100,
        required=True,
        label='Subiect',
        widget=forms.TextInput(attrs={'placeholder': 'Subiectul mesajului'})
    )
    
    minim_zile_asteptare = forms.IntegerField(
        required=True,
        label='Minim zile așteptare',
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 30})
    )

    mesaj = forms.CharField(
        required=True,
        label='Mesaj (Vă rugăm să semnați la finalul mesajului)', 
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Scrieți mesajul aici...'})
    )
    
    
    # def clean(self):
    #     """Validări la nivelul întregului formular."""
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     confirmare_email = cleaned_data.get("confirmare_email")
    #     tip_mesaj = cleaned_data.get("tip_mesaj")
    #     data_nasterii = cleaned_data.get("data_nasterii")
    #     minim_zile_asteptare = cleaned_data.get("minim_zile_asteptare")
        
    #     # VALIDARE 1: E-mail și Confirmare E-mail
    #     if email and confirmare_email and email != confirmare_email:
    #         self.add_error('confirmare_email', "⛔ Adresele de email nu coincid.")

    #     # VALIDARE 2: Data Nașterii (Trebuie să fie în trecut)
    #     if data_nasterii and data_nasterii > date.today():
    #          self.add_error('data_nasterii', "📅 Data nașterii nu poate fi în viitor.")

    #     # VALIDARE 3: Tip Mesaj (Nu permite 'Neselectat')
    #     if tip_mesaj == 'N':
    #         self.add_error('tip_mesaj', "🚫 Vă rugăm să selectați un tip de mesaj valid.")
            
    #     # VALIDARE 4: CNP (Dacă este introdus, verifică formatul)
    #     cnp = cleaned_data.get("cnp")
    #     if cnp and not re.fullmatch(r'\d{13}', cnp):
    #         self.add_error('cnp', "CNP-ul trebuie să conțină exact 13 cifre.")

    #     # VALIDARE 5: Minim Zile Așteptare (Validare dependentă de Tip Mesaj)
    #     if tip_mesaj and minim_zile_asteptare is not None:
            
    #         # Eticheta: "Pentru review-uri/cereri minimul de zile de asteptare trebuie setat de la 4 incolo.
    #         # Iar pentru cereri/intrebari de la 2 incolo." (Am simplificat logica)

    #         if tip_mesaj in ['V', 'C'] and minim_zile_asteptare < 4: # Review (V) sau Cerere (C)
    #              self.add_error('minim_zile_asteptare', "Minimul de așteptare pentru Review-uri și Cereri trebuie să fie de minim 4 zile.")
            
    #         elif tip_mesaj in ['C', 'I'] and minim_zile_asteptare < 2: # Cerere (C) sau Întrebare (I)
    #              self.add_error('minim_zile_asteptare', "Minimul de așteptare pentru Cereri și Întrebări trebuie să fie de minim 2 zile.")
                 
    #     return cleaned_data