# TODO

**Context**: Transitioning from Ruby backend developer (4 years) to Python-focused AI/ML developer. This document tracks learning projects to explore new concepts, technologies, and improve existing skills.

## 1. tools-projects
Learn tool integrations with Python - all tools will be installed locally.

### Python tools/libraries integration

#### Containerization & Deployment
* **Docker**: Containerization for all projects
  - **Benefits**: Consistent environments, easy deployment, isolation
  - **Key Concepts**: Dockerfile, docker-compose, volumes, networks, multi-stage builds
  - **Python-Specific**: Virtual environments inside containers, pip requirements, alpine vs debian base images
  - **Best Practices**: Layer caching, .dockerignore, security scanning, resource limits
  - **Multi-Architecture**: Build for x86_64 (PC/Mac) and ARM (Raspberry Pi)

#### Data & Messaging
* **Redis**: `redis-py`
* **Kafka**: `confluent-kafka` or `kafka-python`
* **Sidekiq Alternatives** (Ruby specific):
    - **Celery**: The most powerful and widely used task queue in Python. It supports Redis, RabbitMQ, and Amazon SQS as brokers.
    - **RQ (Redis Queue)**: A simpler, lightweight alternative to Celery that is strictly backed by Redis.
    - **Huey**: Another "little" task queue for Python that supports Redis and is easy to set up. 

    **NOTE**: There are still ways to interact with Sidekiq from Python. If you have an existing Ruby application using Sidekiq and want a Python script to trigger jobs for it, you can push JSON-formatted job data directly into Redis.

## For a Python-based stack
There are excellent libraries that serve the same roles as Redis, Sidekiq, and Kafka in the Ruby ecosystem.

### Python Task Queues (Sidekiq Alternatives)
While Sidekiq is Ruby-specific, Python has several mature frameworks for background processing:
- **Celery**: The most popular and feature-rich asynchronous task queue. It is often considered the industry standard for Python, similar to how Sidekiq is for Ruby. It supports Redis as a broker and provides advanced features like task scheduling and retries.
- **RQ (Redis Queue)**: A lightweight, simple alternative that is strictly backed by Redis. It is easier to set up than Celery if you only need basic background processing.
- **Dramatiq**: A modern, high-performance background task library that focuses on simplicity and reliability over the complex feature set of Celery. 

### Redis Libraries for Python
To interact with Redis directly for caching or data storage:
- **redis-py**: The official and most widely used client for Redis in Python. For increased performance, you can install it with the hiredis parser.
- **RedisOM Python**: Provides high-level object mapping, allowing you to model your Redis data like an ORM.
- **RedisVL**: A specialized library if you are using Redis as a vector database for AI and LLM applications. 

### Kafka Libraries for Python
For event streaming and real-time data pipelines:
- **confluent-kafka-python**: The recommended choice for high-performance and production environments. It is a thin wrapper around the high-speed C-based librdkafka library.
- **kafka-python**: A pure Python implementation that is easy to install and use for smaller projects or environments where C-extensions are difficult to manage.
- **FastStream**: A modern asynchronous framework designed specifically for working with Kafka, Redis, and RabbitMQ with a syntax similar to FastAPI.
- **Quix Streams**: A Pythonic stream processing library that offers a Pandas-like DataFrame API for processing Kafka data.

### Project Ideas

#### 1. Assets Manager (Raspberry Pi 1GB RAM)
**Description**: Comprehensive asset tracking system developed on PC/Mac but deployed and running on Raspberry Pi with 1GB RAM.

**Asset Categories**:
- **Physical Assets**:
  - Electronics: laptop, mobile, watch, esp32, raspi3b, tablets, cameras
  - Other physical items with location tracking
- **Digital Assets**:
  - Software licenses and tools
  - Game libraries: PS3 games list, PS5 games list
  - Purchased software and subscriptions
- **Debts Tracking**:
  - Money borrowed from others
  - Money lent to others
  - Payment history and due dates

**Core Features**:
- **Search Functionality**: Quick search across all assets
- **Add Items**: Support for adding items with or without images
- **Image Management**: Optimized image storage for low-RAM environment
- **Multi-user Support**: Each user has isolated asset collections
- **User Authentication**: Secure login system
- **CRUD Operations**: Create, Read, Update, Delete for all asset types

**Technical Stack**:
- **Backend Server**: Flask (lightweight) or FastAPI (modern, async)
- **Database**:
  - SQLite (file-based, perfect for Raspi)
  - OR PostgreSQL (if more robust features needed)
- **Image Storage**:
  - Compressed/thumbnail generation
  - Optional external storage (network drive, cloud)
- **Authentication**: Flask-Login or FastAPI-Users
- **Frontend**:
  - Lightweight HTML/CSS/JS
  - OR minimal framework (Alpine.js, htmx)
  - Responsive design for mobile access

**Database Schema**:
```
Users Table:
- user_id, username, password_hash, email, created_at

Physical_Assets Table:
- asset_id, user_id, name, category, location, purchase_date,
  purchase_price, image_path, notes, status

Digital_Assets Table:
- asset_id, user_id, name, category, platform, license_key,
  purchase_date, purchase_price, expiry_date

Debts Table:
- debt_id, user_id, person_name, amount, type (borrowed/lent),
  date, due_date, status (paid/unpaid), notes
```

**Raspberry Pi Optimizations**:
- **Memory Management**: Limit image sizes, use pagination
- **Caching**: Redis (optional) for session management
- **Database**: Use connection pooling, index optimization
- **Static Files**: Serve through nginx (reverse proxy)
- **Process Management**: Use gunicorn with 2-3 workers max

**Docker Deployment**:
- **Docker Compose**: Multi-container setup (app + database + nginx)
- **Dockerfile**: Optimized for ARM architecture (Raspberry Pi)
- **Volume Mounts**: Persistent data and image storage
- **Environment Variables**: Configuration management
- **Resource Limits**: Memory and CPU constraints for Raspi

**Development Workflow**:
1. Develop on PC/Mac with full IDE support
2. Test locally with Docker (similar constraints via resource limits)
3. Build Docker image for ARM64/ARMv7
4. Deploy to Raspberry Pi via Docker Hub or local registry
5. Run with docker-compose for orchestration
6. Access via local network or VPN

**Docker Setup**:
```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["5000:5000"]
    volumes: ["./data:/app/data", "./images:/app/images"]
    environment: ["DATABASE_URL=sqlite:///data/assets.db"]
    mem_limit: 512m

  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes: ["./nginx.conf:/etc/nginx/nginx.conf"]
    mem_limit: 128m
```

**Optional Enhancements**:
- Export/Import functionality (CSV, JSON)
- Backup and restore features
- QR code generation for physical assets
- Barcode scanning support
- Reporting and analytics (asset value, debt summary)
- Email notifications for debt due dates

## 2. LLM-projects

### Concepts & Technologies
- **LangChain**: Framework for developing applications powered by language models
- **LangGraph**: Build stateful, multi-actor applications with LLMs
- **Vector Databases**: Store and retrieve embeddings for semantic search
- **RAG (Retrieval Augmented Generation)**: Enhance LLM responses with retrieved context
- **Agentic AI**: Build autonomous AI agents that can plan and execute tasks

### Local Setup
- **Ollama** installed locally (via Docker for consistency)
- **Available Models**:
  - llama3.1
  - llama3.2
  - phi3-mini
- **Docker Note**: All LLM projects will run in Docker containers with Ollama service

### Project Ideas

#### 1. Local Wikipedia Data Summarizer
**Description**: LLM reads locally saved Wikipedia data on different topics and summarizes/answers questions.
- **Model**: phi3-mini
- **Features**:
  - Read locally saved Wikipedia articles
  - Summarize content on demand
  - Answer questions based on the stored data
- **Technologies**: RAG, vector databases for efficient article retrieval

#### 2. LLM News-Reporter
**Description**: LLM with internet access to monitor and report news on user-defined topics.
- **Model**: llama3.1 or llama3.2
- **Features**:
  - Access to internet, news websites/articles, and Google search
  - Monitor user-saved keywords/favorites:
    - Technology: AI, LLM, Claude, OpenAI
    - Politics: USA-politics, Trump
    - Global issues: politics, war, scarcity, famine, etc.
  - Find and aggregate news on specified topics
  - Additional support for critical news categories (politics/war/scarcity/famine)
- **Technologies**: LangChain for web scraping, agentic AI for autonomous monitoring

#### 3. Intelligent Research Assistant (LangGraph Example)
**Description**: Multi-step research agent that demonstrates LangGraph's stateful workflow capabilities.
- **Model**: llama3.1
- **Features**:
  - Query Planning: LLM generates search queries based on questions
  - Information Gathering: Collects data from multiple sources
  - Quality Checking: LLM evaluates if information is sufficient
  - Iterative Refinement: Loops back to gather more info if needed
  - Synthesis: Generates comprehensive answer from gathered information
- **Technologies**: LangGraph for workflow orchestration, Ollama for local LLM

**Visual Flow**:
```
┌─────────┐
│ Planner │ ← Generates search queries
└────┬────┘
     │
     ↓
┌─────────┐
│Gatherer │ ← Collects information
└────┬────┘
     │
     ↓
┌─────────┐
│ Checker │ ← Evaluates if info is sufficient
└────┬────┘
     │
     ↓
  [Decision]
     ├─→ Enough? → Synthesizer → END
     └─→ Not enough? → Loop back to Planner
```

**Why LangGraph?**
- **State Management**: Track search history, gathered info, iteration count
- **Conditional Routing**: Different paths based on LLM decisions
- **Iterative Workflows**: Can loop back for refinement
- **Debuggable**: Each node is independently testable

**Application to News-Reporter Project**:
The News-Reporter can use similar LangGraph workflow:
```
keyword_monitor → news_searcher → relevance_filter → priority_classifier → summarizer
```
- Conditional routing for urgent news (politics/war/famine) vs regular news
- State tracks: monitored keywords, found articles, relevance scores, summaries

#### 4. Unified LLM Dashboard Application
**Description**: A single, integrated application that combines all LLM projects into one manageable platform with a centralized UI dashboard.

**Architecture Requirements**:
- **Heavily OOP-based**: Class-based architecture with inheritance, composition, and design patterns
- **Lightweight**: Minimal dependencies, optimized resource usage
- **Responsive**: Fast UI updates, async operations
- **Fast**: Efficient processing, caching where appropriate

**Core Features**:
- **UI Dashboard**: Central control panel for all LLM projects
- **Modular Project Sections**:
  - Wikipedia Summarizer module
  - News-Reporter module
  - Research Assistant module
- **Settings Management**: Per-project configuration and preferences
- **Unified Tool Integration**: Use only required tools from tools-project section:
  - Redis (for caching and task queues)
  - Celery/RQ (for background processing)
  - Vector databases (for embeddings storage)

**Technical Stack**:
- **Backend**: FastAPI (lightweight, async, fast)
- **Frontend**: Modern web framework (React/Vue/Svelte) or desktop app (PyQt/Tkinter)
- **State Management**: Redis for caching and session management
- **Task Queue**: RQ or Celery for background LLM operations
- **Database**: SQLite/PostgreSQL for settings and history
- **Vector Store**: ChromaDB or FAISS for embeddings
- **Containerization**: Docker & Docker Compose for orchestration

**Docker Architecture**:
```yaml
# docker-compose.yml
services:
  fastapi:
    build: ./backend
    volumes: ["./models:/app/models"]  # Ollama models
    environment: ["OLLAMA_HOST=ollama:11434"]

  ollama:
    image: ollama/ollama
    volumes: ["ollama_data:/root/.ollama"]

  redis:
    image: redis:alpine
    mem_limit: 256m

  worker:
    build: ./backend
    command: celery -A app.worker worker
    depends_on: [redis]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
```

**OOP Design Pattern**:
```
BaseProject (Abstract)
├── WikiSummarizer
├── NewsReporter
└── ResearchAssistant

BaseModule (Abstract)
├── LLMModule (handles model interactions)
├── StorageModule (handles data persistence)
├── CacheModule (Redis integration)
└── TaskQueueModule (background jobs)

DashboardController
├── ProjectManager
├── SettingsManager
└── UIRenderer
```

**Key Benefits**:
- Single point of access for all LLM projects
- Shared resources (models, cache, database)
- Consistent UI/UX across features
- Centralized settings and configuration
- Easy to extend with new projects