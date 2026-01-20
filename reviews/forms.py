from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_rating(self):
        r = int(self.cleaned_data.get('rating') or 0)
        if r < 1 or r > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return r

    def clean_comment(self):
        c = (self.cleaned_data.get('comment') or '').strip()
        if len(c) < 10:
            raise forms.ValidationError('Please write at least 10 characters.')
        return c
