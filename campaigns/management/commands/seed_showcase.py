"""
Seed two extensive demo candidate accounts that exercise every feature:

  * one PROVINCIAL candidate (Enga Provincial / Governor) — full chain incl. District Coordinators
  * one DISTRICT OPEN candidate (Kainantu Open) — no District Coordinator layer

Every role gets a representative login with a role-based username and the shared
password ``demo12345``. Supporters are registered at every level so the incentive
leaderboard is populated, and the full feature set (calls, messages, events,
polling, AI drafts, PNG-specific modules, constituency, approvals) is seeded.

Re-running is safe: the two demo candidates and their ``prov-*`` / ``dist-*``
logins are removed and rebuilt fresh each time.
"""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from campaigns.models import (
    AIWorkItem, ApprovalStatus, CampaignEvent, CampaignTask, Candidate,
    CandidateProfile, CitizenRequest, CommunityAssistance, CommunityGroup,
    CommunityIssue, CompetitorActivity, ConnectorSetting, DevelopmentFund,
    District, EventAttendance, EventChecklistItem, Influencer, IncludedUsageQuota,
    Landmark, LLG, Message, MessageRecipient, ModuleBundle, ModulePrice,
    PollingIncident, PollingLocation, PollingStatus, PreferenceDeal,
    PromiseTracker, Province, RegistrationDrive, Role, SoftwareModule,
    Subscription, Supporter, TeamMember, TenantModuleSubscription, TenantSettings,
    UsageRateCard, UsageTopUp, UsageWallet, Village, Ward, WardProfile,
)
from campaigns.services import (
    create_speech_ai_work_item, create_ward_ai_work_item,
    provision_included_quotas, provision_team_member_login,
    supporter_attribution_fields,
)

PASSWORD = "demo12345"

FIRST = ["John", "Mary", "Peter", "Anna", "Joseph", "Ruth", "Paul", "Grace",
         "Michael", "Lucy", "Samuel", "Esther", "David", "Rebecca", "Daniel",
         "Margaret", "Thomas", "Susan", "James", "Dorothy", "Philip", "Janet",
         "Andrew", "Helen", "Francis", "Agnes", "Simon", "Naomi", "Robert", "Joyce"]
SUR = ["Kila", "Wapi", "Tongia", "Mendi", "Yaki", "Pora", "Namaliu", "Agarobe",
       "Kalo", "Hagen", "Sai", "Kup", "Pomio", "Bani", "Lus", "Tau", "Gima",
       "Oala", "Wari", "Konga", "Sapu", "Mond", "Pundia", "Lakane"]

GEO_PROV = {
    "province": "Enga Province",
    "districts": [
        {"name": "Wabag Open", "llgs": [
            {"name": "Wabag Urban LLG", "wards": [
                {"name": "Ward 1", "number": "1", "villages": ["Kumbasaka", "Tilyapo"]},
                {"name": "Ward 2", "number": "2", "villages": ["Lakolam", "Pina"]},
            ]},
        ]},
        {"name": "Wapenamanda Open", "llgs": [
            {"name": "Wapenamanda Rural LLG", "wards": [
                {"name": "Ward 9", "number": "9", "villages": ["Sakarip", "Pumakos"]},
            ]},
        ]},
        {"name": "Kompiam-Ambum Open", "llgs": [
            {"name": "Ambum Rural LLG", "wards": [
                {"name": "Ward 4", "number": "4", "villages": ["Monokam", "Yenkisa"]},
            ]},
        ]},
    ],
}

GEO_DIST = {
    "province": "Eastern Highlands Province",
    "districts": [
        {"name": "Kainantu Open", "llgs": [
            {"name": "Kainantu Urban LLG", "wards": [
                {"name": "Ward 1", "number": "1", "villages": ["Ontenu", "Kumpara"]},
                {"name": "Ward 2", "number": "2", "villages": ["Barola", "Aiyura"]},
            ]},
            {"name": "Gadsup Tairora Rural LLG", "wards": [
                {"name": "Ward 7", "number": "7", "villages": ["Tompena", "Norikori"]},
            ]},
        ]},
    ],
}


class Command(BaseCommand):
    help = "Seed two extensive demo candidates (Provincial + District Open) showcasing every feature."

    def handle(self, *args, **options):
        self.User = get_user_model()
        self._name_i = 0
        self.admin, _ = self.User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@campaignmasta.local", "is_staff": True, "is_superuser": True},
        )
        self.admin.is_staff = self.admin.is_superuser = True
        self.admin.set_password("admin12345")
        self.admin.save()

        modules, bundles = self._ensure_catalog()

        # Clean previous demo runs so the data is always fresh and consistent.
        Candidate.objects.filter(name__in=["Enga Provincial Demo Campaign", "Kainantu Open Demo Campaign"]).delete()
        self.User.objects.filter(username__startswith="prov-").delete()
        self.User.objects.filter(username__startswith="dist-").delete()

        prov_creds = self._build_candidate(
            name="Enga Provincial Demo Campaign", candidate_type="PROVINCIAL",
            plan="FULL_PACKAGE", bundle=bundles["complete-platform"],
            geo=GEO_PROV, prefix="prov", candidate_full_name="Hon. Maria Kila",
            party="People's Progress", slogan="Strong Wards, Strong Enga",
        )
        dist_creds = self._build_candidate(
            name="Kainantu Open Demo Campaign", candidate_type="DISTRICT_OPEN",
            plan="PROFESSIONAL", bundle=bundles["professional-campaign"],
            geo=GEO_DIST, prefix="dist", candidate_full_name="Hon. Peter Wari",
            party="Independent", slogan="Service Before Self — Kainantu First",
        )

        self.stdout.write(self.style.SUCCESS("\nDemo showcase seeded successfully.\n"))
        self.stdout.write(f"Platform admin:  admin / admin12345  (superuser)\n")
        self.stdout.write(f"Shared password for ALL team logins below:  {PASSWORD}\n")
        for label, creds in [("PROVINCIAL — Enga Governor", prov_creds), ("DISTRICT OPEN — Kainantu", dist_creds)]:
            self.stdout.write(self.style.HTTP_INFO(f"\n== {label} =="))
            for role, username in creds:
                self.stdout.write(f"  {role:<22} {username}")

    # ── names ────────────────────────────────────────────────────────────────
    def _name(self):
        n = f"{FIRST[self._name_i % len(FIRST)]} {SUR[(self._name_i // len(FIRST)) % len(SUR)]}"
        self._name_i += 1
        return n

    # ── platform catalog (modules / bundles / rate cards) ──────────────────────
    def _ensure_catalog(self):
        admin = self.admin
        module_rows = [
            ("core-crm", "Core Campaign CRM", "FOUNDATION", True, 1),
            ("supporter-registry", "Supporter Registry", "FIELD", True, 2),
            ("ward-intelligence", "Ward Intelligence", "INTELLIGENCE", False, 3),
            ("relationship-calls", "Relationship Calls", "CRM", False, 4),
            ("messaging", "Messaging Platform", "MESSAGING", False, 5),
            ("events-tasks", "Events and Tasking", "FIELD", False, 6),
            ("polling-war-room", "Polling-Day War Room", "POLLING", False, 7),
            ("ai-assistant", "AI Assistant", "AI", False, 8),
            ("constituency-management", "Constituency Management", "CONSTITUENCY", False, 9),
        ]
        modules = {}
        for code, name, category, is_core, order in module_rows:
            m, _ = SoftwareModule.objects.get_or_create(
                code=code,
                defaults={"name": name, "category": category, "is_core": is_core,
                          "sort_order": order, "created_by": admin, "updated_by": admin},
            )
            modules[code] = m
            for cycle, price in [("MONTHLY", 350), ("CAMPAIGN_PERIOD", 1750)]:
                ModulePrice.objects.get_or_create(
                    module=m, billing_cycle=cycle, currency="PGK",
                    defaults={"price": price, "created_by": admin, "updated_by": admin},
                )
        bundle_specs = [
            ("field-starter", "Field Starter", ["core-crm", "supporter-registry", "ward-intelligence"], 4850, 12, False, 1),
            ("professional-campaign", "Professional Campaign",
             ["core-crm", "supporter-registry", "ward-intelligence", "relationship-calls", "messaging", "events-tasks"], 8950, 18, False, 2),
            ("premium-war-room", "Premium War Room",
             ["core-crm", "supporter-registry", "ward-intelligence", "relationship-calls", "messaging", "events-tasks", "polling-war-room", "ai-assistant"], 12450, 22, False, 3),
            ("complete-platform", "Complete Platform", list(modules.keys()), 14950, 25, True, 4),
        ]
        bundles = {}
        for code, name, codes, price, discount, full, order in bundle_specs:
            b, _ = ModuleBundle.objects.get_or_create(
                code=code,
                defaults={"name": name, "billing_cycle": "CAMPAIGN_PERIOD", "bundle_price": price,
                          "discount_percent": discount, "is_full_package": full, "sort_order": order,
                          "created_by": admin, "updated_by": admin},
            )
            b.modules.set([modules[c] for c in codes])
            bundles[code] = b
        for bcode, service, unit, qty in [
            ("professional-campaign", "AI", "REQUEST", 50), ("professional-campaign", "SMS", "MESSAGE", 300),
            ("professional-campaign", "WHATSAPP", "MESSAGE", 150),
            ("complete-platform", "AI", "REQUEST", 150), ("complete-platform", "SMS", "MESSAGE", 600),
            ("complete-platform", "WHATSAPP", "MESSAGE", 300),
        ]:
            IncludedUsageQuota.objects.get_or_create(
                bundle=bundles[bcode], service=service, unit=unit, billing_cycle="CAMPAIGN_PERIOD",
                defaults={"quantity": qty, "created_by": admin, "updated_by": admin},
            )
        for service, provider, model_name, base, markup, fixed, minimum, is_free in [
            ("AI", "OpenAI-compatible", "premium", "0.120000", "35.00", "0.000000", "0.20", False),
            ("SMS", "Local SMS Provider", "", "0.080000", "40.00", "0.000000", "0.10", False),
            ("WHATSAPP", "Meta WhatsApp Business", "", "0.060000", "35.00", "0.000000", "0.08", False),
            ("EMAIL", "SMTP", "", "0.010000", "30.00", "0.000000", "0.02", False),
        ]:
            UsageRateCard.objects.get_or_create(
                service=service, provider=provider, model_name=model_name, unit=("REQUEST" if service == "AI" else ("MESSAGE" if service in ("SMS", "WHATSAPP") else "EMAIL")),
                currency="PGK",
                defaults={"provider_cost_per_unit": base, "markup_percent": markup, "fixed_markup_per_unit": fixed,
                          "minimum_charge": minimum, "is_free": is_free, "created_by": admin, "updated_by": admin},
            )
        return modules, bundles

    # ── one full candidate ─────────────────────────────────────────────────────
    def _build_candidate(self, *, name, candidate_type, plan, bundle, geo, prefix,
                         candidate_full_name, party, slogan):
        admin = self.admin
        today = timezone.localdate()
        now = timezone.now()
        creds = []
        used_login_roles = set()

        province, _ = Province.objects.get_or_create(name=geo["province"])

        # Build geography tree.
        tree = []
        for d in geo["districts"]:
            district, _ = District.objects.get_or_create(province=province, name=d["name"])
            llgs = []
            for l in d["llgs"]:
                llg, _ = LLG.objects.get_or_create(district=district, name=l["name"])
                wards = []
                for w in l["wards"]:
                    ward, _ = Ward.objects.get_or_create(llg=llg, name=w["name"], defaults={"number": w["number"]})
                    villages = [Village.objects.get_or_create(ward=ward, name=v)[0] for v in w["villages"]]
                    wards.append({"obj": ward, "villages": villages})
                llgs.append({"obj": llg, "wards": wards})
            tree.append({"obj": district, "llgs": llgs})

        first_district = tree[0]["obj"]
        candidate = Candidate.objects.create(
            name=name, candidate_type=candidate_type, province=province,
            district=(first_district if candidate_type == "DISTRICT_OPEN" else None),
            subscription_plan=plan, status="ACTIVE", created_by=admin, updated_by=admin,
        )
        CandidateProfile.objects.create(
            candidate=candidate, full_name=candidate_full_name, party=party, slogan=slogan,
            phone="+675 7000 0000", email=f"{prefix}-candidate@campaignmasta.local",
            campaign_office=f"{geo['province']} Campaign HQ", created_by=admin, updated_by=admin,
        )

        # Subscription + modules + included quotas.
        subscription = Subscription.objects.create(
            candidate=candidate, plan=plan, billing_cycle="CAMPAIGN_PERIOD", status="ACTIVE",
            amount=(14950 if plan == "FULL_PACKAGE" else 8950), payment_method="Invoice",
            invoice_number=f"CM-{prefix.upper()}-001", created_by=admin, updated_by=admin,
        )
        for module in bundle.modules.all():
            TenantModuleSubscription.objects.get_or_create(
                candidate=candidate, module=module,
                defaults={"subscription": subscription, "bundle": bundle,
                          "source": ("FULL_PACKAGE" if plan == "FULL_PACKAGE" else "BUNDLE"),
                          "is_enabled": True, "created_by": admin, "updated_by": admin},
            )
        provision_included_quotas(candidate, subscription, bundles=[bundle], user=admin)

        TenantSettings.objects.create(
            candidate=candidate, sms_sender_name="CMasta", ai_assistant_enabled=True,
            polling_day_mode=True, constituency_mode=(candidate_type == "DISTRICT_OPEN"),
            created_by=admin, updated_by=admin,
        )
        ConnectorSetting.objects.create(
            candidate=candidate, connector_type="AI", name="Free AI (DeepSeek/Kimi)",
            provider="DeepSeek", is_enabled=True, status="ACTIVE",
            api_base_url="https://openrouter.ai/api/v1", ai_model="deepseek/deepseek-chat-v3-0324:free",
            ai_system_policy="Assist with summaries and drafts; require human review before sending.",
            created_by=admin, updated_by=admin,
        )
        ConnectorSetting.objects.create(
            candidate=candidate, connector_type="SMS", name="PNG SMS Gateway",
            provider="Local SMS Provider", is_enabled=False, status="DISABLED",
            sms_sender_id="CMasta", sms_default_country_code="+675", created_by=admin, updated_by=admin,
        )
        ConnectorSetting.objects.create(
            candidate=candidate, connector_type="WHATSAPP", name="WhatsApp Business Cloud",
            provider="Meta WhatsApp Business", is_enabled=False, status="DISABLED",
            api_base_url="https://graph.facebook.com", whatsapp_default_template="campaign_update",
            created_by=admin, updated_by=admin,
        )
        for service, bal in [("AI", "25.00"), ("SMS", "30.00"), ("WHATSAPP", "20.00"), ("EMAIL", "5.00")]:
            wallet = UsageWallet.objects.create(
                candidate=candidate, service=service, currency="PGK", balance=0,
                low_balance_threshold="5.00", created_by=admin, updated_by=admin,
            )
            UsageTopUp.objects.create(
                candidate=candidate, wallet=wallet, amount=bal, currency="PGK",
                payment_reference=f"{prefix.upper()}-{service}-TOPUP", payment_method="Demo prepaid credit",
                received_by=admin, created_by=admin, updated_by=admin,
            )

        # ── Team hierarchy ─────────────────────────────────────────────────────
        def mk(role, full_name, district=None, llg=None, ward=None, village=None,
               login_role=None, pending=False, created_by_member=None):
            member = TeamMember.objects.create(
                candidate=candidate, full_name=full_name, role=role, province=province,
                district=district, llg=llg, ward=ward, village=village,
                phone=f"+675 7{self._name_i % 9}00 {1000 + self._name_i}",
                approval_status=(ApprovalStatus.PENDING if pending else ApprovalStatus.APPROVED),
                is_active=(not pending), created_by_member=created_by_member,
                approved_at=(None if pending else now),
                created_by=admin, updated_by=admin,
            )
            if login_role and login_role not in used_login_roles:
                username = f"{prefix}-{login_role}"
                provision_team_member_login(member, username, PASSWORD, user=admin)
                creds.append((member.get_role_display(), username))
                used_login_roles.add(login_role)
            return member

        candidate_member = mk(Role.CANDIDATE, candidate_full_name, login_role="candidate")
        candidate.user = candidate_member.user
        candidate.save(update_fields=["user"])
        manager = mk(Role.CAMPAIGN_MANAGER, self._name(), login_role="manager")
        mk(Role.IT_ADMIN, self._name(), login_role="itadmin")

        ward_coords, area_coords, volunteers, scrutineers = [], [], [], []
        district_coords, llg_coords = [], []
        for dnode in tree:
            district = dnode["obj"]
            dco = None
            if candidate_type == "PROVINCIAL":
                dco = mk(Role.DISTRICT_COORDINATOR, self._name(), district=district, login_role="district")
                district_coords.append(dco)
            for lnode in dnode["llgs"]:
                llg = lnode["obj"]
                lco = mk(Role.LLG_COORDINATOR, self._name(), district=district, llg=llg, login_role="llg")
                llg_coords.append(lco)
                for wnode in lnode["wards"]:
                    ward = wnode["obj"]
                    wco = mk(Role.WARD_COORDINATOR, self._name(), district=district, llg=llg, ward=ward, login_role="ward")
                    ward_coords.append((wco, ward, llg, district))
                    scr = mk(Role.SCRUTINEER, self._name(), district=district, llg=llg, ward=ward, login_role="scrutineer")
                    scrutineers.append((scr, ward, llg, district))
                    for village in wnode["villages"]:
                        aco = mk(Role.VILLAGE_COORDINATOR, self._name(), district=district, llg=llg, ward=ward, village=village, login_role="area")
                        area_coords.append((aco, ward, llg, district, village))
                        vol = mk(Role.VOLUNTEER, self._name(), district=district, llg=llg, ward=ward, village=village, login_role="volunteer", created_by_member=aco)
                        volunteers.append((vol, ward, llg, district, village))

        # Pending members (awaiting approval) + a pending village to showcase approvals.
        sample_ward = ward_coords[0]
        mk(Role.VOLUNTEER, self._name() + " (pending)", district=sample_ward[3], llg=sample_ward[2],
           ward=sample_ward[1], village=area_coords[0][4], pending=True, created_by_member=area_coords[0][0])
        Village.objects.create(
            ward=sample_ward[1], name="New Settlement (pending)",
            approval_status=ApprovalStatus.PENDING, created_by=admin, created_by_member=sample_ward[0],
        )

        # ── Supporters at every level (drives the incentive leaderboard) ────────
        def register(registrant, district, llg, ward, village, status, consent=True, issue="Water supply"):
            s = Supporter(
                candidate=candidate, full_name=self._name(),
                phone=f"+675 74{self._name_i % 9}0 {2000 + self._name_i}",
                gender=("FEMALE" if self._name_i % 2 else "MALE"),
                province=province, district=district, llg=llg, ward=ward, village=village,
                clan=f"{village.name} clan", support_status=status, influence_level="LOW",
                main_issue=issue, consent_to_messages=consent,
                enrollment_status=("VERIFIED_ENROLLED" if consent else "UNKNOWN"),
                created_by=admin, updated_by=admin,
            )
            for field, value in supporter_attribution_fields(
                candidate, registrant, district=district, llg=llg, ward=ward, village=village
            ).items():
                setattr(s, field, value)
            s.save()
            return s

        statuses = ["STRONG", "LEANING", "UNDECIDED", "STRONG", "NOT_SUPPORTIVE"]
        si = 0
        for vol, ward, llg, district, village in volunteers:
            for _ in range(3):  # volunteers register the bulk — their personal incentive count
                register(vol, district, llg, ward, village, statuses[si % len(statuses)], consent=(si % 4 != 0))
                si += 1
        for aco, ward, llg, district, village in area_coords:
            for _ in range(2):  # area coordinators register some directly
                register(aco, district, llg, ward, village, statuses[si % len(statuses)])
                si += 1
        for wco, ward, llg, district in ward_coords[:2]:
            village = ward.villages.first()
            register(wco, district, llg, ward, village, "STRONG")
        for lco in llg_coords[:1]:
            ward = ward_coords[0][1]
            register(lco, ward_coords[0][3], lco.llg, ward, ward.villages.first(), "LEANING")
        for dco in district_coords[:1]:
            ward = ward_coords[0][1]
            register(dco, dco.district, ward.llg, ward, ward.villages.first(), "UNDECIDED")

        # ── Ward intelligence: profiles, landmarks, briefs ─────────────────────
        strengths = ["STRONG", "MEDIUM", "WEAK", "MEDIUM"]
        for i, (wco, ward, llg, district) in enumerate(ward_coords):
            village = ward.villages.first()
            profile = WardProfile.objects.create(
                candidate=candidate, ward=ward, councillor_name=f"Councillor {self._name()}",
                key_clans=f"{village.name} clan, river clan", key_churches="Lutheran, Catholic, SDA",
                important_landmarks=f"{village.name} market, sports field, community hall",
                meeting_places="Church hall and sports field",
                population_estimate=1200 + i * 300, estimated_voting_population=700 + i * 180,
                support_strength=strengths[i % len(strengths)],
                main_community_issues="Road access, water supply, and school fee support are the top concerns.",
                security_concerns=("Inter-clan tension near the boundary — avoid taking sides." if i == 0 else ""),
                youth_groups="Ward youth fellowship", womens_groups="Mothers' union",
                notes_for_candidate="Acknowledge local leaders first; keep commitments specific and realistic.",
                created_by=admin, updated_by=admin,
            )
            Landmark.objects.create(
                candidate=candidate, name=f"{village.name} Community Hall", landmark_type="COMMUNITY_HALL",
                province=province, district=district, llg=llg, ward=ward, village=village,
                created_by=admin, updated_by=admin,
            )
            if i == 0:
                create_ward_ai_work_item(candidate, profile, admin)
                create_speech_ai_work_item(candidate, profile, None, admin)

        # ── Influencers + call logs ────────────────────────────────────────────
        influencers = []
        roles_pool = [("Pastor", "HIGH"), ("Councillor", "HIGH"), ("Youth Leader", "MEDIUM"),
                      ("Women's Leader", "MEDIUM"), ("Business Owner", "MEDIUM"), ("Clan Elder", "HIGH")]
        for i, (wco, ward, llg, district) in enumerate(ward_coords):
            village = ward.villages.first()
            for j in range(2):
                role_name, level = roles_pool[(i + j) % len(roles_pool)]
                inf = Influencer.objects.create(
                    candidate=candidate, full_name=self._name(), phone=f"+675 7555 {1000 + i * 10 + j}",
                    province=province, district=district, llg=llg, ward=ward, village=village,
                    community_role=role_name, influence_category=role_name, influence_level=level,
                    estimated_network_size=150 + i * 40, relationship_status="MEDIUM",
                    preferred_contact_method="CALL", contact_frequency_days=7,
                    last_call_date=today - timedelta(days=10 + i),
                    next_contact_due_date=today - timedelta(days=3) if i == 0 else today + timedelta(days=j),
                    assigned_owner=manager, created_by=admin, updated_by=admin,
                )
                influencers.append(inf)
        from campaigns.models import CallLog
        for i, inf in enumerate(influencers[:5]):
            CallLog.objects.create(
                candidate=candidate, caller=manager, influencer=inf, person_called=inf.full_name,
                person_type="Influencer", phone_number=inf.phone,
                call_datetime=now - timedelta(days=i + 1),
                call_outcome=("ANSWERED" if i % 2 == 0 else "MISSED"),
                discussion_summary="Discussed upcoming ward visit and local priorities.",
                issues_raised="Water supply and road maintenance.",
                commitments_made="Candidate to attend the next community meeting.",
                follow_up_required=(i % 2 == 1), follow_up_date=today + timedelta(days=3),
                recorded_by=admin, created_by=admin, updated_by=admin,
            )

        # ── Tasks ──────────────────────────────────────────────────────────────
        task_specs = [
            ("Confirm ward visit venue", "HIGH", "PENDING", 1),
            ("Mobilise youth group for rally", "NORMAL", "IN_PROGRESS", 3),
            ("Print posters and banners", "NORMAL", "COMPLETED", -2),
            ("Arrange transport for polling teams", "URGENT", "PENDING", 0),
            ("Follow up with councillor", "HIGH", "OVERDUE", -4),
        ]
        for title, prio, status, due in task_specs:
            wco, ward, llg, district = ward_coords[0]
            CampaignTask.objects.create(
                candidate=candidate, title=title, description="Demo task for showcasing the task board.",
                assigned_to=wco, assigned_by=manager, province=province, district=district, llg=llg, ward=ward,
                priority=prio, status=status, due_date=today + timedelta(days=due),
                created_by=admin, updated_by=admin,
            )

        # ── Events (past w/ attendance + upcoming) ─────────────────────────────
        wco, ward, llg, district = ward_coords[0]
        village = ward.villages.first()
        past = CampaignEvent.objects.create(
            candidate=candidate, title=f"{ward.name} Listening Visit", event_type="WARD_VISIT",
            venue_type="VILLAGE_MEETING", province=province, district=district, llg=llg, ward=ward, village=village,
            venue=f"{village.name} community hall", host_person="Pastor Joel",
            start_datetime=now - timedelta(days=5), end_datetime=now - timedelta(days=5) + timedelta(hours=3),
            expected_crowd_size=150, actual_attendance=130,
            talking_points="Water, youth employment, safe transport.",
            event_report="Strong turnout; water supply raised repeatedly.", created_by=admin, updated_by=admin,
        )
        EventChecklistItem.objects.create(candidate=candidate, event=past, title="Confirm venue", assigned_to=wco, is_complete=True, created_by=admin, updated_by=admin)
        EventChecklistItem.objects.create(candidate=candidate, event=past, title="Arrange sound system", assigned_to=wco, is_complete=True, created_by=admin, updated_by=admin)
        for s in Supporter.objects.filter(candidate=candidate, ward=ward)[:5]:
            EventAttendance.objects.create(candidate=candidate, event=past, supporter=s, full_name=s.full_name, phone=s.phone, village=s.village, created_by=admin, updated_by=admin)
        upcoming = CampaignEvent.objects.create(
            candidate=candidate, title="Major Campaign Rally", event_type="RALLY", venue_type="ROADSIDE_RALLY",
            province=province, district=district, llg=llg, ward=ward, village=village, venue="Town oval",
            host_person=manager.full_name, start_datetime=now + timedelta(days=4),
            expected_crowd_size=800, talking_points="Vision, development record, preference appeal.",
            created_by=admin, updated_by=admin,
        )
        EventChecklistItem.objects.create(candidate=candidate, event=upcoming, title="Book PA system", assigned_to=wco, is_complete=False, created_by=admin, updated_by=admin)
        EventChecklistItem.objects.create(candidate=candidate, event=upcoming, title="Security plan", assigned_to=wco, is_complete=False, created_by=admin, updated_by=admin)

        # ── Messages (sent w/ read receipts + draft + polling reminder) ────────
        sent = Message.objects.create(
            candidate=candidate, sender=manager, message_type="STANDARD", recipient_type="All Ward Coordinators",
            subject="Weekly coordination update", body="Confirm venues, acknowledge local leaders, and submit ward reports by Friday.",
            priority="IMPORTANT", delivery_channel="IN_APP", status="SENT", sent_at=now - timedelta(days=1),
            read_receipt_required=True, acknowledgement_required=True, created_by=admin, updated_by=admin,
        )
        for i, (wco, *_rest) in enumerate(ward_coords):
            MessageRecipient.objects.create(
                message=sent, team_member=wco, display_name=wco.full_name, phone=wco.phone,
                delivered_at=now - timedelta(days=1),
                read_at=(now - timedelta(hours=12) if i % 2 == 0 else None),
                acknowledged_at=(now - timedelta(hours=10) if i == 0 else None),
            )
        Message.objects.create(
            candidate=candidate, sender=manager, message_type="POLLING_DAY_REMINDER", recipient_type="Scrutineers",
            subject="Polling day instructions", body="Arrive by 6am, confirm materials, and report booth status hourly.",
            priority="URGENT", delivery_channel="SMS", status="DRAFT", read_receipt_required=True,
            acknowledgement_required=True, created_by=admin, updated_by=admin,
        )

        # ── Issues & promises ──────────────────────────────────────────────────
        for i, (title, cat, prio, status) in enumerate([
            ("Water pressure drops in the evening", "Water supply", "HIGH", "NEW"),
            ("Main road impassable after rain", "Roads", "URGENT", "FOLLOW_UP"),
            ("School needs classroom repairs", "Education", "NORMAL", "UNDER_REVIEW"),
        ]):
            wco, ward, llg, district = ward_coords[i % len(ward_coords)]
            CommunityIssue.objects.create(
                candidate=candidate, title=title, category=cat, description="Raised by residents during ward outreach.",
                province=province, district=district, llg=llg, ward=ward, village=ward.villages.first(),
                reported_by="Community member", priority=prio, status=status, created_by=admin, updated_by=admin,
            )
        for i, (title, cat, status) in enumerate([
            ("Meet the water authority", "WATER_SANITATION", "OPEN"),
            ("Deliver school materials", "EDUCATION", "IN_PROGRESS"),
            ("Grade the access road", "INFRASTRUCTURE", "DELIVERED"),
        ]):
            wco, ward, llg, district = ward_coords[i % len(ward_coords)]
            PromiseTracker.objects.create(
                candidate=candidate, title=title, description="Commitment made during a community visit.",
                category=cat, made_by=candidate_full_name, made_to=f"{ward.name} residents",
                province=province, district=district, llg=llg, ward=ward,
                promise_date=today - timedelta(days=20), target_date=today + timedelta(days=20),
                status=status, public_facing=(status == "DELIVERED"), follow_up_owner=manager,
                created_by=admin, updated_by=admin,
            )

        # ── Polling day ────────────────────────────────────────────────────────
        for i, (scr, ward, llg, district) in enumerate(scrutineers):
            village = ward.villages.first()
            loc = PollingLocation.objects.create(
                candidate=candidate, name=f"{village.name} Primary School Booth",
                province=province, district=district, llg=llg, ward=ward, village=village,
                assigned_scrutineer=scr, contact_number=scr.phone, status="Ready",
                transport_status="Vehicle assigned", security_risk=("MODERATE" if i == 0 else "LOW"),
                expected_turnout=600 + i * 50, past_vote_data={"2022": {"our_candidate": 340 + i * 10, "opponent": 120}},
                created_by=admin, updated_by=admin,
            )
            PollingStatus.objects.create(
                candidate=candidate, polling_location=loc, reported_by=scr, scrutineer_present=True,
                booth_open=(i == 0), materials_available=True, communication_ok=True,
                our_tally=(45 + i * 12 if i == 0 else 0),
                notes="Booth set up; awaiting opening." if i else "Voting underway, steady turnout.",
                created_by=admin, updated_by=admin,
            )
        first_scr, first_ward, first_llg, first_district = scrutineers[0]
        PollingIncident.objects.create(
            candidate=candidate, polling_location=PollingLocation.objects.filter(candidate=candidate).first(),
            reported_by=first_scr, title="Late delivery of ballot papers",
            description="Materials arrived 40 minutes late; voting started slightly delayed.",
            priority="HIGH", status="IN_PROGRESS", created_by=admin, updated_by=admin,
        )

        # ── PNG-specific modules ───────────────────────────────────────────────
        PreferenceDeal.objects.create(
            candidate=candidate, partner_candidate_name=self._name(), partner_party="Independent",
            partner_seat=f"{tree[0]['obj'].name}", status="AGREED", contact_person=manager,
            ward_directives="Push 2nd preference in the urban wards.", deal_terms="Mutual 2nd-preference support.",
            created_by=admin, updated_by=admin,
        )
        for i, (wco, ward, llg, district) in enumerate(ward_coords[:3]):
            CommunityGroup.objects.create(
                candidate=candidate, name=f"{ward.villages.first().name} Youth Fellowship",
                group_type=("YOUTH_GROUP" if i % 2 == 0 else "WOMENS_GROUP"), ward=ward, village=ward.villages.first(),
                estimated_voting_members=80 + i * 20, alignment=("STRONG_SUPPORTER" if i == 0 else "NEUTRAL"),
                key_contact=(influencers[i] if i < len(influencers) else None), created_by=admin, updated_by=admin,
            )
        for i, (wco, ward, llg, district) in enumerate(ward_coords[:2]):
            CommunityAssistance.objects.create(
                candidate=candidate, ward=ward, village=ward.villages.first(), date=today - timedelta(days=7 + i),
                recipient_group=f"{ward.villages.first().name} Church Group",
                assistance_type=("SCHOOL_MATERIALS" if i == 0 else "FOOD_FEAST"),
                description="Community assistance recorded for transparency.",
                estimated_value_pgk=Decimal("1500.00") + i * 500, approved_by=manager, created_by=admin, updated_by=admin,
            )
        CompetitorActivity.objects.create(
            candidate=candidate, opponent_name=self._name(), opponent_party="Rival Party",
            ward=ward_coords[0][1], activity_type="RALLY", source="SOCIAL_MEDIA",
            description="Opponent held a rally promising road upgrades.",
            response_action="Reinforce our delivery record in the same ward.", response_assigned_to=manager,
            created_by=admin, updated_by=admin,
        )
        DevelopmentFund.objects.create(
            candidate=candidate, fund_name=f"{tree[0]['obj'].name} DSIP 2025",
            fund_type=("SDP" if candidate_type == "PROVINCIAL" else "DSIP"), financial_year="2025",
            total_allocation_pgk=Decimal("10000000.00"), spent_pgk=Decimal("6500000.00"),
            ward=ward_coords[0][1], district=tree[0]["obj"], notes="Tracking allocation vs spend by ward.",
            created_by=admin, updated_by=admin,
        )
        drive = RegistrationDrive.objects.create(
            candidate=candidate, title=f"{ward_coords[0][1].name} Enrolment Drive", ward=ward_coords[0][1],
            start_date=today - timedelta(days=5), end_date=today + timedelta(days=5),
            target_count=300, actual_count=180, status="ACTIVE", notes="Helping eligible voters enrol.",
            created_by=admin, updated_by=admin,
        )
        drive.team_members.set([ward_coords[0][0], volunteers[0][0]])

        # ── Constituency (citizen requests) ────────────────────────────────────
        for i, (title, cat, status) in enumerate([
            ("Repair footbridge near market", "Infrastructure", "NEW"),
            ("Sponsorship for school fees", "Education", "UNDER_REVIEW"),
        ]):
            wco, ward, llg, district = ward_coords[i % len(ward_coords)]
            CitizenRequest.objects.create(
                candidate=candidate, title=title, requester_name=f"{ward.villages.first().name} community",
                phone="+675 7444 1999", province=province, district=district, llg=llg, ward=ward,
                village=ward.villages.first(), category=cat, description="Constituency service request after the election.",
                status=status, assigned_to=manager, due_date=today + timedelta(days=14), created_by=admin, updated_by=admin,
            )

        return creds
