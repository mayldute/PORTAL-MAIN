from django import forms

class CategorySubscriptionForm(forms.Form):
       category = forms.ChoiceField(
           widget=forms.Select(attrs={'style': 'width: 30vh; height: 40px; font-size: 16px;'}),
           label='Выберите категорию:'
       )

       def __init__(self, *args, **kwargs):
           categories = kwargs.pop('categories', [])
           super().__init__(*args, **kwargs)
           self.fields['category'].choices = categories

        

