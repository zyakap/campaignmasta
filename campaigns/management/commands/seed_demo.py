from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from campaigns.models import (
    AIWorkItem,
    CampaignEvent,
    CampaignTask,
    CandidateProfile,
    Candidate,
    CitizenRequest,
    CommunityIssue,
    ConnectorSetting,
    District,
    FreeAIModel,
    IncludedUsageQuota,
    Landmark,
    Influencer,
    LLG,
    Message,
    ModuleBundle,
    ModulePrice,
    PollingLocation,
    PollingStatus,
    PromiseTracker,
    Province,
    Role,
    Subscription,
    SoftwareModule,
    Supporter,
    TeamMember,
    TenantSettings,
    TenantModuleSubscription,
    UsageRateCard,
    UsageTopUp,
    UsageWallet,
    Village,
    Ward,
    WardProfile,
)
from campaigns.services import create_ward_ai_work_item, provision_included_quotas


class Command(BaseCommand):
    help = "Seed a mobile-first CampaignMasta demo candidate."

    def handle(self, *args, **options):
        User = get_user_model()
        admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@campaignmasta.local", "is_staff": True, "is_superuser": True})
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("admin12345")
        admin.save()

        province, _ = Province.objects.get_or_create(name="National Capital District")
        district_a, _ = District.objects.get_or_create(province=province, name="Moresby North-West Open")
        district_b, _ = District.objects.get_or_create(province=province, name="Moresby South Open")
        llg_a, _ = LLG.objects.get_or_create(district=district_a, name="Moresby North-West Urban LLG")
        llg_b, _ = LLG.objects.get_or_create(district=district_b, name="Moresby South Urban LLG")
        ward_1, _ = Ward.objects.get_or_create(llg=llg_a, name="Ward 1", defaults={"number": "1"})
        ward_2, _ = Ward.objects.get_or_create(llg=llg_a, name="Ward 2", defaults={"number": "2"})
        ward_3, _ = Ward.objects.get_or_create(llg=llg_b, name="Ward 3", defaults={"number": "3"})
        village_1, _ = Village.objects.get_or_create(ward=ward_1, name="Tokarara")
        village_2, _ = Village.objects.get_or_create(ward=ward_2, name="June Valley")
        village_3, _ = Village.objects.get_or_create(ward=ward_3, name="Koki")

        candidate, _ = Candidate.objects.get_or_create(
            name="Demo NCD Governor Campaign",
            defaults={
                "candidate_type": "PROVINCIAL",
                "province": province,
                "subscription_plan": "PREMIUM",
                "status": "ACTIVE",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        module_rows = [
            ("core-crm", "Core Campaign CRM", "FOUNDATION", True, 1, "Tenant setup, candidate profile, geography, team roles, and dashboard."),
            ("supporter-registry", "Supporter Registry", "FIELD", True, 2, "Supporter and potential supporter records with consent tracking."),
            ("ward-intelligence", "Ward Intelligence", "INTELLIGENCE", False, 3, "Ward profiles, visit briefs, landmarks, issues, and local context."),
            ("relationship-calls", "Relationship Calls", "CRM", False, 4, "Influencer CRM, call logs, reminders, and overdue follow-up discipline."),
            ("messaging", "Messaging Platform", "MESSAGING", False, 5, "Internal messages, targeted broadcasts, read receipts, and acknowledgements."),
            ("events-tasks", "Events and Tasking", "FIELD", False, 6, "Campaign visits, event planning, checklists, attendance, and task assignment."),
            ("polling-war-room", "Polling-Day War Room", "POLLING", False, 7, "Polling locations, scrutineer assignment, status updates, and incidents."),
            ("ai-assistant", "AI Assistant", "AI", False, 8, "Human-reviewed ward briefs, speech notes, summaries, and draft assistance."),
            ("constituency-management", "Constituency Management", "CONSTITUENCY", False, 9, "Citizen requests, projects, grants, and post-election service follow-up."),
        ]
        modules = {}
        for code, name, category, is_core, sort_order, description in module_rows:
            module, _ = SoftwareModule.objects.get_or_create(
                code=code,
                defaults={"name": name, "category": category, "is_core": is_core, "sort_order": sort_order, "description": description, "created_by": admin, "updated_by": admin},
            )
            modules[code] = module
            for cycle, price in [("MONTHLY", 350), ("CAMPAIGN_PERIOD", 1750)]:
                if code == "core-crm":
                    price = 600 if cycle == "MONTHLY" else 3000
                elif code in {"polling-war-room", "ai-assistant"}:
                    price = 500 if cycle == "MONTHLY" else 2500
                elif code == "constituency-management":
                    price = 450 if cycle == "MONTHLY" else 2200
                ModulePrice.objects.get_or_create(module=module, billing_cycle=cycle, currency="PGK", defaults={"price": price, "created_by": admin, "updated_by": admin})

        bundle_specs = [
            ("field-starter", "Field Starter", ["core-crm", "supporter-registry", "ward-intelligence"], 4850, 12, False, 1),
            ("professional-campaign", "Professional Campaign", ["core-crm", "supporter-registry", "ward-intelligence", "relationship-calls", "messaging", "events-tasks"], 8950, 18, False, 2),
            ("premium-war-room", "Premium War Room", ["core-crm", "supporter-registry", "ward-intelligence", "relationship-calls", "messaging", "events-tasks", "polling-war-room", "ai-assistant"], 12450, 22, False, 3),
            ("complete-platform", "Complete Platform", list(modules.keys()), 14950, 25, True, 4),
        ]
        bundles = {}
        for code, name, module_codes, price, discount, is_full, sort_order in bundle_specs:
            bundle, _ = ModuleBundle.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": "Discounted module package for candidates who need this operating level.",
                    "billing_cycle": "CAMPAIGN_PERIOD",
                    "bundle_price": price,
                    "discount_percent": discount,
                    "is_full_package": is_full,
                    "sort_order": sort_order,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )
            bundle.modules.set([modules[module_code] for module_code in module_codes])
            bundles[code] = bundle
        included_quota_specs = [
            ("field-starter", "SMS", "MESSAGE", 250, "Campaign-period SMS messages included with Field Starter."),
            ("professional-campaign", "AI", "REQUEST", 100, "Campaign-period AI assistant requests included with Professional Campaign."),
            ("professional-campaign", "SMS", "MESSAGE", 1000, "Campaign-period SMS messages included with Professional Campaign."),
            ("professional-campaign", "WHATSAPP", "MESSAGE", 500, "Campaign-period WhatsApp messages included with Professional Campaign."),
            ("premium-war-room", "AI", "REQUEST", 500, "Campaign-period AI assistant requests included with Premium War Room."),
            ("premium-war-room", "SMS", "MESSAGE", 2500, "Campaign-period SMS messages included with Premium War Room."),
            ("premium-war-room", "WHATSAPP", "MESSAGE", 1500, "Campaign-period WhatsApp messages included with Premium War Room."),
            ("complete-platform", "AI", "REQUEST", 1000, "Campaign-period AI assistant requests included with Complete Platform."),
            ("complete-platform", "SMS", "MESSAGE", 5000, "Campaign-period SMS messages included with Complete Platform."),
            ("complete-platform", "WHATSAPP", "MESSAGE", 3000, "Campaign-period WhatsApp messages included with Complete Platform."),
        ]
        for bundle_code, service, unit, quantity, description in included_quota_specs:
            IncludedUsageQuota.objects.get_or_create(
                bundle=bundles[bundle_code],
                service=service,
                unit=unit,
                billing_cycle="CAMPAIGN_PERIOD",
                defaults={"quantity": quantity, "description": description, "created_by": admin, "updated_by": admin},
            )
        CandidateProfile.objects.get_or_create(
            candidate=candidate,
            full_name="Maria Kila",
            defaults={
                "party": "Independent",
                "slogan": "Strong Wards, Strong Future",
                "phone": "+675 7000 0000",
                "email": "candidate@campaignmasta.local",
                "campaign_office": "Waigani, Port Moresby",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        subscription, _ = Subscription.objects.get_or_create(
            candidate=candidate,
            defaults={
                "plan": "PREMIUM",
                "billing_cycle": "CAMPAIGN_PERIOD",
                "status": "ACTIVE",
                "amount": 12500,
                "payment_method": "Invoice",
                "invoice_number": "CM-DEMO-001",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        for module in bundles["complete-platform"].modules.all():
            TenantModuleSubscription.objects.get_or_create(
                candidate=candidate,
                module=module,
                defaults={"subscription": subscription, "bundle": bundles["complete-platform"], "source": "FULL_PACKAGE", "is_enabled": True, "created_by": admin, "updated_by": admin},
            )
        if not candidate.tenantusagequotas.filter(subscription=subscription).exists():
            provision_included_quotas(candidate, subscription, bundles=[bundles["complete-platform"]], user=admin)
        TenantSettings.objects.get_or_create(
            candidate=candidate,
            defaults={
                "sms_sender_name": "CMasta",
                "ai_assistant_enabled": True,
                "polling_day_mode": True,
                "constituency_mode": True,
                "created_by": admin,
                "updated_by": admin,
            },
        )
        ConnectorSetting.objects.get_or_create(
            candidate=candidate,
            connector_type="AI",
            name="Campaign AI Assistant",
            defaults={
                "provider": "OpenAI-compatible",
                "is_enabled": True,
                "status": "NEEDS_TEST",
                "api_base_url": "https://api.openai.com/v1",
                "ai_model": "gpt-4.1-mini",
                "ai_system_policy": "Assist with organization, summaries, reminders, and draft preparation. Require human review before sending messages.",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        ConnectorSetting.objects.get_or_create(
            candidate=candidate,
            connector_type="WHATSAPP",
            name="WhatsApp Business Cloud",
            defaults={
                "provider": "Meta WhatsApp Business",
                "is_enabled": False,
                "status": "DISABLED",
                "api_base_url": "https://graph.facebook.com",
                "whatsapp_default_template": "campaign_update",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        ConnectorSetting.objects.get_or_create(
            candidate=candidate,
            connector_type="SMS",
            name="PNG SMS Gateway",
            defaults={
                "provider": "Local SMS Provider",
                "is_enabled": False,
                "status": "DISABLED",
                "sms_sender_id": "CMasta",
                "sms_default_country_code": "+675",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        FreeAIModel.objects.get_or_create(
            model_id="local-free-summary",
            defaults={
                "name": "Local Free Summary Model",
                "provider": "CampaignMasta Free",
                "daily_free_requests": 25,
                "monthly_free_requests": 500,
                "notes": "Free option for low-budget tenants. Uses no prepaid AI balance.",
                "created_by": admin,
                "updated_by": admin,
            },
        )
        for service, provider, model_name, unit, base, markup, fixed, minimum, is_free in [
            ("AI", "OpenAI-compatible", "gpt-4.1-mini", "REQUEST", "0.120000", "35.00", "0.000000", "0.20", False),
            ("AI", "CampaignMasta Free", "local-free-summary", "REQUEST", "0.000000", "0.00", "0.000000", "0.00", True),
            ("SMS", "Local SMS Provider", "", "MESSAGE", "0.080000", "40.00", "0.000000", "0.10", False),
            ("WHATSAPP", "Meta WhatsApp Business", "", "MESSAGE", "0.060000", "35.00", "0.000000", "0.08", False),
            ("EMAIL", "SMTP", "", "EMAIL", "0.010000", "30.00", "0.000000", "0.02", False),
        ]:
            UsageRateCard.objects.get_or_create(
                service=service,
                provider=provider,
                model_name=model_name,
                unit=unit,
                currency="PGK",
                defaults={
                    "provider_cost_per_unit": base,
                    "markup_percent": markup,
                    "fixed_markup_per_unit": fixed,
                    "minimum_charge": minimum,
                    "is_free": is_free,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )
        for service, balance in [("AI", "20.00"), ("SMS", "20.00"), ("WHATSAPP", "20.00"), ("EMAIL", "5.00")]:
            wallet, _ = UsageWallet.objects.get_or_create(
                candidate=candidate,
                service=service,
                currency="PGK",
                defaults={"balance": 0, "low_balance_threshold": "5.00", "created_by": admin, "updated_by": admin},
            )
            if wallet.balance == 0:
                UsageTopUp.objects.get_or_create(
                    candidate=candidate,
                    wallet=wallet,
                    payment_reference=f"DEMO-{service}-TOPUP",
                    defaults={"amount": balance, "currency": "PGK", "payment_method": "Demo prepaid credit", "received_by": admin, "created_by": admin, "updated_by": admin},
                )

        manager, _ = TeamMember.objects.get_or_create(
            candidate=candidate,
            full_name="John Campaign",
            defaults={"role": Role.CAMPAIGN_MANAGER, "phone": "+675 7111 1111", "province": province, "created_by": admin, "updated_by": admin},
        )
        district_coord, _ = TeamMember.objects.get_or_create(
            candidate=candidate,
            full_name="Anna District",
            defaults={"role": Role.DISTRICT_COORDINATOR, "phone": "+675 7222 2222", "province": province, "district": district_a, "created_by": admin, "updated_by": admin},
        )
        ward_coord, _ = TeamMember.objects.get_or_create(
            candidate=candidate,
            full_name="Peter Ward",
            defaults={"role": Role.WARD_COORDINATOR, "phone": "+675 7333 3333", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "created_by": admin, "updated_by": admin},
        )
        scrutineer, _ = TeamMember.objects.get_or_create(
            candidate=candidate,
            full_name="Lisa Scrutineer",
            defaults={"role": Role.SCRUTINEER, "phone": "+675 7666 6666", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "created_by": admin, "updated_by": admin},
        )

        landmark, _ = Landmark.objects.get_or_create(
            candidate=candidate,
            name="Tokarara Community Hall",
            defaults={"landmark_type": "COMMUNITY_HALL", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "village": village_1, "created_by": admin, "updated_by": admin},
        )

        for ward, village, strength, issue in [
            (ward_1, village_1, "STRONG", "Water pressure and youth employment are the main talking points."),
            (ward_2, village_2, "MEDIUM", "Road access and school fee support are being raised by families."),
            (ward_3, village_3, "WEAK", "Market facilities, law and order, and transport need careful listening."),
        ]:
            WardProfile.objects.get_or_create(
                candidate=candidate,
                ward=ward,
                defaults={
                    "councillor_name": f"Councillor {ward.name}",
                    "important_landmarks": f"{village.name} market, church grounds, community hall",
                    "meeting_places": "Church hall and sports field",
                    "support_strength": strength,
                    "main_community_issues": issue,
                    "notes_for_candidate": "Acknowledge local leaders first and keep commitments specific.",
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

        supporter_rows = [
            ("Ruth Tokarara", "+675 7444 1001", ward_1, village_1, "STRONG", True, "Water supply"),
            ("Michael June", "+675 7444 1002", ward_2, village_2, "UNDECIDED", True, "School fees"),
            ("Lucy Koki", "+675 7444 1003", ward_3, village_3, "LEANING", False, "Market upgrade"),
        ]
        for name, phone, ward, village, status, consent, issue in supporter_rows:
            Supporter.objects.get_or_create(
                candidate=candidate,
                full_name=name,
                defaults={
                    "phone": phone,
                    "province": province,
                    "district": ward.llg.district,
                    "llg": ward.llg,
                    "ward": ward,
                    "village": village,
                    "support_status": status,
                    "influence_level": "LOW",
                    "main_issue": issue,
                    "consent_to_messages": consent,
                    "registered_by": ward_coord,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

        today = timezone.localdate()
        for name, role, ward, village, due_offset in [
            ("Pastor Joel", "Church Leader", ward_1, village_1, -2),
            ("Councillor Mary", "Councillor", ward_2, village_2, 0),
            ("Sarah Youth", "Youth Leader", ward_3, village_3, 3),
        ]:
            Influencer.objects.get_or_create(
                candidate=candidate,
                full_name=name,
                defaults={
                    "phone": "+675 7555 0000",
                    "province": province,
                    "district": ward.llg.district,
                    "llg": ward.llg,
                    "ward": ward,
                    "village": village,
                    "community_role": role,
                    "influence_category": role,
                    "influence_level": "HIGH" if "Councillor" in role or "Pastor" in role else "MEDIUM",
                    "relationship_status": "MEDIUM",
                    "contact_frequency_days": 7,
                    "next_contact_due_date": today + timedelta(days=due_offset),
                    "assigned_owner": manager,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

        CampaignTask.objects.get_or_create(
            candidate=candidate,
            title="Confirm Tokarara ward visit venue",
            defaults={"assigned_to": ward_coord, "assigned_by": manager, "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "priority": "HIGH", "due_date": today + timedelta(days=1), "created_by": admin, "updated_by": admin},
        )
        event, _ = CampaignEvent.objects.get_or_create(
            candidate=candidate,
            title="Ward 1 Listening Visit",
            defaults={"event_type": "WARD_VISIT", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "village": village_1, "venue": "Tokarara community hall", "landmark": landmark, "host_person": "Pastor Joel", "start_datetime": timezone.now() + timedelta(days=2), "expected_crowd_size": 120, "talking_points": "Water, youth employment, safe transport.", "created_by": admin, "updated_by": admin},
        )
        CommunityIssue.objects.get_or_create(
            candidate=candidate,
            title="Water pressure drops in Tokarara",
            defaults={"category": "Water supply", "description": "Residents report unreliable water pressure in the evenings.", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "village": village_1, "reported_by": "Ruth Tokarara", "priority": "HIGH", "created_by": admin, "updated_by": admin},
        )
        PromiseTracker.objects.get_or_create(
            candidate=candidate,
            title="Follow up water authority meeting",
            defaults={"description": "Arrange a meeting with the water authority and ward leaders.", "made_by": "Maria Kila", "made_to": "Ward 1 residents", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "target_date": today + timedelta(days=14), "follow_up_owner": manager, "created_by": admin, "updated_by": admin},
        )
        Message.objects.get_or_create(
            candidate=candidate,
            subject="Ward visit prep",
            defaults={"sender": manager, "recipient_type": "Specific Ward", "recipient_group": "Ward 1", "body": "Confirm venue, leader acknowledgements, and issue notes before the visit.", "priority": "IMPORTANT", "status": "DRAFT", "read_receipt_required": True, "acknowledgement_required": True, "created_by": admin, "updated_by": admin},
        )
        polling_location, _ = PollingLocation.objects.get_or_create(
            candidate=candidate,
            name="Tokarara Primary School Booth",
            defaults={"province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "village": village_1, "assigned_scrutineer": scrutineer, "contact_number": scrutineer.phone, "status": "Ready", "transport_status": "Vehicle assigned", "created_by": admin, "updated_by": admin},
        )
        PollingStatus.objects.get_or_create(
            candidate=candidate,
            polling_location=polling_location,
            defaults={"reported_by": scrutineer, "scrutineer_present": True, "booth_open": False, "materials_available": True, "communication_ok": True, "created_by": admin, "updated_by": admin},
        )
        CitizenRequest.objects.get_or_create(
            candidate=candidate,
            title="Repair footbridge near market",
            defaults={"requester_name": "Tokarara Mothers Group", "phone": "+675 7444 1999", "province": province, "district": district_a, "llg": llg_a, "ward": ward_1, "village": village_1, "category": "Infrastructure", "description": "Community asks for support after election period to repair a footbridge.", "assigned_to": manager, "created_by": admin, "updated_by": admin},
        )
        if not AIWorkItem.objects.filter(candidate=candidate, ward=ward_1, work_type="WARD_BRIEF").exists():
            profile = WardProfile.objects.get(candidate=candidate, ward=ward_1)
            create_ward_ai_work_item(candidate, profile, admin)

        self.stdout.write(self.style.SUCCESS("Demo seeded. Login: admin / admin12345"))
