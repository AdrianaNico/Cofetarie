from django import forms
from .models import Prajitura

# class ContactForm(forms.Form):
#     nume = forms.CharField(max_length=100, label='Nume', required=True)
#     email = forms.EmailField(label='Email', required=True)
#     mesaj = forms.CharField(widget=forms.Textarea, label='Mesaj', required=True)
    
    
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
    
    elemente_per_pagina = forms.IntegerField(
        required=False,
        label='Elemente per pagină',
        initial=5,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={'placeholder': '5'})
    )