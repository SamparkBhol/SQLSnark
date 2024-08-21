# SQLSnark

🎉 Welcome to SQLSnark! This project is a smart and interactive chatbot that assists users in constructing, executing, and troubleshooting SQL queries. It's built using Python, Flask, and NLP libraries, with an intuitive and animated frontend for a seamless user experience.

## ✨ Features
- **Automatic Query Generation**: Generate SQL queries based on natural language input.
- **Query Validation and Execution**: Validate and execute queries on an integrated database.
- **Database Schema Exploration**: Visualize and explore the database schema.
- **Memory and Contextual Understanding**: The chatbot retains context within a session.
- **Advanced Frontend**: An animated and responsive user interface.

## 🛠️ Technology Stack
- **Backend**: Python, Flask, spaCy (or NLTK), SQLite (or PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **NLP Libraries**: spaCy (or NLTK)

## 🚀 Getting Started
### Prerequisites
- Python 3.7+
- Flask
- spaCy (or NLTK)
- Modern web browser

### Installation

1. **Clone the Repository**:
   git clone https://github.com/yourusername/sql-snark.git
   cd sql-snark

2. **Set Up a Virtual Environment**:
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**:
   pip install -r requirements.txt  

4. **Download NLP Model (if using spaCy)**:
   python -m spacy download en_core_web_sm

### Running the Application

1. **Start the Backend**:
   cd backend/
   python app.py

2. **Open the Frontend**:
   Navigate to the `frontend/` directory.
   Open `index.html` in your web browser.

3. **Interact with the Chatbot**:
   Start chatting with the assistant, and it will help you construct and execute SQL queries!

## 👥 Contributors
Sampark Bhol

## 🐛 Issues 
 For issues feel free to rasie issue or do any PRs as I will highly appreciate if you say ways to improvement or any bugs in code ...

## 🚧 Known Issues
- 🐛 Sometimes the chatbot might not handle complex queries well.
- ⚠️ Users may experience delays with large databases.

