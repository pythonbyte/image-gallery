import datetime

from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Photo


class PhotoForm(forms.ModelForm):
    friends_name = forms.CharField(
        label="Image Name",
        widget=forms.TextInput(attrs={"class": "input-field col s12"}),
    )
    date_taken = forms.DateField(
        widget=forms.TextInput(
            attrs={"class": "datepicker", "type": "date", "placeholder": ""}
        )
    )

    def clean_friends_name(self):
        friends_name = self.cleaned_data["friends_name"]
        if friends_name.isnumeric():
            raise forms.ValidationError("Invalid name. Please provide a valid one.")
        return friends_name

    def clean_date_taken(self):
        date_taken = self.cleaned_data["date_taken"]
        if not isinstance(date_taken, datetime.date):
            raise forms.ValidationError("You need to provide a correct Date.")
        return date_taken

    def clean_image_file(self):
        image_file = self.cleaned_data["image_file"]
        if (
            not isinstance(image_file, InMemoryUploadedFile)
            or image_file.content_type != "image/jpeg"
        ):
            raise forms.ValidationError(
                "Incorrect type of image, only .JPG/.JPEG allowed."
            )
        return image_file

    class Meta:
        model = Photo
        fields = ["friends_name", "image_file", "date_taken"]
