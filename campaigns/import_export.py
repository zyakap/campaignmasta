import csv
from io import StringIO

from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from .models import (
    CallLog,
    CampaignEvent,
    District,
    ExportRequest,
    ImportBatch,
    Influencer,
    LLG,
    PollingLocation,
    Province,
    Supporter,
    TeamMember,
    Ward,
    WardProfile,
)


def _read_csv(uploaded_file):
    uploaded_file.open("rb")
    content = uploaded_file.read().decode("utf-8-sig")
    uploaded_file.close()
    return list(csv.DictReader(StringIO(content)))


def _resolve_geography(row, candidate):
    province = Province.objects.filter(id=candidate.province_id).first()
    district = candidate.available_districts().filter(name__iexact=row.get("district", "").strip()).first()
    llg = candidate.available_llgs().filter(name__iexact=row.get("llg", "").strip()).first()
    ward = candidate.available_wards().filter(name__iexact=row.get("ward", "").strip()).first()
    village = None
    if ward:
        village = ward.villages.filter(name__iexact=row.get("village", "").strip()).first()
    return province, district, llg, ward, village


def validate_supporter_row(row, row_number):
    errors = []
    if not row.get("full_name"):
        errors.append("full_name is required")
    if row.get("consent_to_messages", "").lower() not in {"", "yes", "no", "true", "false", "1", "0"}:
        errors.append("consent_to_messages must be yes/no")
    return {"row": row_number, "errors": errors}


def process_import_batch(batch):
    rows = _read_csv(batch.uploaded_file)
    batch.total_rows = len(rows)
    errors = []
    imported = 0

    with transaction.atomic():
        if batch.import_type == ImportBatch.ImportType.SUPPORTERS:
            for index, row in enumerate(rows, start=2):
                result = validate_supporter_row(row, index)
                if result["errors"]:
                    errors.append(result)
                    continue
                province, district, llg, ward, village = _resolve_geography(row, batch.candidate)
                Supporter.objects.create(
                    candidate=batch.candidate,
                    full_name=row["full_name"].strip(),
                    phone=row.get("phone", "").strip(),
                    gender=row.get("gender", "").strip().upper() or "UNSPECIFIED",
                    age_range=row.get("age_range", "").strip(),
                    province=province,
                    district=district,
                    llg=llg,
                    ward=ward,
                    village=village,
                    clan=row.get("clan", "").strip(),
                    church_group=row.get("church_group", "").strip(),
                    occupation=row.get("occupation", "").strip(),
                    support_status=row.get("support_status", "UNKNOWN").strip().upper() or "UNKNOWN",
                    influence_level=row.get("influence_level", "LOW").strip().upper() or "LOW",
                    main_issue=row.get("main_issue", "").strip(),
                    consent_to_messages=row.get("consent_to_messages", "").lower() in {"yes", "true", "1"},
                    notes=row.get("notes", "").strip(),
                    created_by=batch.uploaded_by,
                    updated_by=batch.uploaded_by,
                )
                imported += 1

        elif batch.import_type == ImportBatch.ImportType.INFLUENCERS:
            for index, row in enumerate(rows, start=2):
                if not row.get("full_name"):
                    errors.append({"row": index, "errors": ["full_name is required"]})
                    continue
                province, district, llg, ward, village = _resolve_geography(row, batch.candidate)
                Influencer.objects.create(
                    candidate=batch.candidate,
                    full_name=row["full_name"].strip(),
                    phone=row.get("phone", "").strip(),
                    email=row.get("email", "").strip(),
                    province=province,
                    district=district,
                    llg=llg,
                    ward=ward,
                    village=village,
                    community_role=row.get("community_role", "").strip(),
                    influence_category=row.get("influence_category", "").strip(),
                    influence_level=row.get("influence_level", "MEDIUM").strip().upper() or "MEDIUM",
                    notes=row.get("notes", "").strip(),
                    created_by=batch.uploaded_by,
                    updated_by=batch.uploaded_by,
                )
                imported += 1

        elif batch.import_type == ImportBatch.ImportType.TEAM_MEMBERS:
            for index, row in enumerate(rows, start=2):
                if not row.get("full_name") or not row.get("role"):
                    errors.append({"row": index, "errors": ["full_name and role are required"]})
                    continue
                province, district, llg, ward, village = _resolve_geography(row, batch.candidate)
                TeamMember.objects.create(
                    candidate=batch.candidate,
                    full_name=row["full_name"].strip(),
                    phone=row.get("phone", "").strip(),
                    email=row.get("email", "").strip(),
                    role=row["role"].strip().upper(),
                    province=province,
                    district=district,
                    llg=llg,
                    ward=ward,
                    village=village,
                    notes=row.get("notes", "").strip(),
                    created_by=batch.uploaded_by,
                    updated_by=batch.uploaded_by,
                )
                imported += 1

        elif batch.import_type == ImportBatch.ImportType.WARD_DATA:
            for index, row in enumerate(rows, start=2):
                if not row.get("ward"):
                    errors.append({"row": index, "errors": ["ward is required"]})
                    continue
                ward = batch.candidate.available_wards().filter(name__iexact=row["ward"].strip()).first()
                if not ward:
                    errors.append({"row": index, "errors": [f"Ward '{row['ward']}' not found in this campaign"]})
                    continue
                WardProfile.objects.update_or_create(
                    candidate=batch.candidate,
                    ward=ward,
                    defaults={
                        "councillor_name": row.get("councillor_name", "").strip(),
                        "key_clans": row.get("key_clans", "").strip(),
                        "key_churches": row.get("key_churches", "").strip(),
                        "schools": row.get("schools", "").strip(),
                        "health_facilities": row.get("health_facilities", "").strip(),
                        "important_landmarks": row.get("important_landmarks", "").strip(),
                        "access_routes": row.get("access_routes", "").strip(),
                        "population_estimate": int(row["population_estimate"]) if row.get("population_estimate", "").strip().isdigit() else None,
                        "estimated_voting_population": int(row["estimated_voting_population"]) if row.get("estimated_voting_population", "").strip().isdigit() else None,
                        "support_strength": row.get("support_strength", "UNKNOWN").strip().upper() or "UNKNOWN",
                        "main_community_issues": row.get("main_community_issues", "").strip(),
                        "notes_for_candidate": row.get("notes_for_candidate", "").strip(),
                        "updated_by": batch.uploaded_by,
                    },
                )
                imported += 1

        elif batch.import_type == ImportBatch.ImportType.POLLING_LOCATIONS:
            for index, row in enumerate(rows, start=2):
                if not row.get("name"):
                    errors.append({"row": index, "errors": ["name is required"]})
                    continue
                province, district, llg, ward, village = _resolve_geography(row, batch.candidate)
                PollingLocation.objects.update_or_create(
                    candidate=batch.candidate,
                    name=row["name"].strip(),
                    defaults={
                        "province": province,
                        "district": district,
                        "llg": llg,
                        "ward": ward,
                        "village": village,
                        "gps_coordinates": row.get("gps_coordinates", "").strip(),
                        "contact_number": row.get("contact_number", "").strip(),
                        "notes": row.get("notes", "").strip(),
                        "updated_by": batch.uploaded_by,
                    },
                )
                imported += 1

    batch.valid_rows = imported
    batch.error_rows = len(errors)
    batch.validation_errors = errors
    if imported == 0 and errors:
        batch.status = "FAILED"
    else:
        batch.status = "IMPORTED"
    batch.save(update_fields=["total_rows", "valid_rows", "error_rows", "validation_errors", "status", "updated_at"])
    return batch


def _csv_response_file(name, headers, rows):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    filename = f"{name}-{timezone.localdate().isoformat()}.csv"
    return filename, ContentFile(buffer.getvalue().encode("utf-8"))


def build_export_file(export):
    candidate = export.candidate
    if export.export_type == ExportRequest.ExportType.SUPPORTERS:
        headers = ["full_name", "phone", "support_status", "influence_level", "ward", "village", "consent_to_messages"]
        rows = Supporter.objects.filter(candidate=candidate).select_related("ward", "village").values_list(
            "full_name", "phone", "support_status", "influence_level", "ward__name", "village__name", "consent_to_messages"
        )
        filename, content = _csv_response_file("supporters", headers, rows)
    elif export.export_type == ExportRequest.ExportType.CALLS:
        headers = ["person_called", "person_type", "caller", "call_datetime", "call_outcome", "follow_up_required", "next_call_due_date"]
        rows = CallLog.objects.filter(candidate=candidate).select_related("caller").values_list(
            "person_called", "person_type", "caller__full_name", "call_datetime", "call_outcome", "follow_up_required", "next_call_due_date"
        )
        filename, content = _csv_response_file("calls", headers, rows)
    elif export.export_type == ExportRequest.ExportType.WARDS:
        headers = ["ward", "support_strength", "population_estimate", "estimated_voting_population", "main_community_issues"]
        rows = WardProfile.objects.filter(candidate=candidate).select_related("ward").values_list(
            "ward__name", "support_strength", "population_estimate", "estimated_voting_population", "main_community_issues"
        )
        filename, content = _csv_response_file("wards", headers, rows)
    elif export.export_type == ExportRequest.ExportType.EVENTS:
        headers = ["title", "event_type", "ward", "venue", "start_datetime", "expected_crowd_size", "actual_attendance"]
        rows = CampaignEvent.objects.filter(candidate=candidate).select_related("ward").values_list(
            "title", "event_type", "ward__name", "venue", "start_datetime", "expected_crowd_size", "actual_attendance"
        )
        filename, content = _csv_response_file("events", headers, rows)
    elif export.export_type == ExportRequest.ExportType.POLLING:
        headers = ["name", "ward", "assigned_scrutineer", "status", "scrutineer_checked_in", "transport_status"]
        rows = PollingLocation.objects.filter(candidate=candidate).select_related("ward", "assigned_scrutineer").values_list(
            "name", "ward__name", "assigned_scrutineer__full_name", "status", "scrutineer_checked_in", "transport_status"
        )
        filename, content = _csv_response_file("polling-readiness", headers, rows)
    else:
        headers = ["team_member", "role", "phone", "district", "llg", "ward", "is_active"]
        rows = TeamMember.objects.filter(candidate=candidate).select_related("district", "llg", "ward").values_list(
            "full_name", "role", "phone", "district__name", "llg__name", "ward__name", "is_active"
        )
        filename, content = _csv_response_file("coordinator-performance", headers, rows)

    export.output_file.save(filename, content, save=False)
    export.status = "READY"
    export.save(update_fields=["output_file", "status", "updated_at"])
    return export
