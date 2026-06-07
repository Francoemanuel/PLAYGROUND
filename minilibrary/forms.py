from django import forms
from .models import Review

BAD_WORDS = ["malo", "mugroso", "estupido", "wey", "todo wey", "gonorrea"]


class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Califica del 1 al 5',
            'class': 'form-control'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu reseña aquí...',
            'class': 'form-control',
            'rows': 4
        })
    )


class ReviewForm(forms.ModelForm):

    would_recommend = forms.BooleanField(
        label="¿Recomendarías este libro?", required=False)

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Calificación del 1 al 5',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Escribe tu reseña...',
                'class': 'form-control',
                'rows': 4
            })

        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "La calificación debe estar entre 1 y 5.")
        return rating

    def clean_text(self):
        text = self.cleaned_data.get('text')
        for palabra in BAD_WORDS:
            if palabra in text.lower():
                raise forms.ValidationError(
                    f"La reseña contiene una palabra prohíbida: {palabra}")
        return text

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get("rating")
        text = cleaned_data.get("text") or ''

        if rating == 1 and len(text) < 10:
            raise forms.ValidationError(
                "Si la califación es de 1 estrella, por favor explica mejor tu reseña")

    def save(self, commit=True):
        review = super().save(commit=False)
        # agregar lógica para would recommend

        if commit:
            review.save()

        return review
