from django import forms

from blogs.models import BlogPost


class StyleFormMixin:
    """ Применение стилей к форме """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class BlogPostForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'published']
