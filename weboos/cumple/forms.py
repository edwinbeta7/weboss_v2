from django import forms

class CumpleForm(forms.Form):
    id = forms.IntegerField(label='ID', required=True, widget=forms.NumberInput(
        attrs={'class':'form-control'}), max_length=3)
    name = forms.CharField(label='NOMBRE_FUNCIONARIO', required=True, widget=forms.TextInput(
        attrs={'class':'form-control'}), min_length=3, max_length=100)
    nameshort = forms.CharField(label='NOMBRE_CORTO', required=True, widget=forms.TextInput(
        attrs={'class':'form-control'}), min_length=2, max_length=100)
    mes = forms.IntegerField(label='MES_CUMPLE', required=True, widget=forms.NumberInput(
        attrs={'class':'form-control'}), max_length=2)
    dia = forms.IntegerField(label='DIA_CUMPLE', required=True, widget=forms.NumberInput(
        attrs={'class':'form-control'}), max_length=2)
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(
        attrs={'class':'form-control', 'placeholder':'Escribe tu e-mail'}
    ), min_length=3, max_length=100)