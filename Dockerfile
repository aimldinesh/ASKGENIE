## 🐍 Parent Image: Use official lightweight Python image
FROM python:3.10-slim

## ⚙️ Environment Variables:
# Prevent Python from writing .pyc files to disk
# Force stdout/stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## 📁 Set working directory inside the Docker container
WORKDIR /app

## 🔧 Install system-level dependencies required for building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## 📦 Copy all project files from local machine to the container
COPY . .

## 🚀 Install Python dependencies using setup.py in editable mode
RUN pip install --no-cache-dir -e .

## 🌐 Expose the default Streamlit port
EXPOSE 8501

## ▶️ Command to run your Streamlit application inside Docker
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
