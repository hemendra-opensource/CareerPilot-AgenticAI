# Static Interview Question Bank
# Organized by: Role → Category → Difficulty
# Each question includes: question text, answer outline, and key evaluation points.

INTERVIEW_TEMPLATES = {

    # ─────────────────────────────────────────────
    # COMMON HR QUESTIONS (shared across all roles)
    # ─────────────────────────────────────────────
    "HR": {
        "Easy": [
            {
                "question": "Tell me about yourself.",
                "answer_outline": "Briefly describe your background, key skills, recent experience, and career goals.",
                "key_points": ["Structured response (past → present → future)", "Concise and relevant", "Enthusiasm for the role"]
            },
            {
                "question": "Why do you want to work here?",
                "answer_outline": "Align company mission/values with your career goals and show genuine research.",
                "key_points": ["Company-specific knowledge", "Personal motivation", "Long-term alignment"]
            },
            {
                "question": "What are your greatest strengths?",
                "answer_outline": "Mention 2–3 role-relevant strengths with a concrete example for each.",
                "key_points": ["Specificity over generality", "Backed by real examples", "Relevance to the role"]
            }
        ],
        "Medium": [
            {
                "question": "Describe a challenging situation you faced at work and how you resolved it.",
                "answer_outline": "Use STAR format: Situation, Task, Action, Result. Focus on your initiative and outcome.",
                "key_points": ["STAR format", "Problem-solving skills", "Measurable outcome"]
            },
            {
                "question": "Where do you see yourself in 5 years?",
                "answer_outline": "Show ambition aligned with company growth while demonstrating role commitment.",
                "key_points": ["Career goal clarity", "Realistic ambition", "Company alignment"]
            },
            {
                "question": "How do you handle tight deadlines and pressure?",
                "answer_outline": "Describe prioritization strategies, time management tools, and a real example.",
                "key_points": ["Concrete techniques", "Calm under pressure", "Delivery track record"]
            }
        ],
        "Hard": [
            {
                "question": "Tell me about a time you disagreed with a manager's decision. How did you handle it?",
                "answer_outline": "Show professional communication, data-driven reasoning, and respect for authority.",
                "key_points": ["Constructive communication", "Data-driven approach", "Team cohesion outcome"]
            },
            {
                "question": "How do you manage cross-functional collaboration with non-technical stakeholders?",
                "answer_outline": "Describe translation of technical concepts into business value with examples.",
                "key_points": ["Communication clarity", "Stakeholder empathy", "Business value framing"]
            }
        ]
    },

    # ─────────────────────────────────────────────
    # COMMON SCENARIO QUESTIONS (shared across all roles)
    # ─────────────────────────────────────────────
    "Scenario": {
        "Easy": [
            {
                "question": "If a team member is consistently missing deadlines, what would you do?",
                "answer_outline": "Describe a constructive, empathetic approach: private conversation, root cause, support plan.",
                "key_points": ["Empathy first", "Private communication", "Escalation path if necessary"]
            },
            {
                "question": "You are given a new project with no prior documentation. How do you start?",
                "answer_outline": "Outline stakeholder interviews, codebase exploration, and incremental documentation.",
                "key_points": ["Structured discovery", "Stakeholder communication", "Documentation habit"]
            }
        ],
        "Medium": [
            {
                "question": "Your product goes down in production at 2 AM. Walk me through your incident response.",
                "answer_outline": "Describe on-call alerts, triage, rollback strategy, communication, and post-mortem.",
                "key_points": ["Triage discipline", "Clear communication", "Post-mortem mindset"]
            },
            {
                "question": "A stakeholder demands a feature that conflicts with technical best practices. How do you respond?",
                "answer_outline": "Explain trade-offs transparently, propose alternatives, and document the decision.",
                "key_points": ["Technical advocacy", "Business alignment", "Documentation of trade-offs"]
            }
        ],
        "Hard": [
            {
                "question": "Design a system that must handle 1 million requests per second with 99.99% uptime.",
                "answer_outline": "Discuss load balancing, horizontal scaling, caching, CDN, circuit breakers, and monitoring.",
                "key_points": ["Scalability principles", "Fault tolerance", "Trade-off awareness"]
            },
            {
                "question": "You discover a critical security vulnerability in a system you did not build. What do you do?",
                "answer_outline": "Immediate containment, responsible disclosure, patch coordination, and post-mortem.",
                "key_points": ["Security-first mindset", "Responsible disclosure", "Team communication"]
            }
        ]
    },

    # ─────────────────────────────────────────────
    # TECHNICAL QUESTIONS PER ROLE
    # ─────────────────────────────────────────────
    "Technical": {
        "Data Scientist": {
            "Easy": [
                {
                    "question": "What is the difference between supervised and unsupervised learning?",
                    "answer_outline": "Supervised uses labeled data for prediction; unsupervised finds hidden patterns in unlabeled data.",
                    "key_points": ["Labeled vs unlabeled data", "Examples of each", "Use case awareness"]
                },
                {
                    "question": "What is the purpose of the Pandas library?",
                    "answer_outline": "Pandas provides DataFrames for tabular data manipulation, cleaning, and transformation in Python.",
                    "key_points": ["DataFrame structure", "Data cleaning use cases", "Common operations: groupby, merge, pivot"]
                },
                {
                    "question": "What is overfitting and how do you prevent it?",
                    "answer_outline": "Overfitting occurs when a model memorizes training data. Prevent with regularization, cross-validation, pruning.",
                    "key_points": ["Bias-variance trade-off", "Regularization techniques", "Validation strategies"]
                }
            ],
            "Medium": [
                {
                    "question": "Explain the difference between L1 and L2 regularization.",
                    "answer_outline": "L1 (Lasso) produces sparse models via absolute penalty; L2 (Ridge) distributes weights via squared penalty.",
                    "key_points": ["Sparsity from L1", "Weight shrinkage from L2", "When to use each"]
                },
                {
                    "question": "How do you handle class imbalance in a dataset?",
                    "answer_outline": "Techniques include SMOTE, oversampling, undersampling, class weights, and threshold adjustment.",
                    "key_points": ["Sampling techniques", "Metric selection (F1 vs Accuracy)", "Model threshold tuning"]
                },
                {
                    "question": "Explain cross-validation and why it matters.",
                    "answer_outline": "K-fold CV splits data into K folds for model evaluation, providing more robust performance estimates.",
                    "key_points": ["K-fold mechanics", "Generalization benefit", "Stratified CV for imbalanced data"]
                }
            ],
            "Hard": [
                {
                    "question": "Design an end-to-end machine learning pipeline for a churn prediction system.",
                    "answer_outline": "Covers data ingestion, feature engineering, model selection, training, evaluation, deployment, and monitoring.",
                    "key_points": ["Feature engineering depth", "Model selection rationale", "MLOps monitoring"]
                },
                {
                    "question": "Explain the curse of dimensionality and mitigation strategies.",
                    "answer_outline": "High dimensions cause data sparsity. Mitigate with PCA, feature selection, embeddings.",
                    "key_points": ["Data sparsity effects", "Dimensionality reduction techniques", "Distance metric degradation"]
                }
            ]
        },
        "Machine Learning Engineer": {
            "Easy": [
                {
                    "question": "What is the difference between a neural network and a decision tree?",
                    "answer_outline": "Neural nets learn hierarchical features; decision trees split data by feature thresholds.",
                    "key_points": ["Interpretability trade-off", "Data type suitability", "Training complexity"]
                },
                {
                    "question": "What is Docker and why is it used in ML projects?",
                    "answer_outline": "Docker containerizes applications ensuring consistent environments across dev, staging, and production.",
                    "key_points": ["Environment reproducibility", "Dependency isolation", "Deployment consistency"]
                },
                {
                    "question": "What is gradient descent?",
                    "answer_outline": "Gradient descent iteratively adjusts model parameters in the direction that reduces the loss function.",
                    "key_points": ["Loss minimization", "Learning rate role", "Variants: batch, mini-batch, stochastic"]
                }
            ],
            "Medium": [
                {
                    "question": "How do you deploy a PyTorch model to a REST API?",
                    "answer_outline": "Export model with TorchScript or ONNX, wrap with FastAPI/Flask, containerize with Docker.",
                    "key_points": ["Model serialization", "API framework choice", "Containerization for scaling"]
                },
                {
                    "question": "What is transfer learning and when would you use it?",
                    "answer_outline": "Reusing pre-trained model weights for a new task. Use when dataset is small or task is similar.",
                    "key_points": ["Pre-trained model benefits", "Fine-tuning strategy", "Domain similarity requirement"]
                },
                {
                    "question": "Explain the vanishing gradient problem.",
                    "answer_outline": "Gradients shrink during backpropagation in deep networks, slowing learning in early layers.",
                    "key_points": ["Backpropagation mechanics", "ReLU as mitigation", "Batch norm and residual connections"]
                }
            ],
            "Hard": [
                {
                    "question": "Design an MLOps pipeline for continuous training and deployment.",
                    "answer_outline": "Covers data versioning, experiment tracking, model registry, CI/CD, monitoring, and retraining triggers.",
                    "key_points": ["Data/model versioning", "CI/CD integration", "Drift detection and retraining"]
                },
                {
                    "question": "How would you optimize a deep learning model for production inference latency?",
                    "answer_outline": "Use quantization, pruning, ONNX export, TensorRT, batching, and hardware acceleration.",
                    "key_points": ["Quantization trade-offs", "Hardware acceleration", "Batching for throughput"]
                }
            ]
        },
        "Data Engineer": {
            "Easy": [
                {
                    "question": "What is ETL and why is it important?",
                    "answer_outline": "Extract-Transform-Load moves data from source systems into a warehouse in a structured format.",
                    "key_points": ["Pipeline stages", "Data quality role", "Tool examples: Airflow, dbt"]
                },
                {
                    "question": "What is the difference between a data warehouse and a data lake?",
                    "answer_outline": "Warehouse stores structured, processed data for analytics. Lake stores raw data in any format.",
                    "key_points": ["Schema on write vs read", "Use case differentiation", "Storage cost difference"]
                },
                {
                    "question": "What are the main features of Apache Spark?",
                    "answer_outline": "Spark provides distributed in-memory processing for large-scale data with RDDs, DataFrames, and streaming.",
                    "key_points": ["In-memory processing", "Fault tolerance", "Multi-language support"]
                }
            ],
            "Medium": [
                {
                    "question": "How do you design a scalable data ingestion pipeline?",
                    "answer_outline": "Use Kafka/Kinesis for streaming, batch jobs via Airflow, idempotent writes, and monitoring.",
                    "key_points": ["Streaming vs batch decision", "Idempotency", "Failure handling and retries"]
                },
                {
                    "question": "Explain the star schema and when to use it.",
                    "answer_outline": "Star schema has a central fact table linked to dimension tables. Best for OLAP analytical queries.",
                    "key_points": ["Fact vs dimension tables", "Query performance", "When to prefer snowflake schema"]
                },
                {
                    "question": "How do you handle late-arriving data in a streaming pipeline?",
                    "answer_outline": "Use watermarking, event-time windows, and upserts to account for out-of-order events.",
                    "key_points": ["Event time vs processing time", "Watermark configuration", "Correctness vs latency trade-off"]
                }
            ],
            "Hard": [
                {
                    "question": "Design a real-time analytics platform processing 10TB of daily data.",
                    "answer_outline": "Lambda/Kappa architecture, Kafka ingestion, Spark streaming, Delta Lake, and BI layer.",
                    "key_points": ["Architecture pattern choice", "Scalability strategy", "Cost and latency trade-offs"]
                },
                {
                    "question": "How would you ensure data quality at scale?",
                    "answer_outline": "Implement data contracts, schema validation, dbt tests, anomaly detection, and data lineage tracking.",
                    "key_points": ["Data contracts", "Automated testing", "Observability and alerting"]
                }
            ]
        },
        "AI Engineer": {
            "Easy": [
                {
                    "question": "What is a Large Language Model (LLM)?",
                    "answer_outline": "LLMs are neural networks trained on massive text corpora to understand and generate human language.",
                    "key_points": ["Transformer architecture", "Pre-training vs fine-tuning", "Emergent capabilities"]
                },
                {
                    "question": "What is prompt engineering?",
                    "answer_outline": "Designing input text to elicit desired outputs from LLMs through few-shot examples, instructions, and constraints.",
                    "key_points": ["Zero-shot vs few-shot", "Chain-of-thought prompting", "Output consistency techniques"]
                },
                {
                    "question": "What is a vector database and what problem does it solve?",
                    "answer_outline": "Vector DBs store embeddings for similarity search, enabling semantic retrieval over unstructured data.",
                    "key_points": ["Embedding concept", "Similarity metrics (cosine, dot product)", "Use case: RAG, search, recommendation"]
                }
            ],
            "Medium": [
                {
                    "question": "Explain Retrieval-Augmented Generation (RAG) and its benefits.",
                    "answer_outline": "RAG retrieves relevant documents from a vector store and passes them as context to an LLM for grounded generation.",
                    "key_points": ["Hallucination reduction", "Up-to-date knowledge", "Retrieval pipeline components"]
                },
                {
                    "question": "How does LangChain simplify building LLM applications?",
                    "answer_outline": "LangChain provides chains, agents, memory, and tool integration abstractions for orchestrating LLM workflows.",
                    "key_points": ["Chain composition", "Agent tool use", "Memory management patterns"]
                },
                {
                    "question": "What are the trade-offs between fine-tuning an LLM and using RAG?",
                    "answer_outline": "Fine-tuning bakes knowledge into weights (expensive, static); RAG retrieves at runtime (flexible, updatable).",
                    "key_points": ["Cost comparison", "Knowledge freshness", "Latency implications"]
                }
            ],
            "Hard": [
                {
                    "question": "Design a production-grade RAG pipeline for an enterprise knowledge base.",
                    "answer_outline": "Ingest → chunk → embed → store in vector DB → retrieve → rerank → generate with guardrails.",
                    "key_points": ["Chunking strategy", "Reranking layer", "Guardrails and evaluation"]
                },
                {
                    "question": "How do you evaluate and monitor an LLM application in production?",
                    "answer_outline": "Use metrics like RAGAS, faithfulness, answer relevance, latency, and hallucination rate monitoring.",
                    "key_points": ["RAGAS framework", "Latency SLAs", "Feedback loop for continuous improvement"]
                }
            ]
        },
        "Full Stack Developer": {
            "Easy": [
                {
                    "question": "What is the difference between HTML, CSS, and JavaScript?",
                    "answer_outline": "HTML structures content, CSS styles it, JavaScript adds interactivity and dynamic behavior.",
                    "key_points": ["Separation of concerns", "DOM role", "Browser rendering pipeline"]
                },
                {
                    "question": "What is REST and what are its core principles?",
                    "answer_outline": "REST is a stateless API style using HTTP verbs (GET, POST, PUT, DELETE) for resource manipulation.",
                    "key_points": ["Statelessness", "HTTP verb semantics", "Resource-based URLs"]
                },
                {
                    "question": "What is the difference between SQL and NoSQL databases?",
                    "answer_outline": "SQL is relational with fixed schemas; NoSQL is flexible with various data models (document, key-value, graph).",
                    "key_points": ["Schema flexibility", "Consistency vs availability", "Use case suitability"]
                }
            ],
            "Medium": [
                {
                    "question": "Explain React's virtual DOM and why it improves performance.",
                    "answer_outline": "Virtual DOM diffs against real DOM before updating, minimizing expensive re-renders.",
                    "key_points": ["Reconciliation algorithm", "Minimal DOM mutations", "Component re-render conditions"]
                },
                {
                    "question": "How do you secure a Node.js REST API?",
                    "answer_outline": "JWT auth, HTTPS, input validation, rate limiting, helmet.js headers, and CORS configuration.",
                    "key_points": ["JWT token strategy", "Input sanitization", "Rate limiting importance"]
                },
                {
                    "question": "Explain the event loop in JavaScript.",
                    "answer_outline": "The event loop processes the call stack and callback queue, enabling non-blocking async execution.",
                    "key_points": ["Call stack vs callback queue", "Microtask vs macrotask", "Async/await under the hood"]
                }
            ],
            "Hard": [
                {
                    "question": "Design a scalable full-stack architecture for a real-time collaborative document editor.",
                    "answer_outline": "React frontend, Node.js + Socket.io backend, CRDT for conflict resolution, Redis for pub/sub, MongoDB storage.",
                    "key_points": ["WebSocket management", "CRDT conflict resolution", "Horizontal scaling strategy"]
                },
                {
                    "question": "How do you implement CI/CD for a full stack application?",
                    "answer_outline": "GitHub Actions pipeline: lint → test → build → containerize → deploy with rollback strategy.",
                    "key_points": ["Pipeline stages", "Zero-downtime deployment", "Rollback mechanism"]
                }
            ]
        }
    }
}
