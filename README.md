# ApplyDost – Job Application Tracker

A full-stack web application that helps job seekers manage and track their job applications, interviews, statuses, and resumes, and application progress in one place.

## 🚀 Features

- 🔐 User Login & Registration
- 📝 Add, Edit and Delete Job Applications
- 📊 Application Dashboard with Statistics
- 🔎 Search and Filter Applications
- ↕️ Sort Applications
- 📌 Track Application Status
- 🗂️ Kanban-style Job Board
- 📅 Interview Tracking
- 📄 Upload PDF Resume for Applications
- ⬇️ Download Uploaded Resume
- 🗑️ Remove Resume
- 🌙 Dark Mode
- 📤 Export Applications to CSV
- 💾 SQLite Database

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite
- SQLAlchemy

### Tools
- Git
- GitHub
- Visual Studio Code

## 📂 Project Structure

```text
ApplyDost/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
├── instance/
│   └── jobtracker.db
│
└── uploads/
    └── resumes/

NOTE: The local database and uploaded resumes are excluded from GitHub using .gitignore.

HOW TO RUN LOCALLY 
1. Clone the repository
    git clone https://github.com/amritashiv25/ApplyDost-Pro.git

2. Open the project
   cd ApplyDost-Pro

3. Create a virtual environment
   python -m venv .venv

4. Activate the virtual environment 
   Windows:
           .venv\Scripts\activate

5. Install dependencies
   pip install -r requirements.txt

6. Run the application
   python app.py

7. Open in Browser
   https://127.0.0.1:5000

📄 Resume Management
ApplyDost allows users to upload a PDF resume for a specific job application.

Users can:
Upload a resume
Download the uploaded resume
Remove the resume
Maintain different resumes for different applications

📊 Application Tracking
The dashboard helps users keep track of their job search by organizing applications based on their current status.
Example statuses:
Applied
Interview
Offer
Rejected
Saved   

🎯 Purpose
ApplyDost was developed to provide a simple and centralized platform for managing job applications during the job search process.
Instead of maintaining application details across spreadsheets or notes, users can track companies, roles, application status, interviews, and resumes from a single dashboard.

🔮 Future Improvements
1.Email notifications for interviews
2.Job deadline reminders
3.Resume-to-JD keyword matching
4.Job portal API integration
5.Analytics and application success rate
6.Cloud database support
7.Deployment to a cloud platform

👩‍💻 Developer
Amrita Shivhare

BE – Computer Science & Engineering

**IF YOU FIND THIS PROJECT USEFUL, CONSIDER GIVING IT A STAR*


