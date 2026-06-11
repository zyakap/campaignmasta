from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Candidate, District, Province, Role, TeamMember


class CampaignRulesTests(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Eastern Highlands")
        self.district = District.objects.create(province=self.province, name="Kainantu Open")

    def test_district_open_requires_district(self):
        candidate = Candidate(name="Open Race", candidate_type="DISTRICT_OPEN", province=self.province)
        with self.assertRaises(ValidationError):
            candidate.full_clean()

    def test_provincial_rejects_single_district_boundary(self):
        candidate = Candidate(name="Governor Race", candidate_type="PROVINCIAL", province=self.province, district=self.district)
        with self.assertRaises(ValidationError):
            candidate.full_clean()

    def test_district_coordinator_only_for_provincial_campaign(self):
        candidate = Candidate.objects.create(name="Open Race", candidate_type="DISTRICT_OPEN", province=self.province, district=self.district)
        member = TeamMember(candidate=candidate, full_name="Blocked Role", role=Role.DISTRICT_COORDINATOR, province=self.province, district=self.district)
        with self.assertRaises(ValidationError):
            member.full_clean()


class MobileViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass12345")
        self.province = Province.objects.create(name="Morobe")
        self.candidate = Candidate.objects.create(name="Morobe Governor", candidate_type="PROVINCIAL", province=self.province)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_authenticated_user(self):
        self.client.login(username="tester", password="pass12345")
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Morobe Governor")
        self.assertContains(response, "Register")
