from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, CrewRequestForm, VacancyFilterForm
from .models import Rank, Vacancy, VesselType


def home(request):
    return render(request, "crew/home.html", {
        "latest": Vacancy.objects.filter(is_active=True).select_related("rank", "vessel_type")[:3],
        "filter_form": VacancyFilterForm(),
        "vacancy_count": Vacancy.objects.filter(is_active=True).count(),
        "vessel_types": VesselType.objects.all(),
    })


def vacancy_list(request):
    form = VacancyFilterForm(request.GET or None)
    qs = Vacancy.objects.filter(is_active=True).select_related("rank", "vessel_type")
    if form.is_valid():
        d = form.cleaned_data
        if d["rank"]:
            qs = qs.filter(rank=d["rank"])
        if d["vessel_type"]:
            qs = qs.filter(vessel_type=d["vessel_type"])
        if d["min_salary"]:
            qs = qs.filter(salary_usd__gte=d["min_salary"])
    return render(request, "crew/vacancy_list.html", {"vacancies": qs, "form": form})


def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy.objects.select_related("rank", "vessel_type"), pk=pk, is_active=True)
    return render(request, "crew/vacancy_detail.html", {"vacancy": vacancy})


def apply(request):
    initial = {}
    vacancy = None
    vacancy_id = request.GET.get("vacancy") or request.POST.get("vacancy")
    if vacancy_id and vacancy_id.isdigit():
        vacancy = Vacancy.objects.filter(pk=vacancy_id, is_active=True).first()
        if vacancy:
            initial["rank"] = vacancy.rank_id
    form = ApplicationForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.vacancy = vacancy
        application.save()
        messages.success(request, "Заявка принята. Менеджер свяжется с вами в течение рабочего дня.")
        return redirect("apply")
    return render(request, "crew/apply.html", {"form": form, "vacancy": vacancy})


def shipowners(request):
    form = CrewRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Запрос получен. Мы подберём кандидатов и пришлём список.")
        return redirect("shipowners")
    return render(request, "crew/shipowners.html", {"form": form})
