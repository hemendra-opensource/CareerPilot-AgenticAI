# Role-based roadmap templates and learning resources

ROADMAP_TEMPLATES = {
    "Data Scientist": {
        "stages": {
            "Beginner": ["Python", "SQL", "Data Visualization"],
            "Intermediate": ["Pandas", "NumPy", "Statistics"],
            "Advanced": ["Machine Learning", "Scikit-Learn"]
        },
        "resources": {
            "Python": {"docs": "https://docs.python.org/3/", "course": "FreeCodeCamp Python for Beginners", "practice": "HackerRank Python Tracks"},
            "SQL": {"docs": "https://www.postgresql.org/docs/", "course": "SQL Zoo Tutorial", "practice": "LeetCode Database Questions"},
            "Pandas": {"docs": "https://pandas.pydata.org/docs/", "course": "Kaggle Pandas Micro-course", "practice": "Pandas Practice Exercises"},
            "NumPy": {"docs": "https://numpy.org/doc/", "course": "NumPy Tutorial on W3Schools", "practice": "NumPy 100 Exercises"},
            "Statistics": {"docs": "https://openstax.org/books/introductory-statistics", "course": "Khan Academy College Statistics", "practice": "Brilliant.org Stats Practice"},
            "Machine Learning": {"docs": "https://scikit-learn.org/stable/", "course": "Andrew Ng Machine Learning Specialization", "practice": "Kaggle Playground Competitions"},
            "Scikit-Learn": {"docs": "https://scikit-learn.org/stable/user_guide.html", "course": "Scikit-Learn Course on FreeCodeCamp", "practice": "Kaggle Spaceship Titanic"},
            "Data Visualization": {"docs": "https://matplotlib.org/stable/users/index.html", "course": "Seaborn Tutorials", "practice": "Kaggle Data Visualization Course"}
        }
    },
    "Machine Learning Engineer": {
        "stages": {
            "Beginner": ["Python", "Git", "Linux"],
            "Intermediate": ["Machine Learning", "PyTorch", "TensorFlow"],
            "Advanced": ["Deep Learning", "Docker"]
        },
        "resources": {
            "Python": {"docs": "https://docs.python.org/3/", "course": "FreeCodeCamp Python for Beginners", "practice": "HackerRank Python Tracks"},
            "Git": {"docs": "https://git-scm.com/doc", "course": "Git & GitHub Crash Course", "practice": "Learn Git Branching Interactive"},
            "Linux": {"docs": "https://linuxjourney.com/", "course": "EdX Introduction to Linux", "practice": "OverTheWire Bandit Wargame"},
            "Machine Learning": {"docs": "https://scikit-learn.org/stable/", "course": "Andrew Ng Machine Learning Specialization", "practice": "Kaggle Playground Competitions"},
            "PyTorch": {"docs": "https://pytorch.org/docs/stable/index.html", "course": "PyTorch for Beginners on Coursera", "practice": "Build a Simple Neural Net"},
            "TensorFlow": {"docs": "https://www.tensorflow.org/api_docs", "course": "DeepLearning.AI TensorFlow Developer", "practice": "TensorFlow Tutorials Website"},
            "Deep Learning": {"docs": "https://www.deeplearning.ai/", "course": "Deep Learning Specialization", "practice": "Kaggle Digit Recognizer"},
            "Docker": {"docs": "https://docs.docker.com/", "course": "Docker for Beginners on KodeKloud", "practice": "Containerize a Flask Application"}
        }
    },
    "Data Engineer": {
        "stages": {
            "Beginner": ["Python", "SQL"],
            "Intermediate": ["ETL", "Data Warehousing", "AWS"],
            "Advanced": ["Spark", "Airflow"]
        },
        "resources": {
            "Python": {"docs": "https://docs.python.org/3/", "course": "FreeCodeCamp Python for Beginners", "practice": "HackerRank Python Tracks"},
            "SQL": {"docs": "https://www.postgresql.org/docs/", "course": "SQL Zoo Tutorial", "practice": "LeetCode Database Questions"},
            "ETL": {"docs": "https://www.redhat.com/en/topics/integration/what-is-etl", "course": "ETL Pipelines on Coursera", "practice": "Build a Local CSV-to-SQL Pipeline"},
            "Data Warehousing": {"docs": "https://docs.snowflake.com/", "course": "Data Warehousing Fundamentals", "practice": "Design Star/Snowflake Schema"},
            "AWS": {"docs": "https://docs.aws.amazon.com/", "course": "AWS Certified Cloud Practitioner Course", "practice": "Deploy a simple S3-to-Lambda stack"},
            "Spark": {"docs": "https://spark.apache.org/docs/latest/", "course": "Spark & Python for Big Data on Udemy", "practice": "Local PySpark processing tasks"},
            "Airflow": {"docs": "https://airflow.apache.org/docs/", "course": "Astronomer Airflow Academy", "practice": "Schedule a daily web scraper DAG"}
        }
    },
    "AI Engineer": {
        "stages": {
            "Beginner": ["Python", "FastAPI", "Prompt Engineering"],
            "Intermediate": ["LLMs", "LangChain", "RAG"],
            "Advanced": ["Vector Databases", "Docker"]
        },
        "resources": {
            "Python": {"docs": "https://docs.python.org/3/", "course": "FreeCodeCamp Python for Beginners", "practice": "HackerRank Python Tracks"},
            "FastAPI": {"docs": "https://fastapi.tiangolo.com/", "course": "FastAPI Crash Course on YouTube", "practice": "Build a Simple REST API"},
            "Prompt Engineering": {"docs": "https://www.promptingguide.ai/", "course": "ChatGPT Prompt Eng for Developers", "practice": "Perform Prompt Optimization Tasks"},
            "LLMs": {"docs": "https://huggingface.co/docs", "course": "Hugging Face Natural Language Processing", "practice": "Load local LLMs with Transformers"},
            "LangChain": {"docs": "https://python.langchain.com/docs/get_started/introduction", "course": "LangChain for LLM Apps on DeepLearning.ai", "practice": "Build a simple RAG chatbot"},
            "RAG": {"docs": "https://lilianweng.github.io/posts/2023-06-23-agent/", "course": "Advanced RAG on DeepLearning.ai", "practice": "Build a PDF Q&A Search Tool"},
            "Vector Databases": {"docs": "https://docs.trychroma.com/", "course": "Vector Databases Course on Coursera", "practice": "Setup a local Chroma vector database"},
            "Docker": {"docs": "https://docs.docker.com/", "course": "Docker for Beginners on KodeKloud", "practice": "Containerize a FastAPI Application"}
        }
    },
    "Full Stack Developer": {
        "stages": {
            "Beginner": ["HTML", "CSS", "JavaScript"],
            "Intermediate": ["React", "Git", "Node.js"],
            "Advanced": ["Express.js", "MongoDB"]
        },
        "resources": {
            "HTML": {"docs": "https://developer.mozilla.org/en-US/docs/Web/HTML", "course": "FreeCodeCamp HTML Responsive Design", "practice": "Build a static landing page"},
            "CSS": {"docs": "https://developer.mozilla.org/en-US/docs/Web/CSS", "course": "CSS Grid & Flexbox Crash Courses", "practice": "Style a personal profile site"},
            "JavaScript": {"docs": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "course": "JavaScript.info Modern Tutorial", "practice": "Codewars JavaScript Katas"},
            "React": {"docs": "https://react.dev/", "course": "React Course on Scrimba", "practice": "Build an interactive dashboard"},
            "Git": {"docs": "https://git-scm.com/doc", "course": "Git & GitHub Crash Course", "practice": "Learn Git Branching Interactive"},
            "Node.js": {"docs": "https://nodejs.org/en/docs/", "course": "Node.js Crash Course on FreeCodeCamp", "practice": "Build a local command CLI tool"},
            "Express.js": {"docs": "https://expressjs.com/", "course": "Full Stack Open Course (University of Helsinki)", "practice": "Build REST API backend endpoints"},
            "MongoDB": {"docs": "https://www.mongodb.com/docs/", "course": "MongoDB University Basics Course", "practice": "Design database collections schemas"}
        }
    }
}
