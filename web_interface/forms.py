from django import forms

class SwipecodeForm(forms.Form):
    swipecode = forms.CharField(max_length=400)