"""
Static Project Template Database.

Organized by: Role → Difficulty → List of Project objects.

Each project contains:
    title           : Project name
    description     : What the project does and what problem it solves
    skills_required : Prerequisites the candidate should already have
    skills_learned  : Skills this project actively teaches/reinforces
    duration        : Estimated completion time
    portfolio_impact: 0-100 — visibility and impressiveness in a portfolio
    resume_impact   : 0-100 — strength added to a resume bullet
    hiring_value    : 0-100 — how much employers value seeing this project
    companies_that_value : Company types that look for this experience
    dev_phases      : 4-step project development roadmap
"""

PROJECT_TEMPLATES: dict = {

    # ══════════════════════════════════════════════════════════════
    # AI ENGINEER
    # ══════════════════════════════════════════════════════════════
    "AI Engineer": {
        "Beginner": [
            {
                "title": "Prompt Engineering Assistant",
                "description": (
                    "Build a Streamlit app that lets users test different prompt strategies "
                    "(zero-shot, few-shot, chain-of-thought) against an LLM API and compare output quality."
                ),
                "skills_required": ["Python", "API basics"],
                "skills_learned": ["Prompt Engineering", "LLM APIs", "Streamlit", "Python"],
                "duration": "1–2 weeks",
                "portfolio_impact": 55,
                "resume_impact": 60,
                "hiring_value": 65,
                "companies_that_value": ["AI Startups", "Consultancies", "Product companies"],
                "dev_phases": [
                    "Phase 1 – Plan: Define prompt strategy comparisons and UI layout",
                    "Phase 2 – Build: Integrate LLM API, create prompt templates, build Streamlit UI",
                    "Phase 3 – Test: Validate output quality, edge-case prompts, API error handling",
                    "Phase 4 – Deploy: Host on Streamlit Cloud with public shareable link"
                ]
            },
            {
                "title": "AI Resume Analyzer",
                "description": (
                    "Create a tool that parses uploaded PDF resumes, extracts structured profile data "
                    "using an LLM, and provides ATS-readiness feedback and improvement suggestions."
                ),
                "skills_required": ["Python", "PDF parsing basics"],
                "skills_learned": ["LLM APIs", "PDF Parsing", "Prompt Engineering", "Streamlit"],
                "duration": "2–3 weeks",
                "portfolio_impact": 70,
                "resume_impact": 75,
                "hiring_value": 72,
                "companies_that_value": ["HR Tech", "AI Startups", "SaaS companies"],
                "dev_phases": [
                    "Phase 1 – Plan: Design extraction schema and ATS scoring rubric",
                    "Phase 2 – Build: PDF parser, LLM extraction pipeline, feedback generator",
                    "Phase 3 – Test: Upload 10+ varied resumes, validate extraction accuracy",
                    "Phase 4 – Deploy: Host on Streamlit Cloud, add GitHub README with demo"
                ]
            }
        ],
        "Intermediate": [
            {
                "title": "RAG Knowledge Assistant",
                "description": (
                    "Build a Retrieval-Augmented Generation chatbot that ingests custom documents "
                    "(PDFs, text files), chunks and embeds them into a vector database, and answers "
                    "user queries with grounded, cited responses."
                ),
                "skills_required": ["Python", "LLM APIs", "Basic NLP"],
                "skills_learned": ["RAG", "LangChain", "Vector Databases", "Embeddings", "FAISS/ChromaDB"],
                "duration": "3–4 weeks",
                "portfolio_impact": 85,
                "resume_impact": 88,
                "hiring_value": 90,
                "companies_that_value": ["Enterprise AI", "Legal Tech", "FinTech", "Healthcare AI"],
                "dev_phases": [
                    "Phase 1 – Plan: Choose vector DB (FAISS/ChromaDB), design chunking strategy",
                    "Phase 2 – Build: Ingestion pipeline, embedding layer, retrieval chain, chat UI",
                    "Phase 3 – Test: Evaluate faithfulness, answer relevance, retrieval precision",
                    "Phase 4 – Deploy: Containerize with Docker, deploy on Hugging Face Spaces or AWS"
                ]
            },
            {
                "title": "Document Chatbot with Memory",
                "description": (
                    "Create a multi-turn conversational chatbot that maintains conversation history, "
                    "references uploaded documents, and provides contextually consistent answers across sessions."
                ),
                "skills_required": ["Python", "LangChain basics", "LLM APIs"],
                "skills_learned": ["LangChain", "Memory Management", "RAG", "Streamlit", "Vector Databases"],
                "duration": "3–4 weeks",
                "portfolio_impact": 82,
                "resume_impact": 85,
                "hiring_value": 87,
                "companies_that_value": ["Customer Support AI", "SaaS", "Enterprise Software"],
                "dev_phases": [
                    "Phase 1 – Plan: Design conversation memory schema and document ingestion flow",
                    "Phase 2 – Build: Memory buffer, document chain, multi-turn chat interface",
                    "Phase 3 – Test: Validate context retention across 10+ turn conversations",
                    "Phase 4 – Deploy: Streamlit Cloud or Render with environment variable config"
                ]
            }
        ],
        "Advanced": [
            {
                "title": "Multi-Agent AI System",
                "description": (
                    "Design and build a multi-agent orchestration system where specialized agents "
                    "(researcher, writer, critic, executor) collaborate using a framework like LangGraph "
                    "or CrewAI to complete complex multi-step tasks autonomously."
                ),
                "skills_required": ["LangChain", "LLM APIs", "Python OOP", "RAG"],
                "skills_learned": ["LangGraph", "CrewAI", "Agent Orchestration", "Tool Use", "Prompt Engineering"],
                "duration": "6–8 weeks",
                "portfolio_impact": 95,
                "resume_impact": 96,
                "hiring_value": 97,
                "companies_that_value": ["AI Research Labs", "Agentic AI Startups", "Google", "Anthropic", "OpenAI"],
                "dev_phases": [
                    "Phase 1 – Plan: Define agent roles, tool interfaces, and orchestration graph",
                    "Phase 2 – Build: Individual agents, tool integrations, orchestration layer",
                    "Phase 3 – Test: Run complex multi-step tasks, measure completion rate and accuracy",
                    "Phase 4 – Deploy: Package as API with FastAPI, deploy on AWS/GCP"
                ]
            },
            {
                "title": "Autonomous Research Agent",
                "description": (
                    "Build an autonomous AI agent that accepts a research topic, searches the web, "
                    "reads papers, synthesizes insights, and produces a structured research report — "
                    "all without human intervention."
                ),
                "skills_required": ["LangChain", "RAG", "Agent frameworks", "Web scraping"],
                "skills_learned": ["Autonomous Agents", "Tool Use", "Web Search Integration", "LangGraph", "Report Generation"],
                "duration": "6–8 weeks",
                "portfolio_impact": 97,
                "resume_impact": 95,
                "hiring_value": 96,
                "companies_that_value": ["Research Labs", "Consulting Firms", "AI-first Startups"],
                "dev_phases": [
                    "Phase 1 – Plan: Define tool set (web search, PDF reader, summarizer), design agent loop",
                    "Phase 2 – Build: Tool wrappers, agent loop with planning and reflection",
                    "Phase 3 – Test: Run on 5 diverse research topics, measure report quality",
                    "Phase 4 – Deploy: CLI tool with Markdown/PDF report output, GitHub release"
                ]
            }
        ]
    },

    # ══════════════════════════════════════════════════════════════
    # DATA SCIENTIST
    # ══════════════════════════════════════════════════════════════
    "Data Scientist": {
        "Beginner": [
            {
                "title": "Interactive Sales Dashboard",
                "description": (
                    "Build an interactive Plotly/Streamlit dashboard analyzing retail sales data. "
                    "Include KPIs, time-series trends, product category breakdowns, and regional heatmaps."
                ),
                "skills_required": ["Python", "Pandas basics"],
                "skills_learned": ["Pandas", "Plotly", "Streamlit", "Data Visualization", "EDA"],
                "duration": "1–2 weeks",
                "portfolio_impact": 55,
                "resume_impact": 58,
                "hiring_value": 60,
                "companies_that_value": ["Retail Analytics", "E-commerce", "Consulting"],
                "dev_phases": [
                    "Phase 1 – Plan: Define KPIs, select public dataset (Kaggle retail dataset)",
                    "Phase 2 – Build: Data cleaning, aggregation, Plotly charts, Streamlit layout",
                    "Phase 3 – Test: Validate chart accuracy with raw data, check edge cases",
                    "Phase 4 – Deploy: Streamlit Cloud with embedded dataset"
                ]
            },
            {
                "title": "Customer Churn Analysis",
                "description": (
                    "Analyze telecom or banking customer data to identify churn drivers using "
                    "EDA, feature analysis, and a baseline classification model with Scikit-Learn."
                ),
                "skills_required": ["Python", "Pandas", "Basic statistics"],
                "skills_learned": ["EDA", "Scikit-Learn", "Feature Engineering", "Classification", "Matplotlib"],
                "duration": "2 weeks",
                "portfolio_impact": 65,
                "resume_impact": 68,
                "hiring_value": 70,
                "companies_that_value": ["Telecom", "Banking", "Insurance", "SaaS"],
                "dev_phases": [
                    "Phase 1 – Plan: Select dataset, define churn label, identify target features",
                    "Phase 2 – Build: EDA notebook, feature engineering, Logistic Regression baseline",
                    "Phase 3 – Test: Cross-validate, report precision/recall/F1, confusion matrix",
                    "Phase 4 – Deploy: Jupyter notebook on GitHub with detailed README"
                ]
            }
        ],
        "Intermediate": [
            {
                "title": "Fraud Detection System",
                "description": (
                    "Build an end-to-end fraud detection pipeline on imbalanced transaction data "
                    "using SMOTE, ensemble models (XGBoost, RandomForest), and a real-time scoring API."
                ),
                "skills_required": ["Scikit-Learn", "Pandas", "Python", "Basic ML"],
                "skills_learned": ["Imbalanced Learning", "XGBoost", "Model Evaluation", "FastAPI", "SMOTE"],
                "duration": "3–4 weeks",
                "portfolio_impact": 82,
                "resume_impact": 85,
                "hiring_value": 88,
                "companies_that_value": ["FinTech", "Banking", "Payment Processors", "Insurance"],
                "dev_phases": [
                    "Phase 1 – Plan: Define fraud label, handle class imbalance strategy",
                    "Phase 2 – Build: SMOTE pipeline, XGBoost model, FastAPI scoring endpoint",
                    "Phase 3 – Test: AUC-ROC, precision-recall curve, threshold tuning",
                    "Phase 4 – Deploy: Docker container, deploy on Railway or Render"
                ]
            },
            {
                "title": "Movie Recommendation System",
                "description": (
                    "Build a hybrid recommendation engine combining collaborative filtering "
                    "(SVD/ALS) and content-based filtering, served through a Streamlit interface."
                ),
                "skills_required": ["Python", "Pandas", "Scikit-Learn", "NumPy"],
                "skills_learned": ["Collaborative Filtering", "Matrix Factorization", "Content-Based Filtering", "Streamlit"],
                "duration": "3–4 weeks",
                "portfolio_impact": 80,
                "resume_impact": 82,
                "hiring_value": 83,
                "companies_that_value": ["Streaming Platforms", "E-commerce", "Media Tech"],
                "dev_phases": [
                    "Phase 1 – Plan: Select MovieLens dataset, define cold-start strategy",
                    "Phase 2 – Build: SVD model, content features, hybrid ranking, Streamlit UI",
                    "Phase 3 – Test: RMSE evaluation, manual relevance testing with sample users",
                    "Phase 4 – Deploy: Streamlit Cloud with preloaded model artifacts"
                ]
            }
        ],
        "Advanced": [
            {
                "title": "End-to-End ML Pipeline",
                "description": (
                    "Build a production ML pipeline with automated feature engineering, model training, "
                    "hyperparameter tuning (Optuna), experiment tracking (MLflow), and scheduled retraining."
                ),
                "skills_required": ["Scikit-Learn", "Python OOP", "SQL", "Git"],
                "skills_learned": ["MLflow", "Optuna", "Feature Stores", "MLOps", "Pipeline Automation"],
                "duration": "6–8 weeks",
                "portfolio_impact": 93,
                "resume_impact": 95,
                "hiring_value": 95,
                "companies_that_value": ["ML Platforms", "FAANG", "ML Startups", "Enterprise AI Teams"],
                "dev_phases": [
                    "Phase 1 – Plan: Define problem, data schema, evaluation metric, and MLflow setup",
                    "Phase 2 – Build: Feature pipeline, Optuna tuner, MLflow tracking, model registry",
                    "Phase 3 – Test: A/B model comparison, performance regression tests",
                    "Phase 4 – Deploy: GitHub Actions for CI/CD, deploy model via FastAPI + Docker"
                ]
            },
            {
                "title": "Predictive Analytics Platform",
                "description": (
                    "Design a multi-model predictive platform that forecasts business KPIs (sales, demand, "
                    "risk) using time-series models (Prophet, ARIMA, LSTM) with an interactive forecast dashboard."
                ),
                "skills_required": ["Python", "Scikit-Learn", "Pandas", "Statistics", "Deep Learning basics"],
                "skills_learned": ["Time Series Forecasting", "Prophet", "LSTM", "Dashboard Design", "Model Comparison"],
                "duration": "6–8 weeks",
                "portfolio_impact": 92,
                "resume_impact": 93,
                "hiring_value": 94,
                "companies_that_value": ["Finance", "Supply Chain", "Retail", "Energy"],
                "dev_phases": [
                    "Phase 1 – Plan: Select use case and dataset, define forecast horizons",
                    "Phase 2 – Build: Prophet/ARIMA/LSTM models, ensemble combiner, Plotly dashboard",
                    "Phase 3 – Test: MAPE, RMSE comparison across models on hold-out test set",
                    "Phase 4 – Deploy: Streamlit Cloud with downloadable forecast CSVs"
                ]
            }
        ]
    },

    # ══════════════════════════════════════════════════════════════
    # MACHINE LEARNING ENGINEER
    # ══════════════════════════════════════════════════════════════
    "Machine Learning Engineer": {
        "Beginner": [
            {
                "title": "Image Classifier Web App",
                "description": (
                    "Train a CNN image classifier using TensorFlow/Keras on CIFAR-10 or a custom dataset "
                    "and serve predictions through a Streamlit web app with confidence scores."
                ),
                "skills_required": ["Python", "NumPy", "Basic ML"],
                "skills_learned": ["TensorFlow", "Keras", "CNN Architecture", "Model Serving", "Streamlit"],
                "duration": "2–3 weeks",
                "portfolio_impact": 65,
                "resume_impact": 68,
                "hiring_value": 70,
                "companies_that_value": ["Computer Vision Startups", "Healthcare AI", "Retail Tech"],
                "dev_phases": [
                    "Phase 1 – Plan: Choose dataset, define model architecture, plan serving approach",
                    "Phase 2 – Build: CNN model, training loop, Streamlit upload-predict UI",
                    "Phase 3 – Test: Evaluate accuracy, confusion matrix, misclassification analysis",
                    "Phase 4 – Deploy: Streamlit Cloud with saved model artifact (HDF5/SavedModel)"
                ]
            },
            {
                "title": "Sentiment Analysis API",
                "description": (
                    "Fine-tune a pre-trained HuggingFace transformer (DistilBERT) for sentiment classification "
                    "and serve it through a FastAPI endpoint with JSON request/response."
                ),
                "skills_required": ["Python", "Basic NLP", "REST API basics"],
                "skills_learned": ["HuggingFace Transformers", "Transfer Learning", "FastAPI", "Fine-tuning"],
                "duration": "2–3 weeks",
                "portfolio_impact": 72,
                "resume_impact": 75,
                "hiring_value": 78,
                "companies_that_value": ["NLP Startups", "Social Media Analytics", "Customer Experience"],
                "dev_phases": [
                    "Phase 1 – Plan: Select dataset (SST-2 or IMDB), define API schema",
                    "Phase 2 – Build: Fine-tuning script, FastAPI server, prediction pipeline",
                    "Phase 3 – Test: Evaluate F1 on test set, load test the API",
                    "Phase 4 – Deploy: Dockerize and deploy on Hugging Face Spaces"
                ]
            }
        ],
        "Intermediate": [
            {
                "title": "Object Detection Pipeline",
                "description": (
                    "Build a real-time object detection pipeline using YOLOv8, with a video stream "
                    "processing module and a dashboard displaying detection statistics."
                ),
                "skills_required": ["Python", "OpenCV", "Basic Deep Learning", "PyTorch"],
                "skills_learned": ["YOLOv8", "OpenCV", "Real-Time Inference", "PyTorch", "MLOps"],
                "duration": "4–5 weeks",
                "portfolio_impact": 88,
                "resume_impact": 87,
                "hiring_value": 89,
                "companies_that_value": ["Autonomous Vehicles", "Surveillance", "Robotics", "Retail AI"],
                "dev_phases": [
                    "Phase 1 – Plan: Select detection task, gather labeled dataset, choose inference hardware",
                    "Phase 2 – Build: YOLOv8 training, inference pipeline, OpenCV stream processing",
                    "Phase 3 – Test: mAP evaluation, frame-rate profiling, edge case review",
                    "Phase 4 – Deploy: Streamlit or FastAPI with video upload and annotated output"
                ]
            },
            {
                "title": "MLOps Experiment Tracker",
                "description": (
                    "Build an experiment tracking dashboard that logs model hyperparameters, metrics, "
                    "and artifacts from multiple ML runs using MLflow, with a comparison UI."
                ),
                "skills_required": ["Python", "Scikit-Learn", "Basic ML", "Git"],
                "skills_learned": ["MLflow", "Experiment Tracking", "Model Registry", "DVC", "CI/CD"],
                "duration": "3–4 weeks",
                "portfolio_impact": 83,
                "resume_impact": 86,
                "hiring_value": 88,
                "companies_that_value": ["ML Platforms", "Enterprise AI", "Data Teams"],
                "dev_phases": [
                    "Phase 1 – Plan: Define tracked metrics, set up MLflow server, design experiment schema",
                    "Phase 2 – Build: Training scripts with MLflow logging, model registry, comparison UI",
                    "Phase 3 – Test: Run 10+ experiments, verify metric logging, test model loading",
                    "Phase 4 – Deploy: MLflow on Docker, automate runs with GitHub Actions"
                ]
            }
        ],
        "Advanced": [
            {
                "title": "Distributed Model Training System",
                "description": (
                    "Design a distributed training setup using PyTorch DDP or Ray Train for a large model, "
                    "with automated checkpointing, gradient accumulation, and training monitoring."
                ),
                "skills_required": ["PyTorch", "Deep Learning", "Linux/CLI", "Python OOP"],
                "skills_learned": ["Distributed Training", "PyTorch DDP", "Ray Train", "Gradient Accumulation", "Checkpointing"],
                "duration": "7–9 weeks",
                "portfolio_impact": 95,
                "resume_impact": 96,
                "hiring_value": 97,
                "companies_that_value": ["FAANG", "AI Research Labs", "Model Training Companies"],
                "dev_phases": [
                    "Phase 1 – Plan: Define model and dataset, choose distribution strategy, provision GPUs",
                    "Phase 2 – Build: DDP training script, checkpoint manager, monitoring dashboard",
                    "Phase 3 – Test: Scaling efficiency tests (1 vs 2 vs 4 GPU speedup)",
                    "Phase 4 – Deploy: Kubernetes job manifests, GitHub Actions trigger"
                ]
            },
            {
                "title": "LLM Fine-Tuning Pipeline",
                "description": (
                    "Fine-tune an open-source LLM (Mistral/LLaMA) using LoRA/QLoRA on a domain-specific "
                    "dataset, with evaluation, quantization for deployment, and an inference API."
                ),
                "skills_required": ["PyTorch", "HuggingFace", "Deep Learning", "Python"],
                "skills_learned": ["LoRA/QLoRA", "PEFT", "LLM Fine-tuning", "Quantization", "HuggingFace PEFT"],
                "duration": "7–10 weeks",
                "portfolio_impact": 97,
                "resume_impact": 97,
                "hiring_value": 98,
                "companies_that_value": ["LLM Startups", "AI Labs", "Enterprise AI", "Hugging Face"],
                "dev_phases": [
                    "Phase 1 – Plan: Select base model, curate fine-tuning dataset, define evaluation",
                    "Phase 2 – Build: LoRA config, training loop, evaluation harness",
                    "Phase 3 – Test: BLEU/ROUGE evaluation, compare base vs fine-tuned outputs",
                    "Phase 4 – Deploy: Quantize with bitsandbytes, serve via vLLM or Ollama"
                ]
            }
        ]
    },

    # ══════════════════════════════════════════════════════════════
    # DATA ENGINEER
    # ══════════════════════════════════════════════════════════════
    "Data Engineer": {
        "Beginner": [
            {
                "title": "ETL Pipeline with Airflow",
                "description": (
                    "Build an automated ETL pipeline using Apache Airflow that ingests CSV data from an API, "
                    "transforms it with Pandas, and loads it into a PostgreSQL database on a daily schedule."
                ),
                "skills_required": ["Python", "SQL basics", "Pandas"],
                "skills_learned": ["Apache Airflow", "ETL", "PostgreSQL", "Data Pipelines", "Task Scheduling"],
                "duration": "2–3 weeks",
                "portfolio_impact": 68,
                "resume_impact": 72,
                "hiring_value": 75,
                "companies_that_value": ["Data Teams", "Analytics Companies", "E-commerce"],
                "dev_phases": [
                    "Phase 1 – Plan: Define source API, transformation logic, target schema",
                    "Phase 2 – Build: Airflow DAG, extraction operators, transformation tasks, PostgreSQL loader",
                    "Phase 3 – Test: Run DAG, validate row counts, test failure and retry behavior",
                    "Phase 4 – Deploy: Docker Compose for Airflow, schedule daily runs"
                ]
            },
            {
                "title": "Data Quality Monitor",
                "description": (
                    "Create a data quality monitoring tool using Great Expectations that validates "
                    "schema, null rates, value ranges, and uniqueness across datasets with HTML reports."
                ),
                "skills_required": ["Python", "Pandas", "SQL basics"],
                "skills_learned": ["Great Expectations", "Data Validation", "Data Quality", "Profiling", "HTML Reports"],
                "duration": "1–2 weeks",
                "portfolio_impact": 60,
                "resume_impact": 65,
                "hiring_value": 68,
                "companies_that_value": ["Analytics Teams", "FinTech", "Healthcare Data"],
                "dev_phases": [
                    "Phase 1 – Plan: Define expectations suite for a sample dataset",
                    "Phase 2 – Build: Great Expectations suite, checkpoint runner, HTML report generator",
                    "Phase 3 – Test: Inject bad data, verify failures are caught and reported",
                    "Phase 4 – Deploy: Automate via cron or Airflow DAG, publish HTML reports"
                ]
            }
        ],
        "Intermediate": [
            {
                "title": "Real-Time Streaming Pipeline",
                "description": (
                    "Build a real-time data streaming pipeline using Kafka as the message broker and "
                    "PySpark Structured Streaming for processing, storing aggregated results in a data lake."
                ),
                "skills_required": ["Python", "SQL", "Kafka basics", "Spark basics"],
                "skills_learned": ["Apache Kafka", "PySpark", "Structured Streaming", "Delta Lake", "Stream Processing"],
                "duration": "4–5 weeks",
                "portfolio_impact": 88,
                "resume_impact": 90,
                "hiring_value": 92,
                "companies_that_value": ["FinTech", "E-commerce", "Ad Tech", "IoT Companies"],
                "dev_phases": [
                    "Phase 1 – Plan: Design Kafka topic schema, Spark processing logic, storage format",
                    "Phase 2 – Build: Kafka producer, Spark streaming consumer, Delta Lake sink",
                    "Phase 3 – Test: Verify message delivery, late-arrival handling, throughput benchmarks",
                    "Phase 4 – Deploy: Docker Compose cluster, submit Spark job via spark-submit"
                ]
            },
            {
                "title": "Data Warehouse with dbt",
                "description": (
                    "Design and implement a star-schema data warehouse using dbt for transformations, "
                    "with automated tests, documentation, and a BI-ready analytics layer."
                ),
                "skills_required": ["SQL", "Python", "Basic data modeling"],
                "skills_learned": ["dbt", "Data Modeling", "Star Schema", "Data Warehousing", "BigQuery/Snowflake"],
                "duration": "3–4 weeks",
                "portfolio_impact": 85,
                "resume_impact": 87,
                "hiring_value": 89,
                "companies_that_value": ["Analytics Engineering", "SaaS", "Retail", "Finance"],
                "dev_phases": [
                    "Phase 1 – Plan: Define business questions, design star schema, select warehouse",
                    "Phase 2 – Build: dbt models (staging, intermediate, mart), tests, documentation",
                    "Phase 3 – Test: Run dbt test suite, validate mart vs raw data",
                    "Phase 4 – Deploy: dbt Cloud scheduler with Slack alerting on failures"
                ]
            }
        ],
        "Advanced": [
            {
                "title": "Lakehouse Architecture Platform",
                "description": (
                    "Implement a full Lakehouse architecture using Delta Lake, Spark, and Airflow, "
                    "with Bronze/Silver/Gold layers, schema enforcement, and a query layer via Presto/Trino."
                ),
                "skills_required": ["Apache Spark", "SQL", "Airflow", "Cloud basics", "Python"],
                "skills_learned": ["Delta Lake", "Lakehouse Design", "Medallion Architecture", "Trino", "Data Governance"],
                "duration": "8–10 weeks",
                "portfolio_impact": 96,
                "resume_impact": 95,
                "hiring_value": 96,
                "companies_that_value": ["Data Platform Companies", "FAANG", "Cloud Providers"],
                "dev_phases": [
                    "Phase 1 – Plan: Define Bronze/Silver/Gold layers, ingestion sources, governance rules",
                    "Phase 2 – Build: Spark ingestion jobs, Delta Lake tables, Trino query layer",
                    "Phase 3 – Test: Schema evolution tests, ACID transaction verification",
                    "Phase 4 – Deploy: Kubernetes with Helm charts, Airflow orchestration"
                ]
            },
            {
                "title": "DataOps CI/CD Platform",
                "description": (
                    "Build a DataOps platform with automated pipeline testing, data contract validation, "
                    "lineage tracking, and CI/CD for dbt models using GitHub Actions."
                ),
                "skills_required": ["dbt", "Python", "Git", "SQL", "Airflow"],
                "skills_learned": ["DataOps", "Data Contracts", "Data Lineage", "CI/CD for Data", "OpenLineage"],
                "duration": "7–9 weeks",
                "portfolio_impact": 94,
                "resume_impact": 95,
                "hiring_value": 95,
                "companies_that_value": ["Data Platform Teams", "FinTech", "Enterprise Analytics"],
                "dev_phases": [
                    "Phase 1 – Plan: Define data contracts, lineage metadata schema, CI/CD triggers",
                    "Phase 2 – Build: Contract validator, lineage emitter (OpenLineage), GitHub Actions pipeline",
                    "Phase 3 – Test: Break a contract intentionally, verify CI failure and alert",
                    "Phase 4 – Deploy: Marquez lineage server, automated PR checks on dbt models"
                ]
            }
        ]
    },

    # ══════════════════════════════════════════════════════════════
    # FULL STACK DEVELOPER
    # ══════════════════════════════════════════════════════════════
    "Full Stack Developer": {
        "Beginner": [
            {
                "title": "Task Management App",
                "description": (
                    "Build a full-stack to-do/task management app with React frontend, Node.js/Express "
                    "backend, and MongoDB database — featuring CRUD operations, user auth, and drag-and-drop."
                ),
                "skills_required": ["HTML", "CSS", "JavaScript basics"],
                "skills_learned": ["React", "Node.js", "Express", "MongoDB", "REST API", "JWT Auth"],
                "duration": "2–3 weeks",
                "portfolio_impact": 55,
                "resume_impact": 58,
                "hiring_value": 60,
                "companies_that_value": ["Startups", "SaaS companies", "Product agencies"],
                "dev_phases": [
                    "Phase 1 – Plan: Define data model, API endpoints, UI wireframes",
                    "Phase 2 – Build: Express REST API, MongoDB schemas, React UI with state management",
                    "Phase 3 – Test: Jest unit tests for API, Cypress E2E tests for UI",
                    "Phase 4 – Deploy: Vercel (frontend) + Railway (backend) with CI/CD"
                ]
            },
            {
                "title": "Weather Dashboard",
                "description": (
                    "Create a responsive weather dashboard that fetches real-time data from the OpenWeather "
                    "API, shows 7-day forecasts, and uses Chart.js for temperature trend visualizations."
                ),
                "skills_required": ["HTML", "CSS", "JavaScript", "Fetch API basics"],
                "skills_learned": ["REST APIs", "Async JavaScript", "Chart.js", "Responsive CSS", "LocalStorage"],
                "duration": "1–2 weeks",
                "portfolio_impact": 50,
                "resume_impact": 52,
                "hiring_value": 55,
                "companies_that_value": ["Frontend agencies", "Startups", "Web studios"],
                "dev_phases": [
                    "Phase 1 – Plan: API key setup, define data displayed, mobile-first layout",
                    "Phase 2 – Build: Async fetch, localStorage cache, Chart.js trend line",
                    "Phase 3 – Test: Cross-browser testing, API error state, offline graceful degradation",
                    "Phase 4 – Deploy: Vercel or Netlify with environment variable for API key"
                ]
            }
        ],
        "Intermediate": [
            {
                "title": "E-Commerce Platform",
                "description": (
                    "Build a full-featured e-commerce platform with product listings, search/filter, "
                    "cart management, Stripe payment integration, and an admin order dashboard."
                ),
                "skills_required": ["React", "Node.js", "MongoDB", "REST API", "JWT Auth"],
                "skills_learned": ["Stripe API", "Redux", "Admin Dashboards", "Payment Integration", "Image Upload"],
                "duration": "5–6 weeks",
                "portfolio_impact": 88,
                "resume_impact": 87,
                "hiring_value": 88,
                "companies_that_value": ["E-commerce", "Retail Tech", "SaaS", "Startups"],
                "dev_phases": [
                    "Phase 1 – Plan: Database schema, Stripe setup, admin vs user roles",
                    "Phase 2 – Build: Product CRUD, cart logic, Stripe checkout, admin panel",
                    "Phase 3 – Test: Payment flow with Stripe test cards, role-based access tests",
                    "Phase 4 – Deploy: Vercel + Railway with Stripe webhooks configured"
                ]
            },
            {
                "title": "Job Portal Application",
                "description": (
                    "Create a dual-sided job board where employers post jobs and candidates apply — "
                    "with search/filter, resume uploads, applicant tracking, and email notifications."
                ),
                "skills_required": ["React", "Node.js", "SQL/MongoDB", "REST API"],
                "skills_learned": ["Multi-Role Auth", "File Uploads (S3)", "Email (SendGrid)", "Search & Filter", "Pagination"],
                "duration": "5–6 weeks",
                "portfolio_impact": 87,
                "resume_impact": 88,
                "hiring_value": 89,
                "companies_that_value": ["HR Tech", "Recruiting Platforms", "SaaS"],
                "dev_phases": [
                    "Phase 1 – Plan: Dual-role schema, AWS S3 for resumes, email provider setup",
                    "Phase 2 – Build: Auth roles, job CRUD, application pipeline, SendGrid emails",
                    "Phase 3 – Test: Role switching tests, file upload validation, email delivery",
                    "Phase 4 – Deploy: Vercel + AWS EC2/Railway with S3 bucket for uploads"
                ]
            }
        ],
        "Advanced": [
            {
                "title": "SaaS Application Platform",
                "description": (
                    "Build a multi-tenant SaaS platform with team workspaces, subscription billing (Stripe), "
                    "feature flags, usage analytics, and a REST + GraphQL API layer."
                ),
                "skills_required": ["React", "Node.js", "PostgreSQL", "GraphQL", "Redis"],
                "skills_learned": ["Multi-Tenancy", "GraphQL", "Stripe Subscriptions", "Feature Flags", "Usage Analytics"],
                "duration": "8–10 weeks",
                "portfolio_impact": 96,
                "resume_impact": 95,
                "hiring_value": 96,
                "companies_that_value": ["SaaS Startups", "Enterprise Software", "Product Companies"],
                "dev_phases": [
                    "Phase 1 – Plan: Tenant isolation strategy, subscription plan tiers, GraphQL schema",
                    "Phase 2 – Build: Tenant middleware, GraphQL resolvers, Stripe subscription lifecycle",
                    "Phase 3 – Test: Multi-tenant isolation tests, subscription upgrade/downgrade flows",
                    "Phase 4 – Deploy: AWS ECS with Terraform IaC, CloudFront CDN, RDS PostgreSQL"
                ]
            },
            {
                "title": "Real-Time Collaboration Platform",
                "description": (
                    "Design a Notion/Figma-style real-time collaborative editor with WebSockets, "
                    "CRDT conflict resolution, presence indicators, and version history."
                ),
                "skills_required": ["React", "Node.js", "WebSockets", "Redis", "PostgreSQL"],
                "skills_learned": ["WebSockets", "CRDT", "Operational Transform", "Redis Pub/Sub", "Yjs"],
                "duration": "8–12 weeks",
                "portfolio_impact": 98,
                "resume_impact": 97,
                "hiring_value": 97,
                "companies_that_value": ["Collaboration Tools", "Notion-type Startups", "FAANG"],
                "dev_phases": [
                    "Phase 1 – Plan: Choose CRDT library (Yjs), design presence protocol, Redis channel topology",
                    "Phase 2 – Build: Yjs document store, Socket.io server, React collaborative editor UI",
                    "Phase 3 – Test: Multi-user conflict simulation, disconnect/reconnect sync tests",
                    "Phase 4 – Deploy: AWS ECS with auto-scaling, Redis ElastiCache, CloudFront"
                ]
            }
        ]
    }
}
