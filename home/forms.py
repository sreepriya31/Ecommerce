from django import forms
from .models import Product, Category, Comment, Profile

class ProductForm(forms.ModelForm):

    class Meta:
        model=Product
        exclude=['us']

class CategoryForm(forms.ModelForm):

    class Meta:
        model=Category
        fields='__all__'

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=['cmnt']

class ProfileForm(forms.ModelForm):

    class Meta:
        model=Profile
        exclude=['us']