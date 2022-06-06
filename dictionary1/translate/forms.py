from django import forms


class RawPhraseForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 15, 'cols': 60}))
    language_choices=(('en', 'English'), ('pl', 'Polish'), ('es', 'Spanish'), ('pt', 'Portuguese'), ('de', 'German'), ('fr', 'French'),)
    translate_from = forms.ChoiceField(widget=forms.Select, choices=language_choices)
    translate_to   = forms.ChoiceField(widget=forms.Select, choices=language_choices)

class RawPhraseForm_Synonym(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
