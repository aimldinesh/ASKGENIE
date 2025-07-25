# 📘 AskGenie: AI-Powered Quiz Generator

**AskGenie** is a real-time AI-powered quiz generation app built using **Groq’s Llama 3.1 (70B)** model (`llama3-70b-8192`). Users can instantly generate topic-specific quizzes by selecting the type, difficulty, and number of questions.

This project follows full **MLOps + LLMOps** best practices — it is containerized with **Docker**, orchestrated using **Kubernetes**, and continuously deployed via **Jenkins + ArgoCD**.

---

## 📌 Features

- 🔍 **Custom Quiz Generation** - Select **topic**, **question type** (MCQ/Descriptive), **difficulty**, and **number of questions**.
- ⚙️ **Groq LLM Integration** - Powered by **Groq API** using `llama3-70b-8192` for **high-quality**, large-context, and accurate quiz generation.
- 🎯 **Clean UI with Streamlit** - Responsive and intuitive layout for seamless user interaction.
- 🐳 **Dockerized App** - Lightweight and portable container built with **Docker**.
- ☸️ **Kubernetes Deployment** - Fully scalable and deployed on a **GCP VM** via **Minikube** or **GKE**.
- 🚀 **CI/CD Pipeline** - Automated build and deployment using **Jenkins + ArgoCD**.

---

## 🧱 Architecture Overview

```mermaid
flowchart TD
    %% Development and Setup
    subgraph Development_and_Setup
        A1[Project and API Setup]
        A2[Configuration Code]
        A3[Question Schemas & Models Code]
        A4[Prompt Templates Code]
        A5[Groq Client Setup Code]
        A6[Question Generator Code]
        A7[Helper Class Codes]

        A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7
    end

    %% Application
    subgraph Application
        B1[Main Application]
    end

    %% Versioning and Containerization
    subgraph Versioning_and_Containerization
        C1[Code Versioning]
        C2[Dockerfile]
        C1 --> C2
    end

    %% Infrastructure and Deployment
    subgraph Infrastructure_and_Deployment
        D1[Kubernetes Manifests Files]
        D2[GCP VM Instance Setup]
        C2 --> D1
        D1 --> D2
    end

    %% CI/CD Pipeline
    subgraph CICD_Pipeline
        E1[Jenkins Setup]
        E2[GitHub Integration with Jenkins]
        E3[Build and Push Docker Image]
        E4[ArgoCD Setup]
        E5[WebHooks GitHub]

        E1 --> E2 --> E3 --> E4 --> E5
    end

    %% Cross-links
    A7 --> B1
    B1 --> C1
    B1 --> C2
    C2 --> D1
    D1 --> E3

```
