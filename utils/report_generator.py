"""
ReportLab PDF Report Generator.

Compiles structured career assessment outputs into a publication-quality PDF report.
Utilizes NumberedCanvas to support clean "Page X of Y" pagination, headers, and footers.
"""

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page counts
    along with professional running headers and footers on later pages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        # Save page state for the second pass
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # 1. Page 1 (Cover Page): Suppress decorations
        if self._pageNumber == 1:
            # Draw decorative sidebar background on cover page
            self.setFillColor(HexColor("#1A365D"))
            self.rect(0, 0, 30, 792, fill=True, stroke=False)
            self.restoreState()
            return

        # 2. Later Pages: Draw Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(HexColor("#1A365D"))
        self.drawString(54, 750, "CAREERPILOT AI")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#718096"))
        self.drawRightString(558, 750, "CONFIDENTIAL CAREER ASSESSMENT REPORT")
        
        # Header Divider line
        self.setStrokeColor(HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # 3. Later Pages: Draw Footer
        self.line(54, 60, 558, 60)
        self.drawString(54, 45, f"Report Generated: {datetime.now().strftime('%Y-%m-%d')}")
        self.drawRightString(558, 45, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf_report(data: dict, filepath: str) -> str:

    """
    Generates a professional downloadable PDF report based on collected data.

    Args:
        data: Aggregated career tracks dictionary from all modules.
        filepath: Target output file location path.

    Returns:
        String path of the generated PDF file.
    """
    # ── Page Layout Configuration ──
    # Page size: Letter (612 x 792 pts). Margin: 0.75" (54 pts).
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    # ── Color Palette ──
    c_primary = HexColor("#1A365D")    # Dark blue
    c_secondary = HexColor("#2B6CB0")  # Slate blue
    c_dark = HexColor("#2D3748")       # Charcoal body text
    c_light = HexColor("#EDF2F7")      # Table background headers
    c_light_bg = HexColor("#F7FAFC")   # Page backgrounds / accent bars
    c_green = HexColor("#2F855A")      # Safe indicator green
    c_red = HexColor("#C53030")        # Risk indicator red

    # ── Styles Setup ──
    styles = getSampleStyleSheet()
    
    # Text styling overrides
    style_body = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_dark
    )
    style_body_bold = ParagraphStyle(
        'ReportBodyBold',
        parent=style_body,
        fontName='Helvetica-Bold'
    )
    
    # Headings
    style_h1 = ParagraphStyle(
        'ReportH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=12,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'ReportH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    style_bullet = ParagraphStyle(
        'ReportBullet',
        parent=style_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 150))
    
    # Title Block
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=style_h1,
        fontSize=28,
        leading=34,
        textColor=c_primary,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=style_body,
        fontSize=14,
        leading=18,
        textColor=c_secondary,
        spaceAfter=30
    )
    
    story.append(Paragraph("CareerPilot AI", title_style))
    story.append(Paragraph("Personalized Career Assessment Report", subtitle_style))
    
    # Divider bar
    divider_table = Table([[""]], colWidths=[504], rowHeights=[4])
    divider_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_secondary),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(divider_table)
    story.append(Spacer(1, 180))

    # Metadata Panel
    username = data.get("username", "Professional Candidate")
    target_role = data.get("target_role", "Data Scientist")
    date_str = datetime.now().strftime("%B %d, %Y")
    
    metadata_data = [
        [Paragraph("<b>Candidate Name:</b>", style_body), Paragraph(username, style_body)],
        [Paragraph("<b>Target Track:</b>", style_body), Paragraph(target_role, style_body)],
        [Paragraph("<b>Analysis Date:</b>", style_body), Paragraph(date_str, style_body)],
        [Paragraph("<b>Report Status:</b>", style_body), Paragraph("Finalized Assessment", style_body)]
    ]
    metadata_table = Table(metadata_data, colWidths=[120, 384])
    metadata_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(metadata_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("Executive Summary", style_h1))
    
    health_score = data.get("health_score", 50.0)
    health_label = data.get("health_label", "Average")
    readiness_score = data.get("readiness_score", 50.0)
    readiness_label = data.get("readiness_label", "Needs Preparation")
    ats_score = data.get("ats_score", 70.0)
    gap_score = data.get("gap_score", 50.0)
    
    # Metrics Cards table
    metrics_data = [
        [
            Paragraph("<b>Career Health Score</b>", style_body),
            Paragraph("<b>Hiring Readiness</b>", style_body),
            Paragraph("<b>Resume ATS Score</b>", style_body),
            Paragraph("<b>Skill Gap Score</b>", style_body)
        ],
        [
            Paragraph(f"<font size=20 color='#2F855A'><b>{health_score}</b></font><br/>{health_label}", style_body),
            Paragraph(f"<font size=20 color='#2B6CB0'><b>{readiness_score}</b></font><br/>{readiness_label}", style_body),
            Paragraph(f"<font size=20><b>{ats_score}%</b></font><br/>ATS scan compatibility", style_body),
            Paragraph(f"<font size=20 color='#C53030'><b>{gap_score}%</b></font><br/>Core skill gaps detected", style_body)
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[126, 126, 126, 126])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 1, HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    exec_summary_text = (
        f"This career assessment report provides a comprehensive, structured evaluation of your qualifications "
        f"for the role of <b>{target_role}</b>. Based on automated parsing of your profile, your Career Health Score "
        f"rests at <b>{health_score}/100</b>, indicating a <b>{health_label}</b> posture. Your target hiring outlook has been "
        f"derived directly from quantitative gaps in technical skills and mock interview readiness indexes. Review the following "
        f"pages for specific preparation focus areas and recommended action steps."
    )
    story.append(Paragraph(exec_summary_text, style_body))
    story.append(Spacer(1, 20))

    # =========================================================================
    # SECTION 3: RESUME ANALYSIS
    # =========================================================================
    story.append(Paragraph("Resume Analysis", style_h1))
    
    strengths = data.get("resume_strengths", [])
    weaknesses = data.get("resume_weaknesses", [])
    ats_feedback = data.get("ats_feedback", "Perform analysis to review optimization items.")
    
    story.append(Paragraph(f"<b>Overall Resume Completeness Score:</b> {ats_score}/100", style_body))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("Identified Strengths:", style_h2))
    if strengths:
        for s in strengths:
            story.append(Paragraph(f"• {s}", style_bullet))
    else:
        story.append(Paragraph("• No major strengths recorded. Complete Resume Analyzer phase.", style_bullet))
        
    story.append(Paragraph("Improvement Risk Areas:", style_h2))
    if weaknesses:
        for w in weaknesses:
            story.append(Paragraph(f"• {w}", style_bullet))
    else:
        story.append(Paragraph("• Resume audit shows minimal formatting errors.", style_bullet))
        
    story.append(Paragraph("ATS Keywords & Optimization Feedback:", style_h2))
    story.append(Paragraph(ats_feedback, style_body))
    story.append(Spacer(1, 20))

    # =========================================================================
    # SECTION 4: SKILL GAP ANALYSIS
    # =========================================================================
    story.append(Paragraph("Skill Gap Analysis", style_h1))
    
    matched_skills = data.get("matched_skills", [])
    missing_skills = data.get("missing_skills", [])
    
    skills_data = [
        [Paragraph("<b>Matched Skills (Possessed)</b>", style_body), Paragraph("<b>Missing Skills (Targets)</b>", style_body)],
        [
            Paragraph("<br/>".join(f"✔ {s}" for s in matched_skills) if matched_skills else "No skills mapped.", style_body),
            Paragraph("<br/>".join(f"✘ {s}" for s in missing_skills) if missing_skills else "No missing skills detected.", style_body)
        ]
    ]
    skills_table = Table(skills_data, colWidths=[252, 252])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 1, HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 20))

    # =========================================================================
    # SECTION 5: CAREER ROADMAP
    # =========================================================================
    story.append(Paragraph("Career Development Roadmap", style_h1))
    
    timeline_months = data.get("timeline_months", "6 Months")
    roadmap_stages = data.get("roadmap_stages", {})
    monthly_plan = data.get("monthly_plan", {})
    priority_matrix = data.get("priority_matrix", {})
    
    story.append(Paragraph(f"<b>Personalized Timeline Frame:</b> {timeline_months}", style_body))
    story.append(Spacer(1, 8))
    
    # 1. Milestones/Stages
    story.append(Paragraph("Development Milestones by Stage:", style_h2))
    for stage_name, stage_details in roadmap_stages.items():
        if isinstance(stage_details, list):
            skills_text = []
            for item in stage_details:
                if isinstance(item, dict):
                    status_txt = "Matched" if item.get("status") == "Matched" else "Missing"
                    skills_text.append(f"{item.get('skill')} ({status_txt})")
                else:
                    skills_text.append(str(item))
            skills_str = ", ".join(skills_text)
            story.append(Paragraph(f"• <b>{stage_name}:</b> {skills_str}", style_bullet))
        elif isinstance(stage_details, dict):
            desc = stage_details.get("desc", "Study stage guidelines.")
            skills = ", ".join(stage_details.get("skills", []))
            story.append(Paragraph(f"• <b>{stage_name}:</b> {desc} (Focus: {skills})", style_bullet))
        else:
            story.append(Paragraph(f"• <b>{stage_name}:</b> {str(stage_details)}", style_bullet))
    
    # 2. Monthly Plan
    if monthly_plan:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Month-by-Month Plan:", style_h2))
        for period, plan_details in monthly_plan.items():
            if isinstance(plan_details, dict):
                focus = plan_details.get("focus", "")
                skills_list = plan_details.get("skills", [])
                skills_str = ", ".join(skills_list)
                story.append(Paragraph(f"• <b>{period}</b> - {focus} (Target: {skills_str})", style_bullet))
            else:
                story.append(Paragraph(f"• <b>{period}</b> - {str(plan_details)}", style_bullet))
                
    # 3. Skill Priorities
    if priority_matrix:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Skill Priorities Matrix:", style_h2))
        for priority, skills in priority_matrix.items():
            skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
            story.append(Paragraph(f"• <b>{priority} Priority:</b> {skills_str}", style_bullet))
            
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 6: INTERVIEW READINESS
    # =========================================================================
    story.append(Paragraph("Interview Readiness & Risks", style_h1))
    
    interview_risk_questions = data.get("interview_risk_questions", [])
    interview_readiness = data.get("interview_readiness", 50.0)
    
    story.append(Paragraph(f"<b>Interview Preparation Score:</b> {interview_readiness}%", style_body))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("High Risk Interview Questions (Based on skill gaps):", style_h2))
    if interview_risk_questions:
        for i, q in enumerate(interview_risk_questions, 1):
            story.append(Paragraph(f"<b>Q{i}:</b> {q}", style_bullet))
    else:
        story.append(Paragraph("No critical interview risk zones mapped. Continue mock preparation.", style_bullet))
    story.append(Spacer(1, 20))

    # =========================================================================
    # SECTION 7: PROJECT RECOMMENDATIONS
    # =========================================================================
    story.append(Paragraph("Recommended Portfolio Projects", style_h1))
    
    projects_list = data.get("projects", [])
    
    if projects_list:
        for p in projects_list[:4]:  # Top 4 projects
            story.append(Paragraph(f"<b>{p.get('title')}</b> ({p.get('difficulty_label', 'Intermediate')})", style_h2))
            story.append(Paragraph(f"<b>Description:</b> {p.get('description')}", style_body))
            story.append(Paragraph(f"<b>Estimated Duration:</b> {p.get('duration', '3 weeks')} | <b>Skills Learned:</b> {', '.join(p.get('skills_learned', []))}", style_body))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No custom projects recommended yet. Complete Project Recommender phase.", style_body))
    story.append(Spacer(1, 20))

    # =========================================================================
    # SECTION 8: AI ADVISOR & UNIFIED ACTION PLAN
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("AI Advisor Strategy & Next Steps", style_h1))
    
    advisor_summary = data.get("advisor_summary", "Assess missing skill parameters first.")
    story.append(Paragraph(advisor_summary, style_body))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Hiring Outlook:", style_h2))
    hiring_outlook = data.get("hiring_outlook", "Highly competitive. Focus on verified projects.")
    story.append(Paragraph(hiring_outlook, style_body))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Unified Action Timeline Plan", style_h1))
    action_plan = data.get("action_plan", {})
    
    # Action Plan visual table layout
    action_table_data = [
        [Paragraph("<b>Timeframe</b>", style_body), Paragraph("<b>Action Items & Milestones</b>", style_body)],
        [
            Paragraph("<b>Next 7 Days</b><br/>Immediate", style_body),
            Paragraph("<br/>".join(f"• {x}" for x in action_plan.get("immediate_7_days", ["Review resume optimization items."])), style_body)
        ],
        [
            Paragraph("<b>Next 30 Days</b><br/>Short Term", style_body),
            Paragraph("<br/>".join(f"• {x}" for x in action_plan.get("short_term_30_days", ["Complete beginner portfolio projects."])), style_body)
        ],
        [
            Paragraph("<b>Next 90 Days</b><br/>Medium Term", style_body),
            Paragraph("<br/>".join(f"• {x}" for x in action_plan.get("medium_term_90_days", ["Target advanced project milestones."])), style_body)
        ],
        [
            Paragraph("<b>6–12 Months</b><br/>Long Term", style_body),
            Paragraph("<br/>".join(f"• {x}" for x in action_plan.get("long_term_goals", ["Apply to roles and track interviews."])), style_body)
        ]
    ]
    action_table = Table(action_table_data, colWidths=[120, 384])
    action_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 1, HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(action_table)

    # ── Build Document Story storyboard ──
    doc.build(story, canvasmaker=NumberedCanvas)
    return filepath
