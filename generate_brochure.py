#!/usr/bin/env python
"""
CampaignMasta — Marketing Brochure Generator
Produces a professional A4 PDF covering every feature of the platform.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

# ── Palette ──────────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#1A721A")
GREEN_MID   = colors.HexColor("#2AAA2A")
GREEN_LIGHT = colors.HexColor("#E8F8E8")
GREEN_PALE  = colors.HexColor("#F4FCF4")
MAROON      = colors.HexColor("#7C1C1C")
GOLD        = colors.HexColor("#BEA020")
CREAM       = colors.HexColor("#F5F2EC")
CREAM_DARK  = colors.HexColor("#EDE5D2")
INK         = colors.HexColor("#1A0C0C")
MUTED       = colors.HexColor("#7A6858")
LINE        = colors.HexColor("#DDD0B8")
WHITE       = colors.white

W, H = A4
MARGIN = 18 * mm

# ── Page background & header/footer ──────────────────────────────────────────
def on_page(canvas_obj, doc):
    canvas_obj.saveState()
    # Cream background
    canvas_obj.setFillColor(CREAM)
    canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)

    # Top bar — dark green
    canvas_obj.setFillColor(GREEN_DARK)
    canvas_obj.rect(0, H - 14 * mm, W, 14 * mm, fill=1, stroke=0)

    # Logo mark
    canvas_obj.setFillColor(GREEN_MID)
    canvas_obj.roundRect(MARGIN, H - 11 * mm, 8 * mm, 8 * mm, 1.5 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 7)
    canvas_obj.drawCentredString(MARGIN + 4 * mm, H - 7.5 * mm, "CM")

    # Brand name in topbar
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 9)
    canvas_obj.drawString(MARGIN + 10 * mm, H - 7.5 * mm, "CampaignMasta")

    # Page number in topbar
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.HexColor("#A8D8A8"))
    canvas_obj.drawRightString(W - MARGIN, H - 7.5 * mm,
        f"Page {doc.page}  |  campaignmasta.com")

    # Bottom bar
    canvas_obj.setFillColor(GREEN_DARK)
    canvas_obj.rect(0, 0, W, 10 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor("#A8D8A8"))
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawCentredString(W / 2, 3.5 * mm,
        "CampaignMasta — PNG Political Campaign Platform  |  campaignmasta.com  |  © 2025 WebMasta")

    canvas_obj.restoreState()


def on_first_page(canvas_obj, doc):
    canvas_obj.saveState()
    # Full green cover bleed top
    canvas_obj.setFillColor(GREEN_DARK)
    canvas_obj.rect(0, H - 88 * mm, W, 88 * mm, fill=1, stroke=0)
    # Subtle diagonal accent strip
    canvas_obj.setFillColor(colors.HexColor("#1E8A1E"))
    p = canvas_obj.beginPath()
    p.moveTo(0, H - 88 * mm)
    p.lineTo(W * 0.6, H - 88 * mm)
    p.lineTo(W * 0.45, H - 60 * mm)
    p.lineTo(0, H - 60 * mm)
    p.close()
    canvas_obj.drawPath(p, fill=1, stroke=0)
    # Gold accent bar
    canvas_obj.setFillColor(GOLD)
    canvas_obj.rect(0, H - 91 * mm, W, 3 * mm, fill=1, stroke=0)
    # Cream body
    canvas_obj.setFillColor(CREAM)
    canvas_obj.rect(0, 0, W, H - 91 * mm, fill=1, stroke=0)
    # Bottom bar
    canvas_obj.setFillColor(GREEN_DARK)
    canvas_obj.rect(0, 0, W, 10 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor("#A8D8A8"))
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawCentredString(W / 2, 3.5 * mm,
        "CampaignMasta — PNG Political Campaign Platform  |  campaignmasta.com  |  © 2025 WebMasta")
    canvas_obj.restoreState()


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        # Cover
        "cover_eyebrow": s("cover_eyebrow", fontName="Helvetica-Bold", fontSize=9,
            textColor=GOLD, spaceAfter=4, leading=12,
            leftIndent=MARGIN, spaceBefore=0),
        "cover_title": s("cover_title", fontName="Helvetica-Bold", fontSize=34,
            textColor=WHITE, spaceAfter=6, leading=40,
            leftIndent=MARGIN),
        "cover_sub": s("cover_sub", fontName="Helvetica", fontSize=13,
            textColor=colors.HexColor("#C8ECC8"), spaceAfter=10, leading=18,
            leftIndent=MARGIN),
        "cover_tagline": s("cover_tagline", fontName="Helvetica-Bold", fontSize=11,
            textColor=GOLD, spaceAfter=0, leading=16, leftIndent=MARGIN),

        # Body
        "doc_title": s("doc_title", fontName="Helvetica-Bold", fontSize=20,
            textColor=GREEN_DARK, spaceAfter=4, spaceBefore=10, leading=26),
        "section_label": s("section_label", fontName="Helvetica-Bold", fontSize=8,
            textColor=GREEN_MID, spaceAfter=3, spaceBefore=14, leading=11,
            textTransform="uppercase", letterSpacing=1.2),
        "h2": s("h2", fontName="Helvetica-Bold", fontSize=14,
            textColor=INK, spaceAfter=4, spaceBefore=6, leading=18),
        "h3": s("h3", fontName="Helvetica-Bold", fontSize=11,
            textColor=GREEN_DARK, spaceAfter=3, spaceBefore=8, leading=15),
        "body": s("body", fontName="Helvetica", fontSize=9.5,
            textColor=INK, spaceAfter=4, leading=14, alignment=TA_JUSTIFY),
        "body_small": s("body_small", fontName="Helvetica", fontSize=8.5,
            textColor=MUTED, spaceAfter=3, leading=12),
        "bullet": s("bullet", fontName="Helvetica", fontSize=9,
            textColor=INK, spaceAfter=2, leading=13,
            leftIndent=10, firstLineIndent=-10, bulletIndent=0),
        "bullet_green": s("bullet_green", fontName="Helvetica", fontSize=9,
            textColor=INK, spaceAfter=2, leading=13,
            leftIndent=12, firstLineIndent=-12),
        "caption": s("caption", fontName="Helvetica-Oblique", fontSize=8,
            textColor=MUTED, spaceAfter=2, leading=11, alignment=TA_CENTER),
        "toc_entry": s("toc_entry", fontName="Helvetica", fontSize=10,
            textColor=INK, spaceAfter=5, leading=14),
        "toc_num": s("toc_num", fontName="Helvetica-Bold", fontSize=10,
            textColor=GREEN_MID, spaceAfter=5, leading=14),
        "quote": s("quote", fontName="Helvetica-BoldOblique", fontSize=11,
            textColor=GREEN_DARK, spaceAfter=4, leading=16,
            leftIndent=8, borderPad=0),
        "feature_title": s("feature_title", fontName="Helvetica-Bold", fontSize=10,
            textColor=INK, spaceAfter=1, leading=13),
        "feature_body": s("feature_body", fontName="Helvetica", fontSize=9,
            textColor=MUTED, spaceAfter=0, leading=12),
        "white_bold": s("white_bold", fontName="Helvetica-Bold", fontSize=10,
            textColor=WHITE, spaceAfter=2, leading=14),
        "white_body": s("white_body", fontName="Helvetica", fontSize=9,
            textColor=colors.HexColor("#D0ECD0"), spaceAfter=2, leading=13),
        "cell_head": s("cell_head", fontName="Helvetica-Bold", fontSize=8.5,
            textColor=WHITE, spaceAfter=1, leading=12),
        "cell_body": s("cell_body", fontName="Helvetica", fontSize=8,
            textColor=INK, spaceAfter=1, leading=11),
    }


# ── Helper flowables ──────────────────────────────────────────────────────────
def rule(color=LINE, thickness=0.5, spBefore=4, spAfter=8):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=spAfter, spaceBefore=spBefore)

def sp(h=4):
    return Spacer(1, h * mm)

def section_header(st, num, title, subtitle=""):
    items = [
        Paragraph(f"0{num}" if num < 10 else str(num), st["section_label"]),
        Paragraph(title, st["h2"]),
    ]
    if subtitle:
        items.append(Paragraph(subtitle, st["body_small"]))
    items.append(rule(GREEN_MID, 1.2, 2, 6))
    return KeepTogether(items)

def feature_card(st, icon_char, title, body, badge=None):
    badge_html = f' <font color="#1A721A"><b> [{badge}]</b></font>' if badge else ""
    title_p = Paragraph(f"{icon_char}  {title}{badge_html}", st["feature_title"])
    body_p  = Paragraph(body, st["feature_body"])
    tbl = Table([[title_p], [body_p]], colWidths=[W - 2 * MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX",        (0, 0), (-1, -1), 0.5, LINE),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([tbl, sp(1.5)])

def two_col_features(st, items):
    """Render a list of (icon, title, body) tuples in a 2-column grid."""
    col = (W - 2 * MARGIN - 5 * mm) / 2
    rows = []
    for i in range(0, len(items), 2):
        left = _mini_card(st, items[i], col)
        right = _mini_card(st, items[i + 1], col) if i + 1 < len(items) else Paragraph("", st["body"])
        rows.append([left, right])
    tbl = Table(rows, colWidths=[col, col], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("COLPADDING",    (0, 0), (-1, -1), 3),
    ]))
    return tbl

def _mini_card(st, item, col_w):
    icon, title, body = item
    t = Paragraph(f"<b>{icon}  {title}</b>", ParagraphStyle("mc_t",
        fontName="Helvetica-Bold", fontSize=9, textColor=INK, leading=12, spaceAfter=2))
    b = Paragraph(body, ParagraphStyle("mc_b",
        fontName="Helvetica", fontSize=8, textColor=MUTED, leading=11, spaceAfter=0))
    inner = Table([[t], [b]], colWidths=[col_w - 10])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX",        (0, 0), (-1, -1), 0.4, LINE),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ]))
    return inner

def green_table(st, headers, rows, col_widths):
    data = [[Paragraph(h, st["cell_head"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), st["cell_body"]) for c in row])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  GREEN_DARK),
        ("BACKGROUND",    (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GREEN_PALE]),
        ("BOX",           (0, 0), (-1, -1), 0.5, LINE),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.3, LINE),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl

def highlight_box(st, text, bg=GREEN_LIGHT, border=GREEN_MID):
    p = Paragraph(text, ParagraphStyle("hb", fontName="Helvetica-BoldOblique",
        fontSize=10, textColor=GREEN_DARK, leading=15, spaceAfter=0))
    tbl = Table([[p]], colWidths=[W - 2 * MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("BOX",           (0, 0), (-1, -1), 1.5, border),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    return KeepTogether([tbl, sp(2)])

def dark_banner(st, title, subtitle):
    t = Paragraph(title, ParagraphStyle("db_t", fontName="Helvetica-Bold",
        fontSize=11, textColor=WHITE, leading=15, spaceAfter=3))
    s = Paragraph(subtitle, ParagraphStyle("db_s", fontName="Helvetica",
        fontSize=9, textColor=colors.HexColor("#C0E8C0"), leading=13, spaceAfter=0))
    tbl = Table([[t], [s]], colWidths=[W - 2 * MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GREEN_DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
    ]))
    return KeepTogether([tbl, sp(2)])


# ── Document build ────────────────────────────────────────────────────────────
def build():
    out = "/root/campaignmasta/CampaignMasta_Platform_Guide.pdf"
    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=20 * mm, bottomMargin=16 * mm,
        title="CampaignMasta — Complete Platform Guide",
        author="WebMasta",
        subject="CampaignMasta Software Platform — Full Feature Reference",
    )
    st = make_styles()
    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════════
    story += [
        sp(48),  # push below green band
        Paragraph("COMPLETE PLATFORM GUIDE", st["cover_eyebrow"]),
        Paragraph("CampaignMasta", st["cover_title"]),
        Paragraph("Papua New Guinea's Political Campaign Management Platform", st["cover_sub"]),
        Paragraph("Built for PNG. Designed to Win.", st["cover_tagline"]),
        sp(14),
    ]

    # Stats row on cover
    stats = [
        ["16+", "Feature Modules"],
        ["100%", "PNG-Focused"],
        ["Real-Time", "Polling War Room"],
        ["AI-Powered", "Ward Briefs & Speeches"],
    ]
    stat_tbl = Table(
        [[Paragraph(f"<b><font size='22' color='#2AAA2A'>{v}</font></b><br/>"
                    f"<font size='9' color='#7A6858'>{l}</font>", ParagraphStyle(
                    "stat", fontName="Helvetica", fontSize=9, alignment=TA_CENTER,
                    leading=14, spaceAfter=0))
          for v, l in stats]],
        colWidths=[(W - 2 * MARGIN) / 4] * 4
    )
    stat_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), WHITE),
        ("BOX",           (0, 0), (-1, -1), 0.5, LINE),
        ("LINEAFTER",     (0, 0), (2, 0),   0.5, LINE),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story += [stat_tbl, sp(6)]

    intro_p = Paragraph(
        "This document is a complete reference to every feature, module, and capability "
        "within the CampaignMasta platform. Whether you are a candidate evaluating the "
        "software, a campaign manager planning your operations, or a team coordinator "
        "learning the system — every function is explained here in full.",
        ParagraphStyle("intro", fontName="Helvetica", fontSize=10, textColor=MUTED,
            leading=15, alignment=TA_JUSTIFY, leftIndent=MARGIN, rightIndent=MARGIN,
            spaceAfter=0)
    )
    story += [intro_p, PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("TABLE OF CONTENTS", st["section_label"]))
    story.append(rule(GREEN_MID, 1.2, 2, 8))

    toc_items = [
        ("01", "Overview & Platform Philosophy"),
        ("02", "Dashboard & Campaign Metrics"),
        ("03", "Supporter Registry"),
        ("04", "Calls & Relationship Management"),
        ("05", "Messages & Team Communications"),
        ("06", "Tasks & Action Tracking"),
        ("07", "Events & Ward Visits"),
        ("08", "Ward Briefs & Local Intelligence"),
        ("09", "Community Issues & Promises"),
        ("10", "Polling Day War Room"),
        ("11", "Reports & Analytics"),
        ("12", "Data Operations — Import & Export"),
        ("13", "AI Assistant Tools"),
        ("14", "Team Management"),
        ("15", "PNG-Specific Features"),
        ("16", "Subscription, Billing & Modules"),
        ("17", "Settings, Connectors & Integrations"),
        ("18", "Usage, Credits & Billing"),
        ("19", "Security, Audit & Compliance"),
        ("20", "Technology & Deployment"),
    ]

    toc_rows = []
    for num, title in toc_items:
        toc_rows.append([
            Paragraph(f"<b>{num}</b>", ParagraphStyle("tn", fontName="Helvetica-Bold",
                fontSize=10, textColor=GREEN_MID, leading=14)),
            Paragraph(title, ParagraphStyle("te", fontName="Helvetica", fontSize=10,
                textColor=INK, leading=14)),
        ])

    toc_tbl = Table(toc_rows, colWidths=[12 * mm, W - 2 * MARGIN - 12 * mm])
    toc_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",  (0, 0), (-1, -1), [WHITE, GREEN_PALE]),
        ("TOPPADDING",      (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",   (0, 0), (-1, -1), 5),
        ("LEFTPADDING",     (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",    (0, 0), (-1, -1), 6),
        ("LINEBELOW",       (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN",          (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story += [toc_tbl, PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 01 — OVERVIEW
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 1, "Overview & Platform Philosophy",
        "What CampaignMasta is and how it helps PNG candidates win elections"))

    story.append(Paragraph(
        "CampaignMasta is a purpose-built digital command centre for Papua New Guinea election "
        "candidates. It covers the complete lifecycle of a campaign — from registering your first "
        "supporter to running a live polling day war room — all in a single, mobile-friendly platform "
        "designed specifically for PNG's unique political and geographic landscape.",
        st["body"]))
    story.append(sp(2))

    story.append(highlight_box(st,
        '"Every vote, every ward, every promise — tracked, managed, and acted on. '
        'CampaignMasta gives PNG candidates the professional infrastructure to run '
        'modern, data-driven campaigns."'))

    story.append(Paragraph("Who It Is Built For", st["h3"]))
    for line in [
        "<b>District Open Candidates</b> — managing one district across multiple LLGs and wards",
        "<b>Provincial Candidates</b> — managing an entire province with full district rollup reporting",
        "<b>Campaign Managers</b> — coordinating team, outreach, and data across the full operation",
        "<b>District & LLG Coordinators</b> — tracking supporters and events in their zone",
        "<b>Ward Coordinators & Scrutineers</b> — reporting from the ground on polling day",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("Core Design Principles", st["h3"]))
    principles = [
        ("Mobile-First", "Works on any Android or iOS phone, no laptop required"),
        ("PNG Geography Built-In", "Province → District → LLG → Ward → Village hierarchy pre-loaded"),
        ("Role-Based Access", "Each team member sees only what their role allows"),
        ("Audit Trail", "Every action is logged — who did what, and when"),
        ("Offline-Ready Android App", "Native mobile app for field use with or without internet"),
        ("AI-Assisted", "Generate ward briefs and speech notes automatically from your data"),
    ]
    story.append(two_col_features(st, [(a, a, b) for a, b in principles]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 02 — DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 2, "Dashboard & Campaign Metrics",
        "The live pulse of your campaign — everything at a glance"))

    story.append(Paragraph(
        "The Dashboard is the first screen every team member sees after login. It shows a real-time "
        "snapshot of your entire campaign so you can instantly see what needs attention, what is going "
        "well, and what is overdue.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Live Metric Cards", st["h3"]))
    metrics = [
        ["Metric", "What It Shows", "Why It Matters"],
        ["Total Supporters", "Number of people registered in your database", "Track growth of your registered base"],
        ["Strong Supporters", "Count with 'Strong Supporter' status", "Your confirmed vote block"],
        ["Undecided Contacts", "Count still undecided", "Persuasion targets — needs follow-up"],
        ["SMS Consented", "People who agreed to receive messages", "Your legal messaging audience"],
        ["Weak Wards", "Wards with low support strength", "Geography needing urgent attention"],
        ["Overdue Tasks", "Tasks past their due date", "Operational gaps requiring action"],
        ["Open Issues", "Unresolved community issues", "Local concerns you must address"],
        ["Pending Promises", "Promises not yet delivered", "Accountability tracker"],
        ["Polling Incidents", "Active open incidents from polling locations", "Election day risk monitor"],
    ]
    story.append(green_table(st, metrics[0], metrics[1:],
        [45*mm, 75*mm, 55*mm]))
    story.append(sp(3))

    story.append(Paragraph("Dashboard Panels", st["h3"]))
    panels = [
        ("Calls Due Today", "Lists influencers and contacts whose next scheduled call is today or overdue. Quiet coordinators are highlighted. Direct link to log each call."),
        ("Open Tasks", "Shows the 8 highest-priority tasks by due date. Colour-coded by urgency. One-click to create a new task."),
        ("Upcoming Events", "Next 5 ward visits, rallies, and meetings. Click through to event detail and talking points."),
        ("Open Issues", "Latest community issues needing response. Category and priority shown at a glance."),
        ("Prepaid Credit Alert", "If any service wallet (SMS, AI, WhatsApp) is running low, an alert appears here before you run out mid-campaign."),
    ]
    for name, desc in panels:
        story.append(feature_card(st, "▸", name, desc))

    story.append(Paragraph("Quick Actions", st["h3"]))
    story.append(Paragraph(
        "From the dashboard, one tap takes you directly to: Register supporter · Record call · "
        "Compose message · Create task · Plan event · Record issue · Submit polling status · "
        "View reports · Check usage balance.",
        st["body"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 03 — SUPPORTERS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 3, "Supporter Registry",
        "Your most important asset — every voter who has committed to you"))

    story.append(Paragraph(
        "The Supporter Registry is the heart of your campaign database. Every person who has "
        "expressed support is recorded here with full contact details, geographic location, "
        "demographic data, and support status. The system detects and flags potential duplicate "
        "entries automatically.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("What You Can Record Per Supporter", st["h3"]))
    fields = [
        ["Field", "Details"],
        ["Full Name", "Up to 160 characters"],
        ["Gender", "Female / Male / Other / Unspecified"],
        ["Age Range", "Flexible text field (e.g. '35–45')"],
        ["Phone Number", "Primary contact number"],
        ["Geographic Location", "Province → District → LLG → Ward → Village"],
        ["Clan", "Clan or tribal affiliation"],
        ["Church / Community Group", "Primary group affiliation"],
        ["Occupation", "Employment or community role"],
        ["Enrollment Status", "Verified Enrolled / Needs Re-enrolment / Unknown"],
        ["Support Status", "Strong / Leaning / Undecided / Not Supportive / Unknown"],
        ["Influence Level", "High / Medium / Low — how much sway they have in their community"],
        ["Introduced By", "Which team member brought them in"],
        ["Main Issue", "What issue matters most to this person"],
        ["Follow-Up Required", "Flag + scheduled follow-up date"],
        ["SMS Consent", "Has this person agreed to receive messages"],
        ["Registered By", "Which team member recorded this entry"],
        ["Notes", "Free-text additional notes"],
    ]
    story.append(green_table(st, fields[0], fields[1:], [55*mm, 115*mm]))
    story.append(sp(3))

    story.append(Paragraph("Key Capabilities", st["h3"]))
    for line in [
        "Search by name, phone number, or village — results appear instantly",
        "Automatic duplicate detection: system warns if a record with the same name, phone, ward, and village already exists",
        "Filter supporters by ward, status, influence level, or follow-up flag",
        "Bulk import via CSV (see Data Operations section)",
        "Export supporter lists for offline use or external reporting",
        "Each supporter links to their call history, messages received, and events attended",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 04 — CALLS & INFLUENCERS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 4, "Calls & Relationship Management",
        "Never miss a key contact — track every conversation with influencers and supporters"))

    story.append(Paragraph(
        "Campaigns are won through relationships. The Calls module ensures that every important "
        "person — community leaders, church elders, business owners, clan heads — is contacted "
        "on schedule. The system automatically calculates when each person is next due for a call "
        "and alerts you when follow-up is overdue.",
        st["body"]))
    story.append(sp(2))

    story.append(dark_banner(st, "The Influencer CRM",
        "Track your most important relationships with built-in contact frequency scheduling, "
        "influence scoring, and call outcome logging."))

    story.append(Paragraph("Influencer Profile Fields", st["h3"]))
    inf_fields = [
        ["Field", "Details"],
        ["Full Name + Photo", "Identity with optional profile photo"],
        ["Phone & Alternative Phone", "Primary and backup contact numbers"],
        ["Email", "Electronic contact"],
        ["Geographic Location", "Province → District → LLG → Ward → Village"],
        ["Community Role", "e.g. Village Elder, Church Pastor, Market Organiser"],
        ["Influence Category", "e.g. Clan Head, Women's Leader, Business Owner"],
        ["Influence Level", "High / Medium / Low"],
        ["Estimated Network Size", "Approximate number of people they can influence"],
        ["Relationship Status", "Strong / Medium / Weak / Unknown"],
        ["Preferred Contact Method", "Call / SMS / WhatsApp / Visit"],
        ["Contact Frequency", "Days between contacts — High=7, Medium=14, Low=30 (configurable)"],
        ["Last Call / Meeting / Message Date", "Auto-updated when activity logged"],
        ["Next Contact Due Date", "Auto-calculated from last contact + frequency"],
        ["Assigned Owner", "Which team member is responsible for this relationship"],
        ["Influence Score", "Computed score (30–100) from level, network size, and relationship"],
    ]
    story.append(green_table(st, inf_fields[0], inf_fields[1:], [60*mm, 110*mm]))
    story.append(sp(3))

    story.append(Paragraph("Call Log — What Gets Recorded", st["h3"]))
    call_fields = [
        ("Call Outcome", "Answered / Missed / Call Back / Switched Off / Wrong Number"),
        ("Discussion Summary", "Full text of what was discussed"),
        ("Issues Raised", "Any community problems the person raised"),
        ("Commitments Made", "What the candidate or team committed to"),
        ("Follow-Up Required", "Flag + specific follow-up date"),
        ("Call Duration", "How long the conversation lasted"),
        ("Caller", "Which team member made the call"),
    ]
    for name, desc in call_fields:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(2))
    story.append(Paragraph("Automated Behaviours", st["h3"]))
    for line in [
        "When a call is logged, the influencer's Last Call Date and Next Contact Due Date update automatically",
        "The dashboard Calls Due panel surfaces everyone who is overdue or due today",
        "Quiet coordinator alerts: if a coordinator has not logged any activity recently, an escalation flag appears",
        "High influence contacts default to 7-day recall; Medium to 14 days; Low to 30 days — all configurable",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 05 — MESSAGES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 5, "Messages & Team Communications",
        "Reach your team, supporters, and influencers through one unified messaging centre"))

    story.append(Paragraph(
        "The Messages module lets you compose and send communications to any subset of your "
        "network — by geography, by role, or to individual people. Every message is tracked: "
        "who received it, who read it, and who acknowledged it.",
        st["body"]))
    story.append(sp(2))

    msg_features = [
        ("Message Types", "Standard, Polling Day Reminder, Preference Instructions, Constituency Newsletter"),
        ("Recipient Targeting", "All Team, Specific LLG, Specific Ward, All Supporters, custom groups"),
        ("Delivery Channels", "In-App, SMS, Email, WhatsApp — per message"),
        ("Priority Levels", "Normal / Important / Urgent — controls urgency display"),
        ("Scheduled Sending", "Set a future date and time for delivery"),
        ("Attachments", "Attach documents, images, or PDF files"),
        ("Read Receipts", "Track who has read each message"),
        ("Acknowledgement", "Require team members to formally acknowledge critical messages"),
        ("Draft Mode", "Save as draft before sending, preview recipient count"),
        ("Consent Enforcement", "Only sends to supporters who have given consent to receive messages"),
    ]
    for name, desc in msg_features:
        story.append(feature_card(st, "✉", name, desc))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 06 — TASKS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 6, "Tasks & Action Tracking",
        "Assign, monitor, and complete every campaign action item"))

    story.append(Paragraph(
        "Tasks keep your campaign moving. Every action that needs doing — from arranging "
        "transport for a ward visit to following up on a community promise — is created as a "
        "task, assigned to a team member, given a priority, and tracked to completion.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph(
        "Tasks keep your campaign moving. Every action that needs doing — from arranging "
        "transport for a ward visit to following up on a community promise — is created as a "
        "task, assigned to a team member, given a priority, and tracked to completion.",
        st["body"]))
    story.append(sp(2))

    task_grid = [
        ("Priority", "Low / Normal / High / Urgent", "Colour-coded urgency in all views"),
        ("Status", "Pending / In Progress / Completed / Overdue / Cancelled", "Full lifecycle tracking"),
        ("Geographic Scope", "Province → District → LLG → Ward", "Spatial ownership of tasks"),
        ("Due Date", "Specific date for completion", "Dashboard shows overdue tasks immediately"),
        ("Attachment", "Upload any file (photo, PDF, document)", "Context for whoever picks it up"),
        ("Completion Notes", "Free text when marking done", "Evidence of what was done"),
        ("Assigned By / To", "Full team member trail", "Accountability at every level"),
    ]
    tdata = [["Field", "Options / Detail", "Purpose"]] + task_grid
    story.append(green_table(st, tdata[0], tdata[1:], [40*mm, 80*mm, 55*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 07 — EVENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 7, "Events & Ward Visits",
        "Plan, manage, and record every campaign appearance"))

    story.append(Paragraph(
        "From a village meeting to a full rally, every campaign appearance is planned and "
        "tracked in the Events module. Each event has its own logistics checklist, attendance "
        "register, and post-event report — building a permanent record of your entire campaign trail.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Event Types & Venue Types", st["h3"]))
    ev_tbl = Table([
        [Paragraph("<b>Event Types</b>", st["cell_head"]),
         Paragraph("<b>Venue Types</b>", st["cell_head"])],
        [Paragraph("Ward Visit, Rally, Meeting\nFundraiser, Awareness, Polling Training",
                   st["cell_body"]),
         Paragraph("Market Day, Church Service, Roadside Rally\nVillage Meeting, Feast / Mumu, Formal Hall, Other",
                   st["cell_body"])],
    ], colWidths=[(W - 2*MARGIN)/2]*2)
    ev_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), GREEN_DARK),
        ("BACKGROUND",    (0, 1), (-1, -1), WHITE),
        ("BOX",           (0, 0), (-1, -1), 0.5, LINE),
        ("LINEAFTER",     (0, 0), (0, -1), 0.5, LINE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story += [ev_tbl, sp(3)]

    story.append(Paragraph("What Gets Planned Per Event", st["h3"]))
    for line in [
        "<b>Talking Points</b> — candidate briefing notes for this specific audience",
        "<b>Issues to Address</b> — community concerns to acknowledge",
        "<b>People to Acknowledge</b> — clan elders, church leaders, local identities",
        "<b>Host Person</b> — who is organising or hosting the event",
        "<b>Security Notes</b> — any safety considerations",
        "<b>Logistics Checklist</b> — itemised to-do list with team assignments",
        "<b>Ward Coverage</b> — which wards will have people attending (links to speech suggestions)",
        "<b>Expected vs Actual Attendance</b> — crowd size planning and reporting",
        "<b>Attendance Register</b> — check people in on the day with name, phone, village",
        "<b>Photos & Videos</b> — upload media from the event",
        "<b>Event Report</b> — post-event narrative and observations",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 08 — WARD BRIEFS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 8, "Ward Briefs & Local Intelligence",
        "Know every ward before you arrive — intelligence that wins votes"))

    story.append(Paragraph(
        "The Ward Briefs module is your intelligence database. Before visiting any ward, "
        "your team builds a comprehensive profile covering population, community groups, key "
        "people to acknowledge, local issues, infrastructure, access routes, and historical "
        "voting patterns. When you arrive, you already know the ward.",
        st["body"]))
    story.append(sp(2))

    story.append(dark_banner(st, "Ward Intelligence = Confidence on the Ground",
        "Candidates who know the ward's clan structure, the councillor's name, the top issue, "
        "and who the church elder is make a far stronger impression than those who arrive unprepared."))

    story.append(Paragraph("Complete Ward Profile Fields", st["h3"]))
    wb_fields = [
        ["Category", "Fields"],
        ["People", "Councillor name, key clans, important families"],
        ["Community Groups", "Youth groups, women's groups, church groups, business groups"],
        ["Infrastructure", "Schools, markets, health facilities, important landmarks, access routes, meeting places"],
        ["Population", "Population estimate, estimated voting population"],
        ["Political", "Support strength (Strong/Medium/Weak/Unknown), previous election notes, security concerns"],
        ["Issues", "Main community issues (linked to Issues module)"],
        ["Candidate Brief", "Notes for candidate — talking points, sensitivities, commitments"],
    ]
    story.append(green_table(st, wb_fields[0], wb_fields[1:], [50*mm, 120*mm]))
    story.append(sp(3))

    story.append(Paragraph("Ward Brief Detail View", st["h3"]))
    story.append(Paragraph(
        "When you open a ward brief, the system assembles a live dashboard from your data:",
        st["body"]))
    for line in [
        "Current supporter count and undecided count for this ward",
        "Key influencers to acknowledge, with their role",
        "All open community issues linked to this ward",
        "Open promises made in this ward and their delivery status",
        "Upcoming and past events held in this ward",
        "Landmarks, access routes, and meeting places",
        "AI-generated ward brief and speech notes (if AI module enabled)",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 09 — ISSUES & PROMISES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 9, "Community Issues & Promises",
        "Track what your communities need and ensure you deliver on your word"))

    story.append(Paragraph(
        "Papua New Guinea voters have specific, local concerns — road access, school facilities, "
        "water supply, health services. The Issues and Promises modules ensure every concern is "
        "recorded, every commitment is tracked, and nothing falls through the cracks.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Community Issues", st["h3"]))
    iss_fields = [
        ("Title & Category", "What the issue is and how it is classified"),
        ("Geographic Location", "Province → District → LLG → Ward → Village — precisely where the issue is"),
        ("Priority", "Low / Normal / High / Urgent — ranked by urgency"),
        ("Status", "New → Under Review → Follow Up → Resolved / Deferred"),
        ("Reported By", "Who raised the issue (community member name)"),
        ("Related Event", "Which ward visit or rally surfaced this issue"),
        ("Related Influencer", "Community leader associated with this concern"),
        ("Photos", "Photographic evidence of the issue"),
    ]
    for name, desc in iss_fields:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("Promise Tracker", st["h3"]))
    story.append(Paragraph(
        "Every commitment a candidate makes — whether at a village meeting or in a formal "
        "event — is recorded in the Promise Tracker with a delivery date and assigned follow-up owner.",
        st["body"]))
    story.append(sp(2))

    prom_fields = [
        ["Promise Category", "Infrastructure, Education, Health, Water & Sanitation, Economic, Services, Other"],
        ["Made By / Made To", "Candidate or team member name, recipient group or individual"],
        ["Geographic Scope", "Province → District → LLG → Ward"],
        ["Promise Date", "When the commitment was made"],
        ["Target Date", "When it should be delivered"],
        ["Status", "Open → In Progress → Delivered / Cancelled / Deferred"],
        ["Delivery Evidence", "Upload receipt, photo, or official document when fulfilled"],
        ["Public Facing", "Mark delivered promises as visible on the public constituency page"],
        ["Follow-Up Owner", "Team member accountable for chasing delivery"],
    ]
    story.append(green_table(st, ["Field", "Detail"],
        prom_fields, [55*mm, 115*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10 — POLLING DAY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 10, "Polling Day War Room",
        "Real-time command and control on election day"))

    story.append(Paragraph(
        "Polling day is the most critical 12 hours of the entire campaign. CampaignMasta's "
        "Polling War Room gives your campaign a live operations centre — tracking every booth, "
        "every scrutineer, every tally, and every incident in real time from a central command dashboard.",
        st["body"]))
    story.append(sp(2))

    story.append(highlight_box(st,
        "The Polling Command Centre aggregates live tally counts from all booths, shows "
        "scrutineer check-in status, flags security risks, and surfaces unresolved incidents "
        "— all updating in real time as your scrutineers submit reports from the field."))

    story.append(Paragraph("Polling Location Setup", st["h3"]))
    pl_fields = [
        ("Location Name & GPS Coordinates", "Exact booth identification and mapping"),
        ("Primary & Backup Scrutineer", "Two assigned team members per booth"),
        ("Security Risk Level", "Low / Moderate / High / Refused access"),
        ("Expected Turnout", "Forecast number of voters"),
        ("Historical Vote Data", "Previous election results stored per booth (e.g. 2022: Our Candidate 340, Opponent 120)"),
        ("Transport Status", "Whether scrutineer has transport confirmed"),
    ]
    for name, desc in pl_fields:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("Live Booth Status Reports", st["h3"]))
    story.append(Paragraph(
        "Scrutineers submit status updates throughout polling day. Each update captures:", st["body"]))
    status_items = [
        ["Data Point", "What It Confirms"],
        ["Scrutineer Present", "Your representative is physically at the booth"],
        ["Booth Open", "Voting is underway"],
        ["Materials Available", "Ballot boxes and papers are in order"],
        ["Communication OK", "Scrutineer has working phone signal"],
        ["Our Tally", "Running count of observed votes for your candidate"],
        ["Transport Notes", "Any issues with scrutineer or voter transport"],
        ["Logistical Issues", "Any operational problems at the booth"],
        ["Notes", "Free-text situation report"],
    ]
    story.append(green_table(st, status_items[0], status_items[1:],
        [60*mm, 110*mm]))
    story.append(sp(3))

    story.append(Paragraph("Incident Reporting", st["h3"]))
    story.append(Paragraph(
        "Any polling irregularity, security concern, or logistical problem is reported as an "
        "incident. Each incident has a priority level (Normal / High / Urgent) and a status "
        "(Open → In Progress → Resolved). The War Room dashboard shows all open incidents "
        "prominently so the command team can respond immediately.",
        st["body"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 11 — REPORTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 11, "Reports & Analytics",
        "Data-driven decision-making across your entire campaign"))

    story.append(Paragraph(
        "The Reports module gives candidates and campaign managers a geographic rollup of "
        "campaign performance. See where you are strong, where you are weak, and where effort "
        "is needed — broken down by District, LLG, and Ward.",
        st["body"]))
    story.append(sp(2))

    report_items = [
        ("Geographic Rollup", "Supporter counts grouped by District → LLG → Ward with strong vs undecided split"),
        ("Ward Support Map", "Support strength rating per ward — quickly identify weak areas"),
        ("Supporter Growth", "Track how your registered base grows over the campaign period"),
        ("Engagement Metrics", "Messages sent, read rates, call completion rates"),
        ("Polling Location Summary", "Booth-by-booth tally summary from polling day"),
        ("Export Capability", "Download supporter lists, call logs, ward data, event records, polling reports"),
    ]
    for name, desc in report_items:
        story.append(feature_card(st, "■", name, desc))

    story.append(Paragraph("Export System", st["h3"]))
    story.append(Paragraph(
        "Exports can be controlled — standard users submit an export request, which a senior "
        "manager approves before the file is generated. Superusers receive instant approval. "
        "Available export types: Supporters, Calls, Wards, Events, Messages, Polling, Team.",
        st["body"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 12 — DATA OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 12, "Data Operations — Import & Export",
        "Bulk load your existing data and extract what you need"))

    story.append(Paragraph(
        "If you have existing supporter lists, team member records, or ward data in a spreadsheet, "
        "you can bulk import them directly into CampaignMasta. The import system validates every "
        "row and reports exactly which records succeeded and which had errors — no silent failures.",
        st["body"]))
    story.append(sp(2))

    import_types = [
        ["Import Type", "What Gets Imported"],
        ["Supporters", "Full supporter profiles from CSV"],
        ["Team Members", "Coordinator and volunteer records"],
        ["Influencers", "CRM contacts with roles and ward assignments"],
        ["Ward Data", "Community issues, ward profile information"],
        ["Polling Locations", "Booth locations with scrutineer assignments"],
        ["Geography", "Custom province/district/LLG/ward/village data"],
    ]
    story.append(green_table(st, import_types[0], import_types[1:],
        [55*mm, 115*mm]))
    story.append(sp(3))

    story.append(Paragraph("Import Validation", st["h3"]))
    for line in [
        "Every row is validated before import — required fields, format checks, geographic lookups",
        "Import summary shows: Total Rows / Valid Rows / Error Rows",
        "Error detail report shows exactly which rows failed and why",
        "Import history is preserved so you can track all bulk operations and who performed them",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 13 — AI TOOLS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 13, "AI Assistant Tools",
        "Generate ward briefs and campaign speeches automatically from your own data"))

    story.append(Paragraph(
        "The AI module uses your own campaign data — ward profiles, supporter counts, community "
        "issues, influencer relationships, events, and promises — to automatically generate draft "
        "ward visit briefs and speech notes. Every AI output goes through human review before use.",
        st["body"]))
    story.append(sp(2))

    story.append(dark_banner(st, "AI That Knows Your Campaign",
        "Unlike generic AI tools, CampaignMasta's AI uses the actual data in your campaign "
        "database — your wards, your supporters, your issues, your promises — to generate "
        "content that is relevant, accurate, and specific to your campaign."))

    story.append(Paragraph("AI Work Item Types", st["h3"]))
    ai_types = [
        ("Ward Brief", "A full pre-visit briefing document for a specific ward — population, issues, key people, talking points, supporter counts, historical notes"),
        ("Speech Notes", "Talking points for a specific event or ward visit, drawing on local issues, community groups, and promises made in that area"),
        ("Daily Summary", "Campaign summary covering activities, calls due, and key priorities"),
        ("Call Suggestions", "Recommended talking points for upcoming calls with specific influencers"),
        ("Issue Trends", "Analysis of community issues across wards to identify campaign themes"),
        ("Message Draft", "Suggested message content for outreach to supporters or team"),
        ("Event Report", "Post-event summary draft from attendance and notes"),
    ]
    for name, desc in ai_types:
        story.append(feature_card(st, "✦", name, desc))

    story.append(Paragraph("Human Review Workflow", st["h3"]))
    story.append(Paragraph(
        "Every AI-generated item enters a review queue. A senior team member reads the output, "
        "can edit it, and marks it Approved or Rejected with notes. Only approved content is "
        "used. This ensures AI assists — it does not replace — the candidate's judgment.",
        st["body"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 14 — TEAM MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 14, "Team Management",
        "Build your hierarchy from candidate to village coordinator"))

    story.append(Paragraph(
        "CampaignMasta mirrors the structure of a PNG campaign operation — from the candidate "
        "at the top down to ward coordinators and scrutineers on the ground. Each role has "
        "defined access to the data in their geographic area.",
        st["body"]))
    story.append(sp(2))

    roles = [
        ["Role", "Geographic Scope", "Typical Responsibilities"],
        ["Candidate", "Full electorate", "Platform owner, all access"],
        ["Campaign Manager", "Full electorate", "Oversee all operations, approve exports"],
        ["IT Admin", "Full electorate", "Manage connectors, settings, data ops"],
        ["District Coordinator", "District (Provincial only)", "Manage LLG coordinators, district reporting"],
        ["LLG Coordinator", "LLG area", "Coordinate ward teams, track ward activities"],
        ["Ward Coordinator", "Single ward", "Register supporters, record calls, report events"],
        ["Village Coordinator", "Single village", "Ground-level data collection"],
        ["Volunteer", "Assigned area", "Data entry and field registration"],
        ["Scrutineer", "Single polling location", "Submit polling day status reports"],
    ]
    story.append(green_table(st, roles[0], roles[1:], [45*mm, 45*mm, 85*mm]))
    story.append(sp(3))

    story.append(Paragraph("Team Member Provisioning", st["h3"]))
    for line in [
        "Each team member can optionally be given a login account (username + password) to access the platform",
        "Team members without logins can still be referenced in call logs, tasks, messages, and events",
        "Password reset is available from the team member edit screen",
        "Active/Inactive flag — deactivate team members who leave without deleting their history",
        "Profile photo support for easy identification",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 15 — PNG-SPECIFIC FEATURES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 15, "PNG-Specific Features",
        "Built for Papua New Guinea's unique political and cultural landscape"))

    story.append(Paragraph(
        "CampaignMasta includes features found in no generic CRM — built specifically for the "
        "way PNG elections work, from Limited Preferential Voting mechanics to DSIP fund tracking "
        "and community feast logging.",
        st["body"]))
    story.append(sp(2))

    png_modules = [
        ("Preference Deals (LPV)",
         "Papua New Guinea uses Limited Preferential Voting — voters choose 1st, 2nd, and 3rd preference candidates. "
         "The Preference Deals module tracks formal agreements with other candidates to direct their supporters' 2nd "
         "or 3rd preference votes to you. Record partner name, seat, preference number (2nd or 3rd), ward-level "
         "directives, deal terms, and status (Verbal / Agreed / Broken / Inactive)."),
        ("Community Groups",
         "Track clans, church congregations, women's groups, youth clubs, sports clubs, and business associations by "
         "ward. For each group record estimated voting members, current alignment (Strong Support / Leaning / Neutral / "
         "Leaning Away), and the key contact influencer. Know which groups support you before every ward visit."),
        ("Community Assistance Log",
         "Record every act of community assistance — a feast, school materials, tools, medical supplies, transport, "
         "infrastructure contribution — with the recipient group, PGK value, approval chain, and related event. "
         "This creates a transparent, auditable record of community engagement."),
        ("Competitor Intelligence",
         "Track what your opponents are doing. Log their ward visits, promises, rallies, preference deals, and "
         "distributions. For each activity record the source (Confirmed / Social Media / Media Report / Rumour), "
         "and assign a response action to a team member. Stay ahead of the opposition."),
        ("Development Fund Tracking (DSIP/SDP)",
         "Members of Parliament allocate District Services Improvement Programme (DSIP) and Special Development "
         "Programme (SDP) funds. Track total allocation vs amount spent per ward and district. Show communities "
         "what funds were invested in their area — or hold sitting members accountable for unspent allocations."),
        ("Voter Registration Drives",
         "Organise and track voter enrolment drives by ward. Set a target count, assign team members, run the "
         "drive, and record actual enrolments. Enrolled voters are potential supporters — registration drives "
         "are a direct vote-building strategy in PNG."),
    ]
    for name, desc in png_modules:
        story.append(Paragraph(name, st["h3"]))
        story.append(Paragraph(desc, st["body"]))
        story.append(sp(2))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 16 — SUBSCRIPTION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 16, "Subscription, Billing & Modules",
        "Flexible plans built around what each campaign actually needs"))

    story.append(Paragraph(
        "CampaignMasta is sold as a modular platform. You can subscribe to individual modules, "
        "purchase bundled packages at a discount, or take the Full Package for complete access. "
        "All pricing is in Papua New Guinea Kina (PGK).",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Subscription Plans", st["h3"]))
    plans = [
        ["Plan", "Suitable For", "Billing Options"],
        ["Starter", "Small district campaign, limited budget, core functions only",
         "Monthly / Quarterly / Annual / Campaign Period"],
        ["Professional", "Active district or provincial campaign with full team",
         "Monthly / Quarterly / Annual / Campaign Period"],
        ["Full Package", "Maximum capacity campaign — every module unlocked",
         "Campaign Period (flat rate)"],
    ]
    story.append(green_table(st, plans[0], plans[1:], [35*mm, 85*mm, 55*mm]))
    story.append(sp(3))

    story.append(Paragraph("Module Categories", st["h3"]))
    mod_cats = [
        ("Foundation", "Core platform — team, geography, settings, dashboard"),
        ("Field", "Supporter registration, events, ward visits"),
        ("CRM", "Influencer management, calls, relationship tracking"),
        ("Messaging", "In-app, SMS, WhatsApp, email messaging"),
        ("Intelligence", "Ward briefs, issues, competitor tracking, reports"),
        ("Polling", "Polling day war room, scrutineer management, live tallies"),
        ("AI", "AI ward briefs, speech notes, automated summaries"),
        ("Constituency", "Post-election mode — community assistance, development funds, promises"),
        ("Platform", "Data operations, advanced reporting, API access"),
    ]
    for name, desc in mod_cats:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("Quoting & Acceptance", st["h3"]))
    story.append(Paragraph(
        "Generate a formal quote by selecting modules and/or bundles, choosing a billing cycle, "
        "and reviewing the total with any applicable bundle discounts. Quotes show standalone "
        "cost vs bundle price so you can see exactly what you save. Accept the quote to activate "
        "the modules immediately.",
        st["body"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 17 — SETTINGS & CONNECTORS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 17, "Settings, Connectors & Integrations",
        "Configure the platform to match your campaign's operations"))

    story.append(Paragraph(
        "Campaign Settings let you control how the platform behaves. Connectors link "
        "CampaignMasta to external services — SMS gateways, WhatsApp Business, email providers, "
        "AI services, and payment systems.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Campaign Settings", st["h3"]))
    settings_items = [
        ("SMS Sender Name", "The name that appears on outgoing SMS messages"),
        ("Call Frequency Defaults", "Configurable recall intervals for High/Medium/Low influence contacts"),
        ("Export Approval Requirement", "Require manager approval before data exports are generated"),
        ("AI Assistant Enabled", "Enable or disable AI features for the campaign"),
        ("Polling Day Mode", "Switch the dashboard to polling-day focused view"),
        ("Constituency Mode", "Post-election mode — shifts platform focus from campaigning to community service"),
    ]
    for name, desc in settings_items:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("Connector Types", st["h3"]))
    conn_types = [
        ["Connector", "Provider Examples", "What It Enables"],
        ["AI", "OpenAI, Anthropic, local models", "Ward brief and speech generation, AI summaries"],
        ["WhatsApp", "WhatsApp Business API", "Send messages via WhatsApp to supporters and team"],
        ["SMS", "Local PNG SMS gateways", "Send bulk SMS to consented supporters"],
        ["Email", "Any SMTP server", "Email notifications and message delivery"],
        ["Maps", "Google Maps API", "GPS-based landmark and location services"],
        ["Payment", "BSP, ANZ, online gateways", "Process campaign fees and subscriptions"],
        ["Storage", "S3-compatible", "Secure file storage for photos and documents"],
        ["Webhook", "Any HTTP endpoint", "Push events to external systems"],
    ]
    story.append(green_table(st, conn_types[0], conn_types[1:],
        [30*mm, 45*mm, 100*mm]))
    story.append(sp(2))
    story.append(Paragraph(
        "Every connector can be tested from within the platform. The test runs a health check "
        "against the configured credentials and reports success or failure with diagnostic details.",
        st["body"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 18 — USAGE & CREDITS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 18, "Usage, Credits & Billing",
        "Transparent prepaid credit system — know exactly what you are spending"))

    story.append(Paragraph(
        "Services that have per-use costs — AI generation, SMS sending, WhatsApp messaging — "
        "run on a prepaid credit wallet system. You top up credit in advance and spend it as you "
        "use services. Every transaction is logged with full cost breakdown.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Service Wallets", st["h3"]))
    wallets = [
        ("AI Wallet", "Covers AI ward brief and speech generation — costs per token/request"),
        ("SMS Wallet", "Covers outbound SMS messages — costs per message"),
        ("WhatsApp Wallet", "Covers WhatsApp Business API messages — costs per conversation/message"),
        ("Email Wallet", "Covers transactional email delivery"),
        ("Maps Wallet", "Covers GPS and maps API calls"),
        ("Storage Wallet", "Covers file storage for large media uploads"),
    ]
    for name, desc in wallets:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("How It Works", st["h3"]))
    for line in [
        "Each subscription plan includes a free quota for certain services (e.g. 100 AI requests/month)",
        "Once free quota is exhausted, usage is drawn from your prepaid wallet balance",
        "If your wallet balance reaches zero, the service stops — preventing unexpected overcharges",
        "Top up at any time by submitting a top-up record with payment method and reference",
        "Every usage event is logged: service, action, quantity, cost before and after, balance remaining",
        "Low-balance alerts appear on the dashboard before you run out",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 19 — SECURITY & AUDIT
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 19, "Security, Audit & Compliance",
        "Every action logged — full accountability for your campaign data"))

    story.append(Paragraph(
        "CampaignMasta maintains a full audit trail of every significant action in the platform. "
        "This protects the candidate legally, ensures data integrity, and provides accountability "
        "across the entire team.",
        st["body"]))
    story.append(sp(2))

    story.append(Paragraph("Audit Log — What Gets Recorded", st["h3"]))
    audit_events = [
        "Supporter created / updated",
        "Influencer created / call logged",
        "Message composed / sent / read / acknowledged",
        "Task created / completed",
        "Ward profile created / updated / viewed",
        "AI brief generated / reviewed / approved",
        "Data exported / imported / downloaded",
        "Polling location created / status submitted / incident logged",
        "Team member created / login provisioned",
        "Subscription quote created / accepted",
        "Connector created / updated / tested",
        "Usage top-up recorded",
        "Preference deal created / updated",
        "Community group / assistance / competitor activity logged",
    ]
    cols = [audit_events[:7], audit_events[7:]]
    audit_tbl = Table(
        [[Paragraph(f"&#x2022;  {a}", st["cell_body"]) for a in col] for col in zip(*[iter(audit_events)] * 2)]
        if len(audit_events) % 2 == 0
        else [[Paragraph(f"&#x2022;  {a}", st["cell_body"]), Paragraph("", st["cell_body"])]
              for a in audit_events[-1:]],
        colWidths=[(W - 2 * MARGIN) / 2] * 2
    )
    # Simpler: just list them
    for ev in audit_events:
        story.append(Paragraph(f"&#x2022;  {ev}", st["bullet"]))

    story.append(sp(3))
    story.append(Paragraph("Access Control", st["h3"]))
    for line in [
        "Session timeout after 8 hours — automatic logout for security",
        "Role-based access — team members see only their geographic area",
        "Multi-tenant isolation — each candidate's data is completely separate",
        "Export approval workflow — sensitive data exports require manager sign-off",
        "IP address and device logging on every access",
        "Data Lifecycle Requests — formal process for data correction, export, archival, or deletion",
    ]:
        story.append(Paragraph(f"&#x2022;  {line}", st["bullet"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 20 — TECHNOLOGY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(st, 20, "Technology & Deployment",
        "Modern, reliable, and built for PNG's network conditions"))

    story.append(Paragraph(
        "CampaignMasta is built on proven, enterprise-grade open source technology, deployed "
        "on dedicated servers, and accessed through any modern web browser or the Android native app.",
        st["body"]))
    story.append(sp(2))

    tech_items = [
        ("Web Platform", "Django (Python) backend — robust, battle-tested, used by major global platforms"),
        ("Mobile App", "Native Android application with offline capability for field data collection"),
        ("Database", "MySQL — reliable relational database for structured campaign data"),
        ("File Server", "Nginx — high-performance reverse proxy and static file serving"),
        ("Application Server", "Gunicorn — production-grade Python WSGI server"),
        ("Deployment", "Linux VPS — dedicated server with full control"),
        ("Connectivity", "Works on 3G, 4G, and slow connections — optimised for PNG network conditions"),
        ("Browser Support", "Chrome, Firefox, Safari, Edge — any modern browser on any device"),
        ("Security", "HTTPS encryption, CSRF protection, SQL injection prevention, XSS defence"),
        ("Timezone", "Pacific/Port_Moresby (PGK +10) — all timestamps in PNG time"),
    ]
    for name, desc in tech_items:
        story.append(Paragraph(f"<b>{name}:</b>  {desc}", st["bullet"]))

    story.append(sp(4))
    story.append(rule(GOLD, 1.5, 4, 6))

    story.append(highlight_box(st,
        "CampaignMasta is maintained and supported by WebMasta — PNG's leading digital "
        "services company. Support is available via phone, WhatsApp, and email throughout "
        "the campaign period.",
        bg=colors.HexColor("#FDF8EC"), border=GOLD))

    # Final CTA
    cta_data = [[
        Paragraph("<b><font size='13' color='#ffffff'>Ready to run a smarter campaign?</font></b><br/>"
                  "<font size='10' color='#C8ECC8'>Contact WebMasta today to get set up before the election.</font>",
                  ParagraphStyle("cta_t", fontName="Helvetica", fontSize=10, leading=16,
                      textColor=WHITE, alignment=TA_CENTER, spaceAfter=0)),
        Paragraph("<b><font size='11' color='#EDD270'>campaignmasta.com</font></b><br/>"
                  "<font size='9' color='#C8ECC8'>admin@campaignmasta.com</font>",
                  ParagraphStyle("cta_url", fontName="Helvetica", fontSize=9, leading=14,
                      textColor=WHITE, alignment=TA_CENTER, spaceAfter=0)),
    ]]
    cta_tbl = Table(cta_data, colWidths=[(W - 2*MARGIN)*0.6, (W - 2*MARGIN)*0.4])
    cta_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GREEN_DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LINEAFTER",     (0, 0), (0, -1), 0.5, colors.HexColor("#3A8A3A")),
    ]))
    story += [sp(2), cta_tbl]

    # Build
    doc.build(story,
              onFirstPage=on_first_page,
              onLaterPages=on_page)
    print(f"PDF generated: {out}")


if __name__ == "__main__":
    build()
