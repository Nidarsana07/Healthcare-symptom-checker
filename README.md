Healthcare Symptom Checker Chatbot 🩺

A web-based Healthcare Symptom Checker Chatbot developed using Python, Flask, HTML, CSS, JavaScript, and JSON. The application allows users to enter their symptoms and receive possible matches from a predefined symptom dataset, along with severity labels and general health advice.

📌 Project Overview

Understanding health symptoms can be challenging, especially when relevant information is scattered across different sources. This project provides a simple, interactive web application that helps users explore basic symptom-related information through a chatbot interface.

The system processes user-entered text and compares it with symptoms stored in a JSON dataset using rule-based matching. It displays relevant dataset matches and associated information to support preliminary health awareness.

Note: This application is an educational prototype. It does not provide a medical diagnosis or replace professional medical advice.

🎯 Objectives

Develop a user-friendly healthcare chatbot interface.

Store symptom and condition information in a structured JSON dataset.

Implement rule-based symptom matching using Python.

Display possible matches, severity labels, and general advice.

Provide an interactive web application using Flask.

Encourage responsible healthcare information access.

✨ Features

Interactive Chat Interface: Allows users to enter symptoms in natural language.

Symptom Matching: Compares user input with predefined symptom records.

Possible Condition Results: Displays relevant matches from the available dataset.

Severity Labels: Shows the severity category associated with matching records.

General Health Advice: Provides the advice stored in the dataset.

Structured Data Management: Uses JSON to maintain symptom-related records.

Web-Based Access: Runs in a browser through a Flask web application.

Input Validation: Supports handling of empty or invalid messages when implemented in the backend.

🛠️ Technologies Used

Technology

Purpose

Python

Backend logic and symptom matching

Flask

Web application framework and API routes

HTML5

Structure of the chatbot interface

CSS3

Styling and responsive layout

JavaScript

Chat interactions and communication with the backend

JSON

Storage of predefined symptom records

Gunicorn

Production WSGI server for deployment

GitHub

Source code management and version control

Render

Hosting and deployment of the Flask application

📂 Project Structure

healthcare-symptom-checker/
│
├── app.py
├── symptoms.json
├── requirements.txt
├── README.md
│
├── templates/
│   └── chat.html
│
└── static/
    ├── style.css
    └── chat.js

⚙️ Installation and Setup

Prerequisites

Ensure that the following are installed on your system:

Python 3

pip (Python package installer)

A code editor such as Visual Studio Code

A web browser

Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/healthcare-symptom-checker.git

Replace YOUR-USERNAME with your GitHub username.

Step 2: Open the Project Folder

cd healthcare-symptom-checker

Step 3: Create a Virtual Environment (Recommended)

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Step 4: Install Dependencies

Create a requirements.txt file containing:

Flask
gunicorn

Install the required packages:

pip install -r requirements.txt

Step 5: Run the Application

python app.py

Open the following address in your browser:

http://127.0.0.1:5000

The chatbot should now be accessible locally.

☁️ Deployment

The application can be deployed online using Render with GitHub as the source code repository.

Push the project files to GitHub.

Sign in to Render.

Create a new Web Service and connect the GitHub repository.

Configure the build command:

pip install -r requirements.txt

Configure the start command:

gunicorn app:app

Deploy the application and open the public URL provided by Render.

Important: GitHub Pages alone cannot run the Flask backend. Use a Python-compatible hosting service to deploy the complete application.

🔍 How It Works

The user enters symptoms through the chatbot interface.

JavaScript sends the message to the Flask backend.

The backend processes the input and compares it with symptom records in symptoms.json.

The rule-based matching logic identifies possible matches.

Flask returns the results to the frontend.

The chatbot displays the available matching information, severity labels, and general advice.

The results depend on the dataset and matching rules. They should not be interpreted as probabilities or confirmed medical findings.

⚠️ Limitations

The system relies on a predefined symptom dataset.

Matching accuracy depends on the dataset and the implemented rules.

Similar symptoms may occur in different medical conditions.

The application has not been established as a clinically validated diagnostic system.

The output may be incomplete or incorrect and should not be used as the sole basis for healthcare decisions.

🔮 Future Enhancements

Expand and clinically review the symptom dataset.

Improve symptom recognition and handling of alternative symptom descriptions.

Add multilingual support and accessibility improvements.

Introduce secure user feedback and testing mechanisms.

Evaluate matching performance using appropriately reviewed test cases.

Explore machine learning or generative AI only with suitable validation, safeguards, and reliable medical sources.

Strengthen privacy, security, and deployment monitoring.

🩺 Medical Disclaimer

This project is intended for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Do not delay seeking medical care because of information provided by this application. If you believe you are experiencing a medical emergency, contact local emergency services immediately.

👩‍💻 Author

Nidarsana P

Healthcare Symptom Checker Chatbot — Python and Flask Web Application.

📄 License

This project is available for educational and learning purposes. If you intend to distribute or reuse it, add an appropriate open-source license and verify that the dataset and any third-party resources permit your intended use.
