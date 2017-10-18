from django import forms


class PostForm(forms.Form):
    photo = forms.ImageField()
    # text를 받을 수 있는 필드 추가
    # text = forms.CharField(max_length=5)

    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     if data != data.upper():
    #         raise forms.ValidationError('All text must uppercase!')
    #     return data


class PostCommentForm(forms.Form):
    text = forms.CharField(
        label='댓글',
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )
