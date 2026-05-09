# 📱 SMS Spam Detector — Streamlit App

A production-ready NLP web app that classifies SMS messages as **Spam** or **Ham** using a Multinomial Naive Bayes pipeline.

---

## 🚀 Deploy on Streamlit Cloud (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/sms-spam-detector.git
git push -u origin main
```

### Step 2 — Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository → Branch: `main` → Main file: `app.py`
5. Click **"Deploy!"**

> ⚠️ **Important:** Upload your `spam.csv` file to the same folder as `app.py` before pushing. Without it, the app uses a tiny built-in sample and results won't reflect the full model.

---

## 🖥️ Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download spaCy model
python -m spacy download en_core_web_sm

# 3. Place spam.csv in this folder

# 4. Run
streamlit run app.py
```

---

## 📁 File Structure

```
sms_spam_detector/
├── app.py               ← Main Streamlit application
├── spam.csv             ← Dataset (you must add this)
├── requirements.txt     ← Python dependencies
├── packages.txt         ← System packages (empty)
├── .streamlit/
│   └── config.toml      ← Dark theme config
└── README.md
```

---

## ✨ Features

| Page | Content |
|------|---------|
| 🔍 Classifier | Single-message + batch classification with probability gauge |
| 📊 Model Metrics | Confusion matrix, classification report, KPI cards |
| 📈 Data Explorer | Class distribution, message length histogram, searchable dataset |

---

## 🧠 Pipeline

```
Raw SMS → Punctuation Removal → Lowercasing → Tokenization
        → Stop Word Removal → Lemmatization → BoW Vectorization
        → Multinomial Naive Bayes → Spam / Ham
```

**Model:** Multinomial Naive Bayes · **Vectorizer:** Binary Bag-of-Words  
**Libraries:** NLTK · spaCy · scikit-learn · Plotly · Streamlit
