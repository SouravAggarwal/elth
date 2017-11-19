from django import forms

class ChatForm(forms.Form):
    text = forms.CharField(label='Type Here', max_length=1000)
