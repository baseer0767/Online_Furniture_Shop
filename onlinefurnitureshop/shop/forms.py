from django import forms
from about.models import CartItem, Size, Colour
from django.core.exceptions import ValidationError



class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, max_value=3)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            self.fields['size'].queryset = Size.objects.filter(product_id=product_id)
            self.fields['colour'].queryset = Colour.objects.filter(product_id=product_id)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        size = self.cleaned_data['size']
        colour = self.cleaned_data['colour']
        product = size.product  # Assuming Size has a ForeignKey to Product
        if quantity > product.stock:
            raise forms.ValidationError(f"Only {product.stock} items available in stock.")
        return quantity

    class Meta:
        model = CartItem
        fields = ['size', 'colour', 'quantity']
