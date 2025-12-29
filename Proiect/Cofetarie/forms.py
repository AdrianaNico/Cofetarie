from django import forms
from .models import Prajitura, Ingrediente, User
from datetime import date
import re
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


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
    
    ingrediente = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all().order_by('nume_ingredient'),
        required=False,
        label='Ingrediente',
        widget=forms.SelectMultiple(attrs={
            'class': 'ingrediente-select',
            'size': '1', #dropdown in loc de lista
            'style': 'width: 100%;'
        }),
    )
    
    elemente_per_pagina = forms.IntegerField(
        required=False,
        label='Elemente per pagină',
        initial=5,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={'placeholder': '5'})
    )
    
    # def clean_pret_max(self):
    #     pret_min = self.cleaned_data.get('pret_min')
    #     pret_max = self.cleaned_data.get('pret_max')
    #     if pret_min is not None and pret_max is not None and pret_max < pret_min:
    #         raise forms.ValidationError(
    #             "Eroare: Pretul maxim nu poate fi mai mic decat cel minim."
    #         )
    #     return pret_max
    
    def clean_gramaj_min(self):
        gramaj_min = self.cleaned_data.get('gramaj_min')
        if gramaj_min is not None and gramaj_min < 0:
            raise forms.ValidationError(
                "Gramajul minim nu poate fi o valoare negativă."
            )
        return gramaj_min
    
    def clean_pret_min(self):
        pret_min = self.cleaned_data.get('pret_min')
        if pret_min is not None and pret_min < 0:
            raise forms.ValidationError(
                "Pretul minim nu poate fi o valoare negativă."
            )
        return pret_min
    
    def clean_elemente_per_pagina(self):
        elemente = self.cleaned_data.get('elemente_per_pagina')
        if elemente:
            if elemente > 100:
                raise forms.ValidationError("Nu puteți afișa mai mult de 100 de produse pe o singură pagină.")
            if elemente < 1:
                raise forms.ValidationError("Trebuie să afișați cel puțin un produs pe pagină.")
        return elemente
    
    def clean(self):
        cleaned_data = super().clean() #super= inainte de a valida formularul personalizat, ruleaza validarea parintelui(forms.Form)
        
        pret_min = cleaned_data.get('pret_min')
        pret_max = cleaned_data.get('pret_max')

        if pret_min is not None and pret_max is not None:
            if pret_max < pret_min:
                self.add_error('pret_max', "Eroare: Prețul maxim nu poate fi mai mic decât cel minim.")
                
        return cleaned_data
        
        
    
# mutate din contact form ca sa fie folosite si in prajituraForm
    
    
def validate_major(value):
        if not value:
            return

        today = date.today()
        if value > today:
            raise ValidationError("📅 Data nașterii nu poate fi în viitor.", code='future_date')
        
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise forms.ValidationError("Trebuie să aveți cel puțin 18 ani pentru a trimite acest formular.")
        return value


def validate_message_word_count(value):
    words = re.findall(r'[A-Za-z0-9ȘșȚțĂăÂâÎî]+', value) #cauta toate aparitiile si le pune intr o lista. + lipeste literele dintr un cuvant. daca gasesete cv ce nu coincide, pune la lista si continua
    count = len(words)
    
    if count < 5 or count > 100:
        raise ValidationError(f'Mesajul trebuie să conțină între 5 și 100 de cuvinte. (Actual: {count})')


def validate_message_word_length(value):
    words = re.findall(r'[A-Za-z0-9ȘșȚțĂăÂâÎî]+', value)
    for word in words:
        if len(word) > 15:
            raise ValidationError(f'Cuvântul "{word}" depășește limita de 15 caractere ({len(word)}).', code='word_too_long')


def validate_no_links(value):
    # Nici mesajul și nici subiectul nu pot contine linkuri
    if re.search(r'https?://[^\s]+', value, re.IGNORECASE): #[^\s]= orice mai putin spatiu. https?= s e optional
        raise ValidationError('Textul nu poate conține linkuri (http:// sau https://).')
    
    
def validate_uppercase_chars(value):
        #textul incepe cu litera mare si e format doar din spatii, cratima si litere.
        if not value:
            return
        if not value[0].isupper():
            raise ValidationError('Textul trebuie să înceapă cu literă mare.')
            
        if not re.fullmatch(r'^[A-Za-zȘșȚțĂăÂâÎî\s\-]+$', value): #verifica de la inceput(^) pana la sfarsit($) fiecare litera. daca gaseste neregula, se opreste
            raise ValidationError('Textul poate conține doar litere, spații și cratime.')

def validate_uppercase(value):
    # dupa spatiu sau cratima aveti litera mare
    if not value:
        return
        
    matches = re.findall(r'([\s\-])([a-zșțăâî])', value) #numara toate greselille(cauta in tot textul)
    if matches:
        raise ValidationError('După spațiu sau cratimă trebuie să urmeze literă mare.')

def validate_cnp(value):
        # verificare cnp - trebuie sa inceapa cu 1 sau 2, sa contina doar cifre si sa aiba data valida
        if not value:
            return
            
        # Verifică doar cifre (deja parțial verificat de CharField/min_length)
        if not value.isdigit():
            raise ValidationError('CNP-ul trebuie să conțină doar cifre.')
        
        if value[0] not in ['1', '2','5','6']:
            raise ValidationError('CNP-ul nu este valid.')
        
        an = value[1:3]
        luna = value[3:5]
        zi = value[5:7]

        try:
            if value[0] in ['1', '2']:
                an_complet = 1900 + int(an)
            elif value[0] in ['5', '6']:
                an_complet = 2000 + int(an)
                
            datetime(an_complet, int(luna), int(zi))
        except ValueError:
            raise ValidationError('Cifrele din CNP nu formează o dată validă (AA/LL/ZZ).')


def validate_no_temp_email(value):
    # Verificati ca e-mailul nu este unul temporar, avand ca domeniu guerillamail.com sau yopmail.com
    if not value:
        return
        
    domain = value.split('@')[-1].lower()
    BLOCKED_DOMAINS = ['guerillamail.com', 'yopmail.com']
    
    if domain in BLOCKED_DOMAINS:
        raise ValidationError('Adresa de e-mail nu poate avea domenii temporare.')


class ContactForm(forms.Form):
    TIP_MESAJ_CHOICES = [
        ('N', '--- Neselectat ---'),
        ('R', 'Reclamație'),
        ('I', 'Întrebare'),
        ('V', 'Review'),
        ('C', 'Cerere'),
        ('P', 'Programare'),
    ]
    
        # ------------functii de validare formular contact 


    def clean(self):
        """Validări la nivelul întregului formular."""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirmare_email = cleaned_data.get("confirmare_email")
        tip_mesaj = cleaned_data.get("tip_mesaj")
        data_nasterii = cleaned_data.get("data_nasterii")
        minim_zile_asteptare = cleaned_data.get("minim_zile_asteptare")
        cnp = cleaned_data.get("cnp")
        mesaj = cleaned_data.get("mesaj")
        nume = cleaned_data.get("nume")
        
        if email and confirmare_email and email != confirmare_email:
            self.add_error('confirmare_email', "⛔ Adresele de email nu coincid.")

        
        if mesaj and nume:
            words = re.findall(r'[A-Za-z0-9ȘșȚțĂăÂâÎî]+', mesaj)
            if not words or words[-1].lower() != nume.lower():
                self.add_error('mesaj', "✍️ Vă rugăm să semnați mesajul cu numele dumneavoastră la final.")
        
        if cnp and data_nasterii:
            
            if cnp[0] in ['5', '6']:
                prefix_an = "20"
            elif cnp[0] in ['1', '2']:
                prefix_an = "19"
            year =int( prefix_an + cnp[1:3])
            
            month = int(cnp[3:5])
            day = int(cnp[5:7])
            try:
                cnp_date = date(year, month, day)
                if cnp_date != data_nasterii:
                    self.add_error('cnp', "📅 Data nașterii din CNP nu corespunde cu data introdusă.")
            except ValueError:
                pass
            
            
        # Minim zile asteptare (Validare de tip mesaj)            
        if tip_mesaj == 'N':
            self.add_error('tip_mesaj', "🚫 Vă rugăm să selectați un tip de mesaj valid.")

        if tip_mesaj and minim_zile_asteptare is not None:
            
            # "Pentru review-uri/cereri minimul de zile de asteptare trebuie setat de la 4 incolo.
            # Iar pentru cereri/intrebari de la 2 incolo."

            if tip_mesaj in ['V', 'C'] and minim_zile_asteptare < 4 and minim_zile_asteptare < 30 : # Review (V) sau Cerere (C)
                self.add_error('minim_zile_asteptare', "Minimul de așteptare pentru Review-uri și Cereri trebuie să fie de minim 4 zile, maxim 30.")
            
            elif tip_mesaj in ['C', 'I'] and minim_zile_asteptare < 2 and minim_zile_asteptare < 30 : # Cerere (C) sau Întrebare (I)
                self.add_error('minim_zile_asteptare', "Minimul de așteptare pentru Cereri și Întrebări trebuie să fie de minim 2 zile, maxim 30.")

        # --procesarea datelor

        if data_nasterii:
            today = date.today()
            year = today.year - data_nasterii.year
            months = today.month - data_nasterii.month
            if today.day < data_nasterii.day:
                months -= 1
            # ajustare daca am trecut in anul anterior(lunile devin negative)
            if months < 0:
                year -= 1
                months += 12
                
            cleaned_data['varsta'] = f"{year} ani și {months} luni"
            
        if mesaj:
            mesaj_procesat = re.sub(r'\s+', ' ', mesaj.replace('\n', ' ')).strip() #inlocuim enter cu space, apoi facem re.sub: ce vrem sa inlocuim(spatiile mutiple), cu ce inlocuim(spatiu singur), din ce sir(cel fara enter).
            def capitalize_match(match):
                # returnam semnul + spatiul + litera facuta mare
                return match.group(1) + match.group(2) + match.group(3).upper() #match.group(0)= tot ce a gasit in regex, restul parantezele din regex

            mesaj_procesat = re.sub(r'([.?!]|\.\.\.)(\s+)([a-zșțăâî])', capitalize_match, mesaj_procesat)
            
            cleaned_data['mesaj'] = mesaj_procesat
            
        if tip_mesaj and minim_zile_asteptare is not None:
            limita_minima = 0
            if tip_mesaj in ['V', 'C']:
                limita_minima = 4
            elif tip_mesaj == 'I':
                limita_minima = 2
            
            if minim_zile_asteptare == limita_minima:
                cleaned_data['urgent'] = True
            else:
                cleaned_data['urgent'] = False
            
        return cleaned_data


    nume = forms.CharField(
        max_length=10,
        required=True,
        label='Nume',
        widget=forms.TextInput(attrs={'placeholder': "Numele:"}),
        validators=[validate_uppercase_chars, validate_uppercase]
    )
    
    prenume = forms.CharField(
        max_length=20,
        required=False,
        label='Prenume',
        widget=forms.TextInput(attrs={'placeholder': "Prenumele:"}),
        validators=[validate_uppercase_chars, validate_uppercase]
    )
    
    cnp = forms.CharField(
        max_length=13,
        min_length=13,
        required=False,
        label="CNP",
        widget=forms.TextInput(attrs={'placeholder':'CNP(13 cifre)'}),
        validators=[validate_cnp]
    )
    
    data_nasterii = forms.DateField(
        required=True,
        label='Data Nasterii',
        widget=forms.DateInput(attrs={'type':'date'}),
        validators=[validate_major]
    )
    
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'Adresa de Email'}),
        validators=[validate_no_temp_email]
    )

    confirmare_email = forms.EmailField(
        required=True,
        label='Confirmare E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'Reintroduceți adresa de Email'}),
        validators=[validate_no_temp_email]
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
        widget=forms.TextInput(attrs={'placeholder': 'Subiectul mesajului'}),
        validators=[validate_uppercase_chars, validate_no_links]
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
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Scrieți mesajul aici...'}),
        validators=[validate_message_word_count, validate_message_word_length, validate_no_links]
    )


class PrajituraForm(forms.ModelForm):
    
    nume_prajitura = forms.CharField(
        label="Nume Prajitură",
        validators=[validate_uppercase_chars]
    )
    
    descriere = forms.CharField(
        label="Descriere",
        widget=forms.Textarea,
        validators=[validate_uppercase_chars, validate_message_word_length],
        required=True
    )
    
    cost_productie = forms.DecimalField(
        label="Cost de producție (RON)",
        max_digits=6,
        decimal_places=2,
        help_text="Introduceți costul materiilor prime."
    )

    adaos_comercial = forms.IntegerField(
        label="Adaos Comercial (%)",
        initial=0,
        help_text="Procentul adăugat la cost."
    )
    class Meta:
        model = Prajitura
        fields = ['nume_prajitura', 'categorie', 'gramaj', 'ingrediente', "imagine"]
        
        
    def clean_adaos_comercial(self):
        adaos = self.cleaned_data.get('adaos_comercial')
        
        if adaos is not None:
            if adaos < 0:
                raise ValidationError("Adaosul comercial nu poate fi negativ.")
            if adaos > 300:
                raise ValidationError("Adaosul comercial este prea mare (maxim 300%).")
        return adaos

    def clean_cost_productie(self):
        cost = self.cleaned_data.get('cost_productie')
        
        if cost is not None and cost <= 0:
            raise ValidationError("Costul de producție trebuie să fie strict pozitiv (mai mare ca 0).")
        return cost

    def clean_descriere(self):
        descriere = self.cleaned_data.get('descriere')
        
        if descriere:
            if len(descriere) < 20:
                raise ValidationError(f"Descrierea este prea scurtă ({len(descriere)} caractere). Vă rugăm scrieți minim 20 de caractere.")
        
        return descriere
    
    def clean(self):
        cleaned_data = super().clean()
        
        nume = cleaned_data.get('nume_prajitura')
        descriere = cleaned_data.get('descriere')
        
        if nume and descriere:
            if nume.lower() == descriere.strip().lower():
                self.add_error('descriere', "Descrierea nu poate fi identică cu numele prăjiturii.")
        
        return cleaned_data
        



class InregistrareForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefon', 'adresa', 'oras', 'data_nasterii', 'promotii']
        
        widgets = {
            'data_nasterii': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
        # labels = {
        #     'first_name': 'Prenume',
        #     'last_name': 'Nume',
        #     'telefon': 'Număr de telefon',
        #     'adresa': 'Adresă',
        #     'oras': 'Oraș',
        #     'data_nasterii': 'Data nașterii',
        # }
    
    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if not telefon.isdigit():
            raise ValidationError("Numărul de telefon trebuie să conțină doar cifre.")
        if len(telefon) != 10:
            raise ValidationError("Numărul de telefon trebuie să aibă exact 10 cifre.")
        if not telefon.startswith('07'):
            raise ValidationError("Numărul de telefon trebuie să înceapă cu '07'.")
        return telefon

    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        if data_nasterii:
            azi = date.today()
            varsta = azi.year - data_nasterii.year - ((azi.month, azi.day) < (data_nasterii.month, data_nasterii.day))
            if varsta < 18:
                raise ValidationError("Trebuie să aveți minim 18 ani pentru a vă înregistra.")
        return data_nasterii

    def clean_oras(self):
        oras = self.cleaned_data.get('oras')
        if oras and not oras[0].isupper():
            raise ValidationError("Numele orașului trebuie să înceapă cu majusculă.")
        return oras
    
    
    def clean_password1(self):
        parola = self.cleaned_data.get('password1')
        
        if parola:
            if len(parola) < 8:
                raise ValidationError("Parola nouă trebuie să aibă minim 8 caractere.")
            if not re.search(r'[A-Z]', parola):
                raise ValidationError("Parola nouă trebuie să conțină cel puțin o literă mare.")
            if not re.search(r'[0-9]', parola):
                raise ValidationError("Parola nouă trebuie să conțină cel puțin o cifră.")
        return parola

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = None
        
        self.fields['password1'].help_text = "Reguli: minim 8 caractere, o literă mare și o cifră."

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        label="Ține-mă minte logat pentru o zi",
        widget=forms.CheckboxInput()
    )
    
    
class SchimbareParolaForm(PasswordChangeForm):
    def clean_new_password1(self):
        parola = self.cleaned_data.get('new_password1')
        
        if parola:
            if len(parola) < 8:
                raise ValidationError("Parola nouă trebuie să aibă minim 8 caractere.")
            if not re.search(r'[A-Z]', parola):
                raise ValidationError("Parola nouă trebuie să conțină cel puțin o literă mare.")
            if not re.search(r'[0-9]', parola):
                raise ValidationError("Parola nouă trebuie să conțină cel puțin o cifră.")
        return parola

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields['new_password1'].help_text = "Reguli: minim 8 caractere, o literă mare și o cifră."