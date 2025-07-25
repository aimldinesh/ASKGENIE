![Python](https://img.shields.io/badge/python-3.11-blue)
![LLM Model](https://img.shields.io/badge/LLM-Groq--LLaMA3--70B-ff69b4)
![Deployment](https://img.shields.io/badge/deployment-Kubernetes%20on%20GCP-blueviolet)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![ArgoCD Dev](https://img.shields.io/badge/ArgoCD--Dev-Synced-brightgreen?logo=argo)
![ArgoCD Prod](https://img.shields.io/badge/ArgoCD--Prod-Healthy-brightgreen?logo=argo)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/aimldinesh/ASKGENIE)
![Issues](https://img.shields.io/github/issues/aimldinesh/ASKGENIE)

# 📘 AskGenie: AI-Powered Quiz Generator

**AskGenie** is a real-time AI-powered quiz and fill-in-the-blank generation app built using **Groq’s Llama 3.1 (70B)** model (`llama3-70b-8192`). Users can instantly generate topic-specific quizzes by selecting the type, difficulty, and number of questions.
This project follows full **MLOps + LLMOps** best practices — it is containerized with **Docker**, orchestrated using **Kubernetes**, and continuously delivered using **Jenkins + ArgoCD**.

---
## 📚 Table of Contents
- [🔄 Project Workflow ][#-project-workflow]
- [🧱 Project Architecture](#-project-architecture)
- [📌 Features](#-features)
- [🧪 Inputs & Functionality](#-inputs--functionality)
- [🛠️ Tech Stack](#-tech-stack)
- [📸 Project Screenshots](#-project-screenshots)
  - [🔧 Jenkins CI/CD Pipeline](#-jenkins-cicd-pipeline)
  - [🐳 Docker Image Build](#-docker-image-build)
  - [🚀 ArgoCD Deployment](#-argocd-deployment)
  - [🎯 AskGenie App UI – Quiz Generation](#-askgenie-app-ui--quiz-generation)
- [🔧 Prerequisites](#-prerequisites)
- [🧪 Local Setup](#-local-setup)
- [🐳 Docker Build & Run](#-docker-build--run)
- [🛠️ Full CI/CD Deployment Setup Instructions](#️-full-cicd-deployment-setup-instructions)
- [🤝 Contributors](#-contributors)

---

## 🔄 Project Workflow

```mermaid
    flowchart TD
        subgraph "🛠️ Dev & Setup"
            A1[📦 Project/API Setup]
            A2[⚙️ Configuration Code]
            A3[📄 Schemas & Models]
            A4[📝 Prompt Templates]
            A5[🔌 Groq Client Setup]
            A6[🧠 Question Generator]
            A7[🧰 Helper Classes]
            A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7
        end

        subgraph "💡 Application"
            B1[🧪 Main Application]
        end

        subgraph "📦 Versioning + Docker"
            C1[📂 Code Versioning]
            C2[🐳 Dockerfile]
            C1 --> C2
        end

        subgraph "🚀 Infra Deploy"
            D1[📦 Kubernetes Manifests]
            D2[🖥️ GCP VM Setup]
            D1 --> D2
        end

        subgraph "🔁 CI/CD Pipeline"
            E1[🔧 Jenkins Setup]
            E2[🔗 GitHub Integration]
            E3[📤 Build & Push Image]
            E4[🚦 ArgoCD Setup]
            E5[📬 WebHooks]
            E1 --> E2 --> E3 --> E4 --> E5
        end

        A7 --> B1
        B1 --> C1
        C2 --> D1
        D2 --> E3

```
---

## 🧱 Project Architecture

```mermaid
graph TD
    A[🧑 User] -->|Request: Generate Quiz| B[🌐 Streamlit Frontend]
    B --> C[🧠 Question Generator Logic]
    C --> D[📦 Prompt Templates + Helper Functions]
    C --> E[🔗 Groq LLM API LLaMA-3.1-8B-Instant]

    E -->|Response: Generated Questions| C
    C --> B
    B -->|Render Quiz| A

    subgraph Deployment
      F[🐳 Docker Container] --> G[Kubernetes Pod llmops-app]
      G --> H[☁️ GCP VM Instance]
    end

    B --> F
    F --> G
    G --> H

    subgraph CI/CD
      I[🔧 Jenkins] --> J[📥 Build & Push Docker Image]
      J --> K[🚀 ArgoCD]
      K --> G
    end

    H -->|Exposed| A

```
---

## 📌 Features

- 🔍 **Custom Quiz Generation** – Choose **topic**, **question type** (MCQ/Fill in the Blank), **difficulty**, and **number of questions**
- ⚙️ **Groq LLM Integration** – Uses **Groq API** with `llama3-70b-8192` for fast, context-rich question generation
- 🎯 **Streamlit UI** – Intuitive, responsive interface for a seamless user experience
- 🐳 **Dockerized App** – Lightweight, portable, and production-ready
- ☸️ **Kubernetes Deployment** – Scalable app deployed on **GCP VM** (via Minikube or GKE)
- 🚀 **CI/CD Pipeline** – End-to-end automation with **Jenkins + ArgoCD + GitHub Webhooks**

---

## 🧪 Inputs & Functionality
| Input Field                | Description                               |
| -------------------------- | ----------------------------------------- |
| 🧠 **Question Type**       | MCQ or Fill in the Blank                  |
| 📚 **Topic**               | Subject area like AI, History, Math, etc. |
| 🎯 **Difficulty**          | Easy / Medium / Hard                      |
| 🔢 **Number of Questions** | Choose from 1 to 10                       |

---

## 🛠️ Tech Stack
| Layer                | Tools Used                          |
| -------------------- | ----------------------------------- |
| 💻 **UI**            | Streamlit                           |
| 🧠 **LLM**           | Groq API (`llama3-70b-8192`)        |
| 🧪 **Backend**       | Python (Modular, Functional Design) |
| 🐳 **Container**     | Docker                              |
| ☸️ **Orchestration** | Kubernetes (Minikube / GKE)         |
| 🔧 **CI/CD**         | Jenkins + GitHub + ArgoCD           |
| ☁️ **Cloud**         | Google Cloud VM                     |

---
## 📸 Project Screenshots

### 🔧 Jenkins CI/CD Pipeline

- ✅ **Pipeline Start**

  ![Jenkins Pipeline Start](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/Jenkins_pipeline/jenkins%20pipeline%20build%20start.PNG)

- ✅ **Pipeline Success**

  ![Jenkins Pipeline Success](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/Jenkins_pipeline/jenkins%20pipeline%20build%20success.PNG)

---

### 🐳 Docker Image Build

- 📦 **Docker Images Built**

  ![Docker Images](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/Docker_Image/docker_images.PNG)

---

### 🚀 ArgoCD Deployment

- 🔄 **ArgoCD Sync and Health Status**

  ![ArgoCD Sync](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/ArgoCD/argocd_image_1.PNG)

---

### 🎯 AskGenie App UI – Quiz Generation

- 🧠 **MCQ Question Generation – Page 1**

  ![MCQ Image 1](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/Quiz_Generation_ui/app_image_1_mcq.PNG)

- 🧠 **MCQ Question Generation – Page 2**

  ![MCQ Image 2](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/Quiz_Generation_ui/app_image_2_mcq.PNG)

- ✍️ **Fill-in-the-Blank Question Interface**

  ![Fill in the Blank](https://github.com/aimldinesh/ASKGENIE/blob/main/screenshots/Quiz_Generation_ui/app_image_3_fill_in_blank.png)

---
## 🔧 Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.11+
- Docker
- Groq API Key (signup at [Groq Cloud](https://console.groq.com/))
- GCP VM or Localhost for deployment
- (Optional) Jenkins, ArgoCD if deploying CI/CD pipeline

## 🧪 Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/aimldinesh/ASKGENIE.git
cd ASKGENIE

# 2. Create virtual environment & activate
python -m venv venv
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate     # for Windows

# 3. Install dependencies
pip install -e .

# 4. Set up Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run locally
streamlit run app.py
```
--- 

## 🐳 Docker Build & Run
```bash
# Build Docker image
docker build -t askgenie .

# Run container
docker run -p 8501:8501 askgenie
```

---

## 🛠️ Full CI/CD Deployment Setup Instructions
For detailed end-to-end deployment steps—including Docker build, Kubernetes deployment on GCP, Jenkins CI/CD pipeline, GitHub integration, ArgoCD sync, and GitOps automation—check the guide below:

[View Full Setup Instructions →](./complete_setup.md).

Credit: Huge thanks to Data Guru for the full setup documentation that made this deployment seamless.

## 🤝 Contributors
- [Dinesh Chaudhary](https://github.com/aimldinesh)