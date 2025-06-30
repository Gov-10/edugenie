 📚 EduGenie — AI-Powered Personalized Learning Platform

EduGenie is a full-stack, AI-integrated learning assistant built for students. It generates tailored quizzes, provides resume feedback, stores academic records, and includes an intelligent chatbot — all in one platform.

> 🧠 Built with Django, PostgreSQL (NeonDB), AWS Lambda, Google Gemini, and modern web technologies.

---

## 🚀 Inspiration

In traditional learning systems, students often get overwhelmed by generalized content and lack personalized guidance. EduGenie was born to help students **learn smartly** using AI — whether by generating custom quizzes, getting resume advice, or interacting with a smart mentor chatbot.

---
🛠️ What It Does

- ✨ **AI-Generated Quizzes** based on selected topics, difficulty, and timing
- 📝 **Resume Tester** that uses AI to review and give personalized resume feedback
- 🧠 **EduBot Chatbot** for doubt resolution and nervous-exam-day encouragement
- 💬 **Testimonial Submission** with automatic AI moderation
- 🔐 **Login System** with student-type-based routing (school/college)

---

## 🏗️ How We Built It

- **Backend**: Django, Django REST Framework, PostgreSQL
- **Frontend**: HTML, Tailwind CSS, Vanilla JS
- **AI Integration**: Google Gemini 1.5 Flash via AWS Lambda
- **Authentication**: Django's built-in auth with user-type filtering
- **Database**: PostgreSQL (NeonDB)
---

## ☁️ AWS Services Used

| Service        | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| **AWS Lambda** | Serverless compute for Gemini-based and Bedrock AI tasks                |
| **Amazon SNS** | (Planned) For SMS-based OTP delivery and notifications                  |
| **IAM**        | Secure permission-based access to resources                             |
| **Amazon S3**  | Store files                                                             |
| **API Gateway** | Acts as a public HTTPS endpoint for lambda triggering                                                                                 |
| **AWS Bedrock** | Used in chatbot                                                        |
---
## 🔧 How AWS Lambda Was Used
We used **AWS Lambda** to offload all time-intensive and stateless AI-related tasks: (in conjuction with API Gateway)
### 1. 🎓 Quiz Generation
- When a student submits quiz preferences, Django sends a POST request to an AWS Lambda function.
- The Lambda function:
  - Builds a prompt for Gemini 1.5 Pro Latest.
  - Receives the quiz questions.
  - Parses the questions and sends them back to Django.
- ✅ Result: AI generation doesn't block the main server. Scalable and secure.
> 💡 Using AWS Lambda improved scalability, speed, and security — making the app cloud-ready and production-friendly.

---
# 🧠 Try It Yourself (make sure to setup .env file with Gemini API key, email host password, recaptcha keys, neonDB credentials and AWS credentials)

```bash
git clone https://github.com/Gov-10/edugenie
cd edugenie
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


## 🙌 Team
Built by:
- Govind S. (Full Stack Dev + AWS + AI Integration)
- Suryadeep V (Frontend Designing)