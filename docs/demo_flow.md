# docs/demo_flow.md
# CareerPilot AI — User Demo Flow

This document describes the end-to-end user journey through CareerPilot AI.

---

## Standard Flow (Manual Mode)

```
User Opens App
      │
      ▼
┌─────────────────────┐
│  📄 Resume Analyzer  │  Upload PDF → ATS Score + Parsed Profile
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  🔍 Skill Gap Agent  │  Select Role → Match / Gap / Score %
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  🗺️ Roadmap Agent   │  Generates 3-tier monthly learning plan
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  🎙️ Interview Coach  │  Mock Q&A + Readiness Score + Risk Areas
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  🛠️ Project Mentor   │  Portfolio projects ranked by priority score
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  👑 Master Agent     │  Health Score + Readiness + Action Plan
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  📥 PDF Report       │  Download full career assessment report
└─────────────────────┘
```

---

## Agentic Flow (Automated Mode)

```
User pastes Resume Text + Selects Target Role
      │
      ▼
┌───────────────────────────────────┐
│  🤖 Agentic Career Advisor Page    │
│                                   │
│  Step 1 ── Resume Specialist      │
│  Step 2 ── Skill Gap Analyst      │
│  Step 3 ── Roadmap Strategist     │
│  Step 4 ── Interview Coach        │
│  Step 5 ── Project Mentor         │
│  Step 6 ── Career Advisor         │
│                                   │
│  Real-time live step panel        │
└────────────────┬──────────────────┘
                 │
                 ▼
      Unified Career Assessment
      (All results in one view)
```

---

## Key Output Metrics

| Metric | Source | Range |
|---|---|---|
| ATS Completeness Score | Resume Agent | 0–100 |
| Skill Gap Score | Skill Gap Agent | 0–100% |
| Roadmap Timeline | Roadmap Agent | months |
| Interview Readiness | Interview Agent | 0–100 |
| Portfolio Impact | Project Agent | 0–100 |
| Career Health Score | Master Agent | 0–100 |
| Hiring Readiness Score | Master Agent | 0–100 |

---

## Target Roles Supported

The system currently supports analysis for the following career tracks:

- Data Scientist
- Machine Learning Engineer
- Backend Developer
- Frontend Developer
- Full Stack Developer
- DevOps Engineer
- Cloud Architect
- Cybersecurity Analyst
- Data Analyst
- AI/ML Research Engineer

*(Extendable via `utils/role_database.py`)*
