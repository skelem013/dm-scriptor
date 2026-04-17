# DM Scriptor - Setup & Deployment Guide

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/skelem013/dm-scriptor.git
cd dm-scriptor
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:8080` in your browser.

## 🗄️ Database Setup

The app uses SQLite by default. On first run, the database is automatically created.

For production, update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dm_scriptor
```

## 📦 Project Structure

```
dm-scriptor/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── Procfile             # Render deployment config
├── templates/           # HTML templates
│   ├── index.html       # Main scriptor page
│   ├── login.html       # Login page
│   ├── 404.html         # Error pages
│   └── 500.html
├── tests/               # Test suite
│   └── test_app.py      # Unit tests
└── README.md            # Project documentation
```

## 🧪 Running Tests

```bash
python -m pytest tests/
# or
python -m unittest tests.test_app
```

## 🌐 Deployment on Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set Environment Variables:
   - `FLASK_ENV=prod`
   - `SECRET_KEY=your_secret_key`
   - `PASSWORD=your_access_password`
   - `DATABASE_URL=your_postgres_url`

5. Deploy!

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Update `PASSWORD` for access control
- [ ] Use strong passwords/secrets
- [ ] Enable HTTPS (Render does this automatically)
- [ ] Review `.env` before committing (it's in .gitignore)

## 📈 Features

- ✅ Session-based authentication
- ✅ Mobile-first responsive design
- ✅ Copy-to-clipboard functionality
- ✅ Database-ready architecture
- ✅ Error handling with custom pages
- ✅ Production-ready with Gunicorn

## 🛠️ Troubleshooting

### Port already in use
```bash
PORT=3000 python app.py
```

### Database locked
Delete `dm_scriptor.db` and restart:
```bash
rm dm_scriptor.db
python app.py
```

### Module not found
Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 📞 Support

For issues, create a GitHub issue with:
- Error message
- Steps to reproduce
- Environment details

---

Built with ❤️ by Thato Mashabela
