# power/forms.py
from django import forms
from django.core.validators import RegexValidator
from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(07\d{8}|01\d{8}|\+254\d{9})$",
                message="Enter a valid Kenyan phone number (e.g. 07XXXXXXXX, 01XXXXXXXX, or +254XXXXXXXXX)",
            )
        ],
    )

    class Meta:
        model = ServiceRequest
        fields = ["name", "email", "phone", "service", "message"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set required fields
        self.fields["name"].required = True
        self.fields["email"].required = True
        self.fields["phone"].required = True
        self.fields["service"].required = True

        # Add HTML5 validation attributes
        self.fields["name"].widget.attrs.update(
            {
                "minlength": "2",
                "maxlength": "100",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "type": "email",
            }
        )
        self.fields["phone"].widget.attrs.update(
            {
                "pattern": r"^(07\d{8}|01\d{8}|\+254\d{9})$",
                "title": "Kenyan phone number (07XXXXXXXX, 01XXXXXXXX, or +254XXXXXXXXX)",
            }
        )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long")
        return name.strip()

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if len(message.strip()) < 5:
            raise forms.ValidationError("Please provide more details in your message")
        return message.strip()



from django import forms
from .models import Service, CaseStudy, InstallationProject, MonthlyMetric

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = '__all__'

class InstallationProjectForm(forms.ModelForm):
    class Meta:
        model = InstallationProject
        fields = '__all__'
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MonthlyMetricForm(forms.ModelForm):
    class Meta:
        model = MonthlyMetric
        fields = '__all__'
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }