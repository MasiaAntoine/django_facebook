from django import forms
from .models import Post


class PostForm(forms.ModelForm):
	images = forms.FileField(
		widget=forms.ClearableFileInput(),
		required=False
	)

	class Meta:
		model = Post
		fields = ['title', 'description', 'category', 'images']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
