import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from crew.models import Department, Rank, Vacancy, VesselKind, VesselType


class Command(BaseCommand):
    help = "Заполняет базу демонстрационными должностями, типами судов и вакансиями"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Удалить старые вакансии и создать заново")

    def handle(self, *args, **options):
        K = VesselKind
        types = {}
        for name, kind in [
            ("Контейнеровоз", K.CONTAINER), ("Балкер", K.BULK),
            ("Танкер-нефтевоз", K.TANKER_OIL), ("Танкер-химовоз", K.TANKER_CHEM),
            ("Газовоз (LPG)", K.LPG), ("Генгруз", K.GENERAL), ("Ро-ро / паромы", K.RORO),
        ]:
            obj, _ = VesselType.objects.get_or_create(name=name)
            obj.kind = kind
            obj.save()
            types[name] = obj

        D = Department
        ranks = {}
        for name, dep in [
            ("Капитан", D.DECK), ("Старший помощник", D.DECK), ("Второй помощник", D.DECK),
            ("Третий помощник", D.DECK), ("Боцман", D.DECK), ("Матрос 1 класса", D.DECK),
            ("Старший механик", D.ENGINE), ("Второй механик", D.ENGINE), ("Третий механик", D.ENGINE),
            ("Моторист", D.ENGINE), ("Электромеханик", D.ELECTRO),
            ("Повар", D.GALLEY), ("Стюард", D.GALLEY),
        ]:
            ranks[name] = Rank.objects.get_or_create(name=name, defaults={"department": dep})[0]

        if Vacancy.objects.exists():
            if not options["force"]:
                self.stdout.write("Вакансии уже есть — пропускаю (запустите с --force, чтобы пересоздать).")
                return
            Vacancy.objects.all().delete()

        random.seed(7)
        ships = {
            "Контейнеровоз": ["MSC Aurora", "Maersk Elba", "CMA CGM Rhône", "Hapag Nordland", ""],
            "Балкер": ["Cape Horizon", "Pacific Grain", "Iron Voyager", ""],
            "Танкер-нефтевоз": ["Atlas Spirit", "Black Sea Crown", "Aegean Dawn", ""],
            "Танкер-химовоз": ["Nordic Pearl", "Chem Orion", "Baltic Amber", ""],
            "Газовоз (LPG)": ["Gas Polaris", "LPG Adriatic", ""],
            "Генгруз": ["Baltic Star", "Danube Trader", "Lisa B", ""],
            "Ро-ро / паромы": ["Aegean Link", "Adria Express", ""],
        }
        flags = ["Либерия", "Мальта", "Панама", "Маршалловы о-ва", "Багамы", "Кипр", "Антигуа и Барбуда"]
        ports = ["Одесса", "Роттердам", "Гамбург", "Констанца", "Пирей", "Сингапур", "Антверпен",
                 "Валенсия", "Стамбул", "Дубай", "Генуя", "Гданьск"]
        # (должность, типы судов, оклад от, оклад до, опыт, контракт мес.)
        spec = [
            ("Капитан", ["Контейнеровоз", "Балкер", "Танкер-нефтевоз", "Ро-ро / паромы"], 8500, 12500, 5, (3, 4)),
            ("Старший помощник", ["Контейнеровоз", "Танкер-химовоз", "Газовоз (LPG)", "Генгруз"], 5800, 7600, 3, (4, 4)),
            ("Второй помощник", ["Балкер", "Танкер-нефтевоз", "Контейнеровоз"], 3900, 5200, 2, (4, 6)),
            ("Третий помощник", ["Контейнеровоз", "Генгруз", "Ро-ро / паромы"], 2900, 3600, 0, (6, 6)),
            ("Боцман", ["Генгруз", "Балкер", "Контейнеровоз"], 2700, 3300, 4, (6, 8)),
            ("Матрос 1 класса", ["Танкер-химовоз", "Балкер", "Ро-ро / паромы"], 1800, 2400, 1, (6, 8)),
            ("Старший механик", ["Танкер-нефтевоз", "Контейнеровоз", "Газовоз (LPG)"], 9000, 12000, 5, (3, 4)),
            ("Второй механик", ["Балкер", "Танкер-химовоз", "Контейнеровоз"], 5600, 7400, 3, (4, 6)),
            ("Третий механик", ["Генгруз", "Балкер", "Ро-ро / паромы"], 3600, 4600, 1, (6, 6)),
            ("Моторист", ["Контейнеровоз", "Танкер-нефтевоз", "Генгруз"], 1900, 2600, 1, (6, 8)),
            ("Электромеханик", ["Газовоз (LPG)", "Контейнеровоз", "Танкер-химовоз"], 4300, 5600, 2, (5, 6)),
            ("Повар", ["Ро-ро / паромы", "Балкер", "Танкер-нефтевоз"], 2100, 2900, 2, (6, 8)),
            ("Стюард", ["Контейнеровоз", "Газовоз (LPG)"], 1700, 2200, 0, (6, 8)),
        ]
        extra = {
            "Танкер-нефтевоз": " Обязателен допуск на нефтяные танкеры (Oil Tanker Familiarization).",
            "Танкер-химовоз": " Обязателен допуск на химовозы (Chemical Tanker Familiarization).",
            "Газовоз (LPG)": " Обязателен допуск на газовозы (Liquefied Gas Tanker Familiarization).",
        }
        today = date.today()
        count = 0
        for rank, tnames, lo, hi, exp, (m1, m2) in spec:
            for tn in tnames:
                for _ in range(1 if rank in ("Капитан", "Старший механик") else 2):
                    if count >= 36:
                        break
                    Vacancy.objects.create(
                        rank=ranks[rank], vessel_type=types[tn],
                        vessel_name=random.choice(ships[tn]), flag=random.choice(flags),
                        salary_usd=round(random.randint(lo, hi), -2),
                        contract_months=random.randint(m1, m2),
                        joining_port=random.choice(ports),
                        joining_date=today + timedelta(days=random.randint(5, 60)),
                        min_experience=exp,
                        requirements="Действующие дипломы и сертификаты по STCW, медицинское заключение, "
                                     "виза по требованию порта. Рабочий английский язык." + extra.get(tn, ""),
                    )
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"Создано вакансий: {count}"))
