from io import TextIOWrapper

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from course.models import BrandName, MarketId, Profile, Store, StoreNumber, TerminalId


# creating a form
class StoreForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = Store

        # specify fields to be used
        fields = [
            "brand_name",
            "market_id",
            "store_number",
            "terminal_id",
            "uploaded_file",
        ]

        def __init__(self, *args, **kwargs):

            super(StoreForm, self).__init__(*args, **kwargs)
            self.fields["market_id"] = forms.ModelChoiceField(
                queryset=Store.objects.filter(market_id__isnull=False)
            )
            self.fields["store_number"] = forms.ModelChoiceField(
                queryset=Store.objects.filter(store_number__isnull=False)
            )
            self.fields["terminal_id"] = forms.ModelChoiceField(
                queryset=Store.objects.filter(terminal_id__isnull=False)
            )

        def clean_myfilefield1(self):
            my_file = self.cleaned_data["uploaded_file"]
            read_file = TextIOWrapper(my_file.file, encoding="ASCII")

            read_file.detach()

        def clean_myfilefield2(self):
            my_file = self.cleaned_data["converted_file"]
            read_file = TextIOWrapper(my_file.file, encoding="ASCII")

            read_file.detach()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "image",
        ]


class StoreNumberForm(forms.ModelForm):
    class Meta:
        model = StoreNumber
        fields = [
            "store_number",
        ]

    def clean_store_number(self):
        store_number = self.cleaned_data.get("store_number")
        if len(store_number) != 4:
            raise forms.ValidationError("Store number must be 4 digits")
        return store_number


class MarketIdForm(forms.ModelForm):
    class Meta:
        model = MarketId
        fields = [
            "market_id",
        ]

    def clean_market_id(self):
        market_id = self.cleaned_data.get("market_id")
        if len(market_id) != 6:
            raise forms.ValidationError("Market ID must be 6 digits")
        return market_id


class TerminalIdForm(forms.ModelForm):
    class Meta:
        model = TerminalId
        fields = [
            "terminal_id",
        ]

    def clean_terminal_id(self):
        terminal_id = self.cleaned_data.get("terminal_id")
        if len(terminal_id) != 3:
            raise forms.ValidationError("Terminal ID must be 3 digits")
        return terminal_id


class BrandNameForm(forms.ModelForm):
    class Meta:
        model = BrandName
        fields = [
            "brand_name",
        ]
