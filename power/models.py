from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Service(models.Model):
    """Represents our 5 signature service pillars"""

    SERVICE_CHOICES = [
        ("SEA", "Smart Energy Assessment"),
        ("CSE", "Custom Solar & Efficiency Plan"),
        ("SER", "Sustainability & ESG Roadmap"),
        ("REC", "Remote Energy Coaching"),
        ("IS", "Installation & Supervision"),
    ]

    # Key identifier for URLs
    slug = models.SlugField(max_length=50, unique=True)

    # Choice field using our predefined options
    service_type = models.CharField(max_length=3, choices=SERVICE_CHOICES, unique=True)

    # Display title
    title = models.CharField(max_length=100)

    # Detailed description
    description = models.TextField()

    # What makes this service unique
    value_proposition = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True, null=True)

    # FontAwesome icon class
    icon_class = models.CharField(max_length=30, default="fas fa-solar-panel")

    # Ordering field for display sequence
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title


class CaseStudy(models.Model):
    """Showcases real client installations and results"""

    CLIENT_TYPES = [
        ("RES", "Residential"),
        ("COM", "Commercial"),
        ("IND", "Industrial"),
    ]

    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=100, blank=True)
    client_type = models.CharField(max_length=3, choices=CLIENT_TYPES)

    # Location details
    location = models.CharField(max_length=100)
    installation_date = models.DateField()

    # System details
    system_capacity = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="System size in kW"
    )

    # Financial metrics
    project_cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Energy metrics (in kWh)
    previous_consumption = models.PositiveIntegerField(
        help_text="Monthly consumption before installation"
    )
    current_consumption = models.PositiveIntegerField(
        help_text="Monthly consumption after installation"
    )

    # Client testimonial
    testimonial = models.TextField(blank=True)

    # Service this case study relates to
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="case_studies"
    )

    # Image for display
    featured_image = models.ImageField(upload_to="case_studies/", blank=True)

    def energy_savings(self):
        """Safely calculate monthly energy savings in kWh"""
        if (
            self.previous_consumption is not None
            and self.current_consumption is not None
        ):
            return self.previous_consumption - self.current_consumption
        return 0  # Or return None if you'd prefer that

    def savings_percentage(self):
        """Safely calculate percentage savings"""
        if self.previous_consumption and self.energy_savings() is not None:
            return (self.energy_savings() / self.previous_consumption) * 100
        return 0  # Or return None

    def __str__(self):
        return f"{self.title} - {self.get_client_type_display()}"


# class ESGResource(models.Model):
#     """Educational materials for sustainability"""

#     RESOURCE_TYPES = [
#         ("GUIDE", "Guide"),
#         ("REPORT", "Industry Report"),
#         ("CASE", "Case Study"),
#         ("TOOL", "Tool/Template"),
#     ]

#     title = models.CharField(max_length=200)
#     resource_type = models.CharField(max_length=8, choices=RESOURCE_TYPES)
#     description = models.TextField()
#     file = models.FileField(upload_to="esg_resources/")
#     published_date = models.DateField(auto_now_add=True)
#     is_featured = models.BooleanField(default=False)

#     class Meta:
#         ordering = ["-published_date"]

#     def __str__(self):
#         return f"{self.get_resource_type_display()}: {self.title}"

#     # power/models.py (add these models)


from django.db import models
from django.utils import timezone


class ServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ("SEA", "Smart Energy Assessment"),
        ("CSE", "Custom Solar & Efficiency Plan"),
        ("SER", "Sustainability & ESG Roadmap"),
        ("REC", "Remote Energy Coaching"),
        ("IS", "Installation & Supervision"),
        ("OTH", "Other"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=3, choices=SERVICE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_service_display()}"


class AdminLog(models.Model):
    ACTION_CHOICES = [
        ("LOGIN", "Admin Login"),
        ("EDIT", "Content Edit"),
        ("DELETE", "Content Deletion"),
        ("CONFIG", "Configuration Change"),
    ]

    admin_user = models.CharField(max_length=100)
    action = models.CharField(max_length=6, choices=ACTION_CHOICES)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.admin_user} - {self.get_action_display()}"


# power/models.py
from django.db import models


class InstallationProject(models.Model):
    client_name = models.CharField(max_length=100)
    completion_date = models.DateField()
    system_size_kw = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.ForeignKey("Service", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def year(self):
        return self.completion_date.year


class MonthlyMetric(models.Model):
    month = models.DateField(unique=True)  # First day of month
    new_clients = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    expenses = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def profit(self):
        return self.revenue - self.expenses
