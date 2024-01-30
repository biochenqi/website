from django import forms


class QueryForm(forms.Form):
    QT = (
        ('Gene', 'Gene'),
        ('Sample', 'Sample')
    )
    query_type = forms.ChoiceField(choices=QT)
    query_content = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
