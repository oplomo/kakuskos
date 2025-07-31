from django.shortcuts import render, get_object_or_404
from .models import Service, CaseStudy
from django.contrib import messages

# from .models import ESGResource


from django.shortcuts import render, redirect
from .forms import ServiceRequestForm

import logging

logger = logging.getLogger(__name__)


# Add this to the top of views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def update_chart_data(request):
    chart_type = request.POST.get("chart_type")

    # You would implement specific data fetching logic here
    # For now, we'll just return a success response
    return JsonResponse({"status": "success"})


def home(request):
    services = Service.objects.all()
    featured_cases = CaseStudy.objects.filter(featured_image__isnull=False)[:3]

    form = ServiceRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        # messages.success(
        #     request, "✅ Booking submitted successfully! We'll contact you shortly."
        # )
        return redirect("booking_success")  # You can add a success message later

    return render(
        request,
        "cust/index.html",
        {"services": services, "case_studies": featured_cases, "form": form},
    )


def booking_success(request):
    return render(request, "cust/booking_success.html")


def all_services(request):
    services = Service.objects.all()
    recent_projects = CaseStudy.objects.order_by("-installation_date")[:4]
    return render(
        request,
        "cust/services.html",
        {"services": services, "recent_projects": recent_projects},
    )


def case_study_detail(request, id):
    case = get_object_or_404(CaseStudy, pk=id)
    return render(request, "cust/case_detail.html", {"case": case})


# def esg_resources(request):
#     resources = ESGResource.objects.filter(is_featured=True)
#     return render(request, "cust/esg_resources.html", {"resources": resources})


def about(request):
    return render(request, "cust/about.html")


# power/views.py (add these views)
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import ServiceRequestForm
from .models import ServiceRequest, AdminLog


def contact(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, "Your request has been submitted successfully!"
                )
                return redirect("home")  # Redirect back to contact page to show message
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ServiceRequestForm()

    return render(request, "cust/contact.html", {"form": form})


# power/views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncYear, TruncMonth
from django.db.models import Sum, Count, Avg
from .models import InstallationProject, MonthlyMetric
import json


# power/views.py (update the analytics view)
# power/views.py
@staff_member_required
def business_analytics(request):
    yearly_data = (
        InstallationProject.objects.annotate(year=TruncYear("completion_date"))
        .values("year")
        .annotate(
            total_projects=Count("id"),
            total_profit=Sum("profit"),
            avg_system_size=Avg("system_size_kw"),
            total_revenue=Sum("total_cost"),
        )
        .order_by("year")
    )

    # Prepare yearly chart data
    yearly_labels = [
        str(item["year"].year) if item["year"] else "N/A" for item in yearly_data
    ]
    yearly_profit_data = [float(item["total_profit"] or 0) for item in yearly_data]
    yearly_clients_data = [item["total_projects"] or 0 for item in yearly_data]
    yearly_revenue_data = [float(item["total_revenue"] or 0) for item in yearly_data]

    # Monthly metrics (from MonthlyMetric model)
    monthly_metrics = MonthlyMetric.objects.order_by("-month")[:12][
        ::-1
    ]  # Last 12 months, oldest first
    monthly_labels = [item.month.strftime("%b %Y") for item in monthly_metrics]
    monthly_revenue_data = [float(item.revenue) for item in monthly_metrics]
    monthly_expenses_data = [float(item.expenses) for item in monthly_metrics]
    monthly_profit_data = [float(item.profit) for item in monthly_metrics]
    monthly_clients_data = [item.new_clients for item in monthly_metrics]

    # Service distribution
    service_distribution = (
        InstallationProject.objects.values("service_type__title")
        .annotate(count=Count("id"), total_profit=Sum("profit"))
        .order_by("-count")
    )
    service_labels = [item["service_type__title"] for item in service_distribution]
    service_data = [item["count"] for item in service_distribution]
    service_profit_data = [float(item["total_profit"]) for item in service_distribution]

    # Client types distribution
    case_study_distribution = (
        CaseStudy.objects.values("client_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    client_type_labels = [
        dict(CaseStudy.CLIENT_TYPES).get(item["client_type"], item["client_type"])
        for item in case_study_distribution
    ]
    client_type_data = [item["count"] for item in case_study_distribution]

    return render(
        request,
        "admin/analytics.html",
        {
            "yearly_labels": json.dumps(yearly_labels),
            "yearly_profit_data": json.dumps(yearly_profit_data),
            "yearly_clients_data": json.dumps(yearly_clients_data),
            "yearly_revenue_data": json.dumps(yearly_revenue_data),
            "monthly_labels": json.dumps(monthly_labels),
            "monthly_revenue_data": json.dumps(monthly_revenue_data),
            "monthly_expenses_data": json.dumps(monthly_expenses_data),
            "monthly_profit_data": json.dumps(monthly_profit_data),
            "monthly_clients_data": json.dumps(monthly_clients_data),
            "service_labels": json.dumps(service_labels),
            "service_data": json.dumps(service_data),
            "service_profit_data": json.dumps(service_profit_data),
            "client_type_labels": json.dumps(client_type_labels),
            "client_type_data": json.dumps(client_type_data),
        },
    )


def privacy_policy(request):
    return render(request, "cust/privacy_policy.html")


def terms_conditions(request):
    return render(request, "cust/terms_conditions.html")


def disclaimer(request):
    return render(request, "cust/disclaimer.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Service,
    CaseStudy,
    ServiceRequest,
    AdminLog,
    InstallationProject,
    MonthlyMetric,
)
from .forms import (
    ServiceForm,
    CaseStudyForm,
    InstallationProjectForm,
    MonthlyMetricForm,
)
from django.db.models import Count, Q, F, ExpressionWrapper, fields
from django.db.models.functions import TruncMonth, ExtractMonth
from datetime import datetime, timedelta
from django.utils import timezone


@login_required
def admin_dashboard(request):
    # Basic counts
    total_requests = ServiceRequest.objects.count()
    pending_requests = ServiceRequest.objects.filter(is_completed=False).count()
    recent_requests = ServiceRequest.objects.order_by("-submitted_at")[:5]
    admin_logs = AdminLog.objects.order_by("-timestamp")[:10]
    total_services = Service.objects.count()
    total_case_studies = CaseStudy.objects.count()
    active_projects = InstallationProject.objects.count()

    # Time periods for calculations
    current_month = timezone.now().month
    current_year = timezone.now().year
    last_month = timezone.now().replace(day=1) - timedelta(days=1)
    last_month_start = last_month.replace(day=1)

    # Service growth calculation
    services_this_month = Service.objects.filter(
        created_at__month=current_month, created_at__year=current_year
    ).count()
    services_last_month = Service.objects.filter(
        created_at__month=last_month.month, created_at__year=last_month.year
    ).count()
    service_growth = calculate_growth_rate(services_this_month, services_last_month)

    # Case study growth calculation
    case_studies_this_month = CaseStudy.objects.filter(
        installation_date__month=current_month, installation_date__year=current_year
    ).count()
    case_studies_last_month = CaseStudy.objects.filter(
        installation_date__month=last_month.month,
        installation_date__year=last_month.year,
    ).count()
    case_study_growth = calculate_growth_rate(
        case_studies_this_month, case_studies_last_month
    )

    # Project calculations
    new_projects_this_week = InstallationProject.objects.filter(
        completion_date__gte=timezone.now() - timedelta(days=7)
    ).count()

    # Request trend analysis
    completed_requests_this_month = ServiceRequest.objects.filter(
        is_completed=True,
        submitted_at__month=current_month,
        submitted_at__year=current_year,
    ).count()

    # Financial metrics (from InstallationProject)
    current_year_projects = InstallationProject.objects.filter(
        completion_date__year=current_year
    )
    total_revenue = (
        current_year_projects.aggregate(total=Sum("total_cost"))["total"] or 0
    )
    total_profit = current_year_projects.aggregate(total=Sum("profit"))["total"] or 0

    # Efficiency metrics
    avg_project_duration = current_year_projects.annotate(
        duration=ExpressionWrapper(
            F("completion_date") - F("created_at"), output_field=fields.DurationField()
        )
    ).aggregate(avg_duration=Avg("duration"))["avg_duration"] or timedelta(0)

    return render(
        request,
        "admin/dashboard.html",
        {
            # Basic counts
            "total_requests": total_requests,
            "pending_requests": pending_requests,
            "recent_requests": recent_requests,
            "admin_logs": admin_logs,
            "total_services": total_services,
            "total_case_studies": total_case_studies,
            "active_projects": active_projects,
            # Calculated metrics
            "service_growth": service_growth,
            "case_study_growth": case_study_growth,
            "new_projects_this_week": new_projects_this_week,
            "completed_requests_this_month": completed_requests_this_month,
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "avg_project_duration": avg_project_duration.days,
            # Time periods
            "current_month": timezone.now().strftime("%B"),
            "last_month": last_month.strftime("%B"),
        },
    )


def calculate_growth_rate(current, previous):
    """Calculate percentage growth rate between two values"""
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 1)


# Service Management Views
@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, "admin/service_list.html", {"services": services})


@login_required
def edit_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            AdminLog.objects.create(
                admin_user=request.user.username,
                action="EDIT",
                details=f"Edited service: {service.title}",
            )
            return redirect("service_list")
    else:
        form = ServiceForm(instance=service)

    return render(
        request, "admin/edit_service.html", {"form": form, "service": service}
    )


# Case Study Management Views
@login_required
def case_study_list(request):
    case_studies = CaseStudy.objects.all()
    return render(request, "admin/case_study_list.html", {"case_studies": case_studies})


@login_required
def add_case_study(request):
    if request.method == "POST":
        form = CaseStudyForm(request.POST, request.FILES)
        if form.is_valid():
            case_study = form.save()
            AdminLog.objects.create(
                admin_user=request.user.username,
                action="EDIT",
                details=f"Added case study: {case_study.title}",
            )
            return redirect("case_study_list")
    else:
        form = CaseStudyForm()

    return render(
        request, "admin/edit_case_study.html", {"form": form, "title": "Add Case Study"}
    )


@login_required
def edit_case_study(request, pk):
    case_study = get_object_or_404(CaseStudy, pk=pk)
    if request.method == "POST":
        form = CaseStudyForm(request.POST, request.FILES, instance=case_study)
        if form.is_valid():
            form.save()
            AdminLog.objects.create(
                admin_user=request.user.username,
                action="EDIT",
                details=f"Edited case study: {case_study.title}",
            )
            return redirect("case_study_list")
    else:
        form = CaseStudyForm(instance=case_study)

    return render(
        request,
        "admin/edit_case_study.html",
        {"form": form, "title": "Edit Case Study"},
    )


@login_required
def delete_case_study(request, pk):
    case_study = get_object_or_404(CaseStudy, pk=pk)
    if request.method == "POST":
        title = case_study.title
        case_study.delete()
        AdminLog.objects.create(
            admin_user=request.user.username,
            action="DELETE",
            details=f"Deleted case study: {title}",
        )
        return redirect("case_study_list")

    return render(
        request,
        "admin/confirm_delete.html",
        {"object": case_study, "type": "case study"},
    )


# Service Request Management
@login_required
def service_request_list(request):
    requests = ServiceRequest.objects.order_by("-submitted_at")
    return render(request, "admin/service_request_list.html", {"requests": requests})


@login_required
def mark_request_completed(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if not service_request.is_completed:
        service_request.is_completed = True
        service_request.save()
        AdminLog.objects.create(
            admin_user=request.user.username,
            action="EDIT",
            details=f"Marked request as completed: {service_request.name} - {service_request.get_service_display()}",
        )
    return redirect("service_request_list")


# Installation Project Views
@login_required
def project_list(request):
    # Get all projects ordered by completion date (newest first)
    projects = InstallationProject.objects.order_by("-completion_date")
    
    # Calculate totals and growth rates
    if projects.exists():
        current_year = timezone.now().year
        last_year = current_year - 1
        
        # Total calculations
        total_projects = projects.count()
        total_revenue = projects.aggregate(total=Sum('total_cost'))['total'] or 0
        total_profit = projects.aggregate(total=Sum('profit'))['total'] or 0
        
        # Current year projects
        current_year_projects = projects.filter(completion_date__year=current_year)
        current_year_count = current_year_projects.count()
        current_year_revenue = current_year_projects.aggregate(total=Sum('total_cost'))['total'] or 0
        current_year_profit = current_year_projects.aggregate(total=Sum('profit'))['total'] or 0
        
        # Last year projects (for growth comparison)
        last_year_projects = projects.filter(completion_date__year=last_year)
        last_year_count = last_year_projects.count()
        last_year_revenue = last_year_projects.aggregate(total=Sum('total_cost'))['total'] or 0
        last_year_profit = last_year_projects.aggregate(total=Sum('profit'))['total'] or 0
        
        # Growth rate calculations
        growth_rate = calculate_growth_rate(current_year_count, last_year_count)
        revenue_growth = calculate_growth_rate(current_year_revenue, last_year_revenue)
        profit_growth = calculate_growth_rate(current_year_profit, last_year_profit)
        
        # Add status and featured flags to each project
        for project in projects:
            project.status = 'completed'  # Default status since we only have completion_date
            project.is_featured = False  # Default to not featured
    else:
        total_projects = 0
        total_revenue = 0
        total_profit = 0
        growth_rate = 0
        revenue_growth = 0
        profit_growth = 0
    
    return render(request, "admin/project_list.html", {
        "projects": projects,
        "total_projects": total_projects,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "growth_rate": growth_rate,
        "revenue_growth": revenue_growth,
        "profit_growth": profit_growth,
    })

def calculate_growth_rate(current, previous):
    """Calculate percentage growth rate between two values"""
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 1)

@login_required
def add_project(request):
    if request.method == "POST":
        form = InstallationProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            AdminLog.objects.create(
                admin_user=request.user.username,
                action="EDIT",
                details=f"Added project: {project.client_name}",
            )
            return redirect("project_list")
    else:
        form = InstallationProjectForm()

    return render(
        request, "admin/edit_project.html", {"form": form, "title": "Add Project"}
    )


@login_required
def edit_project(request, pk):
    project = get_object_or_404(InstallationProject, pk=pk)
    if request.method == "POST":
        form = InstallationProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            AdminLog.objects.create(
                admin_user=request.user.username,
                action="EDIT",
                details=f"Edited project: {project.client_name}",
            )
            return redirect("project_list")
    else:
        form = InstallationProjectForm(instance=project)

    return render(
        request, "admin/edit_project.html", {"form": form, "title": "Edit Project"}
    )


@login_required
def monthly_metrics(request):
    # Get all metrics ordered by month (newest first)
    metrics = MonthlyMetric.objects.order_by("-month")
    
    # Calculate totals and growth rates
    if metrics.exists():
        current_month = metrics.first()
        previous_month = metrics[1] if len(metrics) > 1 else None
        
        # Total calculations
        total_revenue = sum(m.revenue for m in metrics)
        total_profit = sum(m.profit for m in metrics)
        total_clients = sum(m.new_clients for m in metrics)
        
        # Growth rate calculations
        revenue_growth = calculate_growth_rate(
            current_month.revenue,
            previous_month.revenue if previous_month else 0
        )
        
        profit_growth = calculate_growth_rate(
            current_month.profit,
            previous_month.profit if previous_month else 0
        )
        
        client_growth = calculate_growth_rate(
            current_month.new_clients,
            previous_month.new_clients if previous_month else 0
        )
        
        # Add profit margin to each metric
        for metric in metrics:
            metric.profit_margin = (metric.profit / metric.revenue * 100) if metric.revenue != 0 else 0
    else:
        total_revenue = 0
        total_profit = 0
        total_clients = 0
        revenue_growth = 0
        profit_growth = 0
        client_growth = 0
    
    return render(request, "admin/monthly_metrics.html", {
        "metrics": metrics,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_clients": total_clients,
        "revenue_growth": revenue_growth,
        "profit_growth": profit_growth,
        "client_growth": client_growth,
    })

def calculate_growth_rate(current, previous):
    """Calculate percentage growth rate between two values"""
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 1)


@login_required
def add_monthly_metric(request):
    if request.method == "POST":
        form = MonthlyMetricForm(request.POST)
        if form.is_valid():
            metric = form.save()
            AdminLog.objects.create(
                admin_user=request.user.username,
                action="EDIT",
                details=f"Added monthly metric for {metric.month.strftime('%B %Y')}",
            )
            return redirect("monthly_metrics")
    else:
        form = MonthlyMetricForm()

    return render(
        request, "admin/edit_metric.html", {"form": form, "title": "Add Monthly Metric"}
    )
