from django import forms
from .models import Application, CrewRequest, Rank, VesselType


class VacancyFilterForm(forms.Form):
    rank = forms.ModelChoiceField(Rank.objects.all(), required=False, empty_label="Любая должность", label="Должность")
    vessel_type = forms.ModelChoiceField(VesselType.objects.all(), required=False, empty_label="Любой тип судна", label="Тип судна")
    min_salary = forms.IntegerField(required=False, min_value=0, label="Оклад от, USD",
                                    widget=forms.NumberInput(attrs={"placeholder": "например, 3000"}))


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["rank", "full_name", "email", "phone", "experience_years", "certificates", "cv", "message"]
        widgets = {
            "certificates": forms.Textarea(attrs={"rows": 3}),
            "message": forms.Textarea(attrs={"rows": 3}),
        }


class CrewRequestForm(forms.ModelForm):
    class Meta:
        model = CrewRequest
        fields = ["company", "contact_person", "email", "phone", "vessel_type", "crew_needed"]
        widgets = {"crew_needed": forms.Textarea(attrs={"rows": 4})}
