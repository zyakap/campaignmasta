from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Candidate, CandidateType, District, Province, Role, TeamMember


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
        # The user must have an active team role in the candidate to see its dashboard.
        TeamMember.objects.create(
            candidate=self.candidate,
            user=self.user,
            full_name="Tester",
            role=Role.CAMPAIGN_MANAGER,
            province=self.province,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_authenticated_user(self):
        self.client.login(username="tester", password="pass12345")
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Morobe Governor")
        self.assertContains(response, "Register")


class TenantIsolationTests(TestCase):
    """A non-superuser must never resolve to a candidate they have no role in."""

    def setUp(self):
        User = get_user_model()
        self.province = Province.objects.create(name="Enga")
        self.candidate_a = Candidate.objects.create(name="Candidate A", candidate_type="PROVINCIAL", province=self.province)
        self.candidate_b = Candidate.objects.create(name="Candidate B", candidate_type="PROVINCIAL", province=self.province)
        self.outsider = User.objects.create_user(username="outsider", password="pass12345")
        self.member_b_user = User.objects.create_user(username="member_b", password="pass12345")
        TeamMember.objects.create(
            candidate=self.candidate_b,
            user=self.member_b_user,
            full_name="Member B",
            role=Role.WARD_COORDINATOR,
            province=self.province,
        )

    def test_outsider_sees_no_candidate(self):
        self.client.login(username="outsider", password="pass12345")
        response = self.client.get(reverse("dashboard"))
        self.assertNotContains(response, "Candidate A")
        self.assertNotContains(response, "Candidate B")

    def test_member_cannot_hijack_other_tenant_via_session(self):
        self.client.login(username="member_b", password="pass12345")
        session = self.client.session
        session["candidate_id"] = self.candidate_a.id  # attempt to reach another tenant
        session.save()
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Candidate B")
        self.assertNotContains(response, "Candidate A")
