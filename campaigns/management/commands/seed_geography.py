"""
Management command to seed all PNG provinces and districts.
Usage: python manage.py seed_geography
       python manage.py seed_geography --clear   (wipe and re-seed)
"""
from django.core.management.base import BaseCommand
from campaigns.models import Province, District

PNG_DATA = {
    "National Capital District": [
        "NCD",
    ],
    "Central Province": [
        "Abau",
        "Goilala",
        "Kairuku-Hiri",
        "Rigo",
    ],
    "Gulf Province": [
        "Kerema",
        "Kikori",
    ],
    "Western Province": [
        "Fly River",
        "Middle Fly",
        "North Fly",
        "South Fly",
    ],
    "Milne Bay Province": [
        "Alotau",
        "Esa'ala",
        "Kiriwina-Goodenough",
        "Samarai-Murua",
    ],
    "Oro (Northern) Province": [
        "Ijivitari",
        "Sohe",
    ],
    "Southern Highlands Province": [
        "Ialibu-Pangia",
        "Imbonggu",
        "Kagua-Erave",
        "Mendi-Munihu",
        "Nipa-Kutubu",
    ],
    "Hela Province": [
        "Komo-Margarima",
        "Koroba-Lake Kopiago",
        "Tari-Pori",
    ],
    "Enga Province": [
        "Kandep",
        "Kompiam-Ambum",
        "Lagaip-Porgera",
        "Wabag",
        "Wapenamanda",
    ],
    "Western Highlands Province": [
        "Dei",
        "Hagen",
        "Mul-Baiyer",
        "Tambul-Nebilyer",
    ],
    "Jiwaka Province": [
        "Anglimp-South Waghi",
        "Jimi",
        "North Waghi",
    ],
    "Simbu (Chimbu) Province": [
        "Chuave",
        "Gumine",
        "Karimui-Nomane",
        "Kerowagi",
        "Kundiawa-Gembogl",
        "Salt-Nomane",
    ],
    "Eastern Highlands Province": [
        "Daulo",
        "Goroka",
        "Henganofi",
        "Kainantu",
        "Lufa",
        "Obura-Wonenara",
        "Okapa",
        "Unggai-Bena",
    ],
    "Morobe Province": [
        "Bulolo",
        "Finschhafen",
        "Huon Gulf",
        "Kabwum",
        "Lae",
        "Markham",
        "Menyamya",
        "Nawae",
        "Tewai-Siassi",
    ],
    "Madang Province": [
        "Bogia",
        "Madang",
        "Middle Ramu",
        "Rai Coast",
        "Sumkar",
        "Usino-Bundi",
    ],
    "East Sepik Province": [
        "Ambunti-Dreikikir",
        "Angoram",
        "Maprik",
        "Wewak",
        "Wosera-Gawi",
        "Yangoru-Saussia",
    ],
    "Sandaun (West Sepik) Province": [
        "Amanab",
        "Nuku",
        "Telefomin",
        "Vanimo-Green River",
        "Mianmin-Magi",
        "Aitape-Lumi",
        "Maimai-Yangoru",
    ],
    "Manus Province": [
        "Manus",
    ],
    "New Ireland Province": [
        "Kavieng",
        "Namatanai",
    ],
    "East New Britain Province": [
        "Gazelle",
        "Kokopo",
        "Pomio",
        "Rabaul",
    ],
    "West New Britain Province": [
        "Kandrian-Gloucester",
        "Talasea",
    ],
    "Autonomous Region of Bougainville": [
        "Buin",
        "Buka",
        "Atolls",
        "Central Bougainville",
        "North Bougainville",
        "South Bougainville",
    ],
}


class Command(BaseCommand):
    help = "Seed PNG provinces and districts into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing provinces and districts before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            District.objects.all().delete()
            Province.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared all existing province/district data."))

        provinces_created = 0
        districts_created = 0
        provinces_skipped = 0
        districts_skipped = 0

        for province_name, districts in PNG_DATA.items():
            province, created = Province.objects.get_or_create(name=province_name)
            if created:
                provinces_created += 1
                self.stdout.write(f"  + Province: {province_name}")
            else:
                provinces_skipped += 1

            for district_name in districts:
                _, d_created = District.objects.get_or_create(
                    province=province,
                    name=district_name,
                )
                if d_created:
                    districts_created += 1
                else:
                    districts_skipped += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. "
            f"{provinces_created} provinces created ({provinces_skipped} already existed). "
            f"{districts_created} districts created ({districts_skipped} already existed)."
        ))
