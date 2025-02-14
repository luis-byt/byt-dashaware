from django import forms

from apps.core.widgets import (
    UnfoldAdminSelectWidget,
    UnfoldAdminTextInputWidget,
)


class SearchForm(forms.Form):
    def __init__(self, name, label, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[name] = forms.CharField(
            label=label,
            required=False,
            widget=UnfoldAdminTextInputWidget,
        )


class DropdownForm(forms.Form):
    def __init__(self, name, label, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[name] = forms.ChoiceField(
            label=label,
            required=False,
            choices=choices,
            widget=UnfoldAdminSelectWidget,
        )
