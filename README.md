# Data Lab Projects

This workspace contains 12 independent Flask projects aligned to the **Data & AI Foundations Bootcamp Curriculum v1.0 (2026-09-02)**. Every project owns its own `app.py`, `templates/index.html`, `static/css/style.css`, `static/js/app.js`, `requirements.txt`, README, objective mapping in documentation, and (where useful) local data files.

## Quick start

Each app is independent and can be run from its own folder:

```bash
cd week1_personal_data_diary
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the port shown in the project README. The apps use ports 5001–5012 so they can be launched together for a tour.

## Project map

| Week | Project | Folder | Port |
|---|---|---|---:|
| Week 1 · P1 | Week1 Personal Data Diary | `week1_personal_data_diary` | 5001 |
| Week 1 · P2 | Week1 Storytelling Dashboard | `week1_storytelling_dashboard` | 5002 |
| Week 2 · P1 | Week2 Budget Calculator | `week2_budget_calculator` | 5003 |
| Week 2 · P2 | Week2 Text Cleaner Word Counter | `week2_text_cleaner_word_counter` | 5004 |
| Week 3 · P1 | Week3 Sales Kpi Analyzer | `week3_sales_kpi_analyzer` | 5005 |
| Week 3 · P2 | Week3 Eda Visual Report | `week3_eda_visual_report` | 5006 |
| Week 4 · P1 | Week4 Survey Insights Report | `week4_survey_insights_report` | 5007 |
| Week 4 · P2 | Week4 Churn Classifier | `week4_churn_classifier` | 5008 |
| Week 5 · P1 | Week5 Study Planner Assistant | `week5_study_planner_assistant` | 5009 |
| Week 5 · P2 | Week5 Content Generator | `week5_content_generator` | 5010 |
| Week 6 · P1 | PharmaInsight AI | `week6_pharmainsight_ai` | 5011 |
| Week 6 · P2 | AI Pitch & Demo | `week6_ai_pitch_demo` | 5012 |

## Curriculum alignment

Each project now exposes a `/api/curriculum` endpoint and curriculum-alignment documentation. The portfolio includes curriculum evidence for data cleaning, spreadsheet-style summaries, 1,000+ row KPI analysis, EDA upload/reporting, five-question statistics, train/test ML evaluation, prompt templates, batch content generation, responsible-AI review, and a five-slide capstone pitch.

See [`CURRICULUM_ALIGNMENT.md`](CURRICULUM_ALIGNMENT.md) for the objective-by-objective mapping.

## Shared conventions

The apps use project-specific responsive palettes, accessible labels, server-side JSON endpoints under `/api`, and a project-status indicators route for smoke checks. No external database or API credentials are required for the local demonstrations; optional Colab, spreadsheet, public-dataset, and LLM workflows are documented in the project READMEs.
