# 🎓 EduGenie – AI-Powered Learning Assistant

## 🌐 Live Demo

🔗 **Try EduGenie here:** https://edugenie-ai-assistant-pkfr.onrender.com/

## 📖 Project Overview

**EduGenie** is a lightweight, responsive, AI-powered learning assistant developed as part of the **Smart Bridge Internship (GenAI Track)**. It uses the **Google GenAI SDK** with the **Gemini 2.5 Flash** model to help students understand complex topics, generate quizzes, and summarize educational content in real time through a simple and user-friendly web interface.

---

## 📁 Project Structure

### 📄 `requirements.txt`

Lists all the Python dependencies required to run the application.

**Libraries Used**

* **FastAPI** – Builds the backend REST API.
* **Uvicorn** – Runs the FastAPI application.
* **Google GenAI SDK** – Connects securely with the Gemini API.
* **Jinja2** – Renders dynamic HTML templates.
* **python-multipart** – Handles form data submitted from the frontend.

---

### ⚙️ `main.py`

The main backend file that controls the application logic.

**Key Responsibilities**

* Handles routing for the home page and form submissions.
* Receives user-selected features and educational content.
* Connects with the **Gemini 2.5 Flash** model.
* Generates AI responses based on the selected learning feature.

---

### 🎨 `templates/index.html`

The frontend interface where users interact with EduGenie.

**Features**

* Responsive and clean user interface.
* Dropdown menu for selecting AI tools.
* Large text area for entering educational content.
* Lightweight CSS for fast loading and mobile compatibility.

---

# 🚀 Features

### 📚 1. Smart Question Answering

* Explains difficult academic concepts in simple language.
* Uses relatable examples and easy-to-understand explanations.

### 📝 2. AI Quiz Generator

* Creates multiple-choice quizzes from the provided study material.
* Generates **3 MCQs** along with the correct answers for self-assessment.

### 📄 3. Text Summarizer

* Summarizes lengthy chapters, notes, or articles.
* Produces concise key points while preserving important information.

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Uvicorn
* Google GenAI SDK
* Gemini 2.5 Flash
* Jinja2
* HTML5
* CSS3

---

## 🎯 Project Highlights

* AI-powered educational assistant
* Responsive web interface
* Fast and lightweight architecture
* Real-time Gemini AI integration
* Beginner-friendly design
* Supports learning, revision, and self-assessment

---

## 📌 Future Enhancements

* PDF and document upload support
* Flashcard generation
* Multi-language learning support
* Conversation history
* User authentication and personalized learning
