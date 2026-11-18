from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Department(models.TextChoices):
    DECK = "deck", "Палубная команда"
    ENGINE = "engine", "Машинная команда"
    GALLEY = "galley", "Камбуз и сервис"
    ELECTRO = "electro", "Электрики"


class VesselKind(models.TextChoices):
    CONTAINER = "container", "Контейнеровоз"
    BULK = "bulk", "Балкер"
    TANKER_OIL = "tanker_oil", "Нефтевоз"
    TANKER_CHEM = "tanker_chem", "Химовоз"
    LPG = "lpg", "Газовоз"
    GENERAL = "general", "Генгруз"
    RORO = "roro", "Ро-ро / паром"


class VesselType(models.Model):
    name = models.CharField("Тип судна", max_length=80, unique=True)
    kind = models.CharField("Иллюстрация", max_length=12, choices=VesselKind.choices,
                            default=VesselKind.GENERAL, help_text="Какая картинка показывается у вакансий этого типа")

    class Meta:
        verbose_name = "тип судна"
        verbose_name_plural = "типы судов"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Rank(models.Model):
    name = models.CharField("Должность", max_length=80, unique=True)
    department = models.CharField("Служба", max_length=10, choices=Department.choices)

    class Meta:
        verbose_name = "должность"
        verbose_name_plural = "должности"
        ordering = ["department", "name"]

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT, verbose_name="Должность", related_name="vacancies")
    vessel_type = models.ForeignKey(VesselType, on_delete=models.PROTECT, verbose_name="Тип судна", related_name="vacancies")
    vessel_name = models.CharField("Название судна", max_length=100, blank=True)
    flag = models.CharField("Флаг", max_length=60, blank=True)
    salary_usd = models.PositiveIntegerField("Оклад, USD / мес.")
    contract_months = models.PositiveSmallIntegerField("Контракт, мес.", default=6)
    joining_port = models.CharField("Порт посадки", max_length=100)
    joining_date = models.DateField("Дата посадки")
    min_experience = models.PositiveSmallIntegerField("Мин. опыт в должности, лет", default=0)
    requirements = models.TextField("Требования", blank=True)
    photo = models.ImageField("Своё фото судна", upload_to="vessels/", blank=True,
                              help_text="Необязательно. Если не загружено — берётся иллюстрация по типу судна")
    is_active = models.BooleanField("Открыта", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"
        ordering = ["joining_date"]

    def __str__(self):
        return f"{self.rank} — {self.vessel_type}"

    def get_absolute_url(self):
        return reverse("vacancy_detail", args=[self.pk])

    @property
    def image_url(self):
        if self.photo:
            return self.photo.url
        return static(f"img/{self.vessel_type.kind}.svg")


class Application(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="Вакансия", related_name="applications")
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT, verbose_name="Должность")
    full_name = models.CharField("ФИО", max_length=150)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=30)
    experience_years = models.PositiveSmallIntegerField("Опыт в должности, лет", default=0)
    certificates = models.TextField("Дипломы и сертификаты", blank=True,
                                    help_text="Например: ДОПОГ, BST, GMDSS, медсправка")
    cv = models.FileField("Резюме", upload_to="cv/", blank=True)
    message = models.TextField("Комментарий", blank=True)
    processed = models.BooleanField("Обработана", default=False)
    created_at = models.DateTimeField("Получена", auto_now_add=True)

    class Meta:
        verbose_name = "заявка моряка"
        verbose_name_plural = "заявки моряков"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.rank})"


class CrewRequest(models.Model):
    company = models.CharField("Компания / судовладелец", max_length=150)
    contact_person = models.CharField("Контактное лицо", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=30, blank=True)
    vessel_type = models.ForeignKey(VesselType, on_delete=models.PROTECT, verbose_name="Тип судна")
    crew_needed = models.TextField("Какой экипаж нужен", help_text="Должности, количество, сроки")
    processed = models.BooleanField("Обработан", default=False)
    created_at = models.DateTimeField("Получен", auto_now_add=True)

    class Meta:
        verbose_name = "запрос судовладельца"
        verbose_name_plural = "запросы судовладельцев"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.company} — {self.vessel_type}"
