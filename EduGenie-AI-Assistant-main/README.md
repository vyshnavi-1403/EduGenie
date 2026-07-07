Project Overview: EduGenie
EduGenie is a lightweight, responsive, AI-powered learning assistant built for the GenAI track of the Smart Bridge Internship. It leverages the official Google GenAI SDK to turn complex educational content into structured, student-friendly resources in real-time.

📂 File Structure & Content Breakdown
Your repository contains exactly three core files that fulfill the entire technical requirement criteria cleanly:

1. requirements.txt (Dependencies)
What it is: The configuration file that lists the specific Python libraries needed to run the app.

What it contains: * fastapi & uvicorn: To build and power the high-performance local web server.

google-genai: The official Google client used to securely interact with the Gemini API.

jinja2: The templating engine that renders dynamic backend data into the frontend HTML template.

python-multipart: Allows the backend to read raw input data sent from the website's forms.

2. main.py (The Backend Core)
What it is: The server logic that runs your application, sets up endpoints, and manages API handshakes.

What it contains:

Routing Logic: Listens for incoming requests on the home page (/) and captures user input from the dropdown menu and text area.

Gemini Integration: Connects using the next-generation gemini-2.5-flash model. It dynamically changes its internal system prompts depending on the tool selected by the user.

3. templates/index.html (The Frontend UI)
What it is: The visual interface the user interacts with inside their browser.

What it contains:

Responsive HTML Form: Contains a clean selection dropdown to pick a feature and a spacious text box for educational inputs.

Embedded CSS: Uses lightweight styling to make sure the app loads fast, looks modern, and works smoothly on both desktop monitors and mobile devices.

🎯 Core Features Implemented
The application implements the three explicit criteria outlined in your internship rubric:

Feature 1: Intelligent Question Answering & Explanations * How it works: Takes difficult, dense academic topics and instructs Gemini to rewrite them using simple, intuitive analogies for quick student comprehension.

Feature 2: AI-Powered Quiz Generation

How it works: Analyzes any pasted text or learning material and instantly formats a neat 3-question multiple-choice quiz complete with answer keys for self-assessment.

Feature 3: Educational Text Summarization

How it works: Condenses massive textbook chapters, documents, or articles into bite-sized key takeaways without losing the core context.
