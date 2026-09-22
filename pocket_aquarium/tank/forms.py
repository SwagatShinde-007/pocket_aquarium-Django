from django import forms

from .models import Fish


class FishForm(forms.ModelForm):
    class Meta:
        model = Fish
        fields = ["name", "color", "size", "speed"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name your fish", "maxlength": 24, "autocomplete": "off"}),
            "color": forms.TextInput(attrs={"type": "color"}),
            "size": forms.NumberInput(attrs={"type": "range", "min": 60, "max": 180, "step": 5}),
            "speed": forms.NumberInput(attrs={"type": "range", "min": 6, "max": 40, "step": 1}),
        }

    def clean_color(self):
        color = self.cleaned_data["color"]
        if len(color) != 7 or not color.startswith("#"):
            raise forms.ValidationError("Pick a colour from the picker.")
        try:
            int(color[1:], 16)
        except ValueError:
            raise forms.ValidationError("Pick a colour from the picker.")
        return color
