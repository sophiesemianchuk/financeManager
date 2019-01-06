from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Transaction


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='This field is required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='This field is required.')
    email = forms.EmailField(max_length=200, required=True, help_text='This field is required.')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class CategoryForm(forms.ModelForm):
    category = forms.CharField(max_length=100, required=True, help_text='Please add category name..')
    description = forms.CharField(max_length=300, required=False, help_text='It does not have to be.')

    class Meta:
        model = Category
        fields = (
            'category',
            'description',
        )


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text='Please select category..')
    operation = forms.CharField(max_length=8, required=True, help_text='Please select operation..')
    sum = forms.DecimalField(max_digits=7, decimal_places=2)
    date_operation = forms.DateField(required=True)
    description = forms.CharField(max_length=300)

    class Meta:
        model = Transaction
        fields = (
            'category',
            'operation',
            'sum',
            'date_operation',
            'description',
        )
