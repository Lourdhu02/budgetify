
# Budgetify – Personal Finance Tracker

A responsive full-stack web application to help users track expenses, set budgets, and visualize spending trends.  
Built with **Flask**, **SQLite**, **Bootstrap**, and **Chart.js**, and deployable on **Heroku**.

---

## 🚀 Features
- 📊 **Expense Tracking** – Add, edit, delete daily expenses with categories.
- 💵 **Budget Management** – Set monthly budgets and view remaining amounts.
- 📈 **Reports & Analytics** – Visualize spending trends using Chart.js.
- 📱 **Responsive UI** – Mobile-friendly design using Bootstrap.
- ☁ **Deployment Ready** – Deployable to Heroku with minimal configuration.

---

## 🛠 Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, Bootstrap 5, CSS, JavaScript, Chart.js
- **Deployment:** Heroku
- **Version Control:** Git & GitHub

---

## 📂 Project Structure
```

budgetify/
│
├── app.py                  # Main Flask application entry point
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for Heroku
├── Procfile                # Heroku entry point declaration
├── .gitignore              # Ignore virtual env, pycache, etc.
├── README.md               # Project documentation
│
├── config.py               # Configurations (DB, secret keys, etc.)
├── models.py               # Database models
├── forms.py                # WTForms (if used)
│
├── static/                 # Frontend static files
│   ├── css/style.css       # Custom styles
│   ├── js/charts.js        # Chart.js configurations
│   └── img/                # Static images
│
├── templates/              # HTML templates
│   ├── base.html           # Common layout
│   ├── index.html          # Dashboard/home
│   ├── add\_expense.html    # Expense form
│   ├── set\_budget.html     # Budget form
│   └── reports.html        # Charts & analytics
│
└── database/               # SQLite database files
└── budgetify.db        # Local database

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Lourdhu02/budgetify.git
cd budgetify
````

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python app.py
```

Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---


## 👨‍💻 Author

**\[Lourdu Raju]**

