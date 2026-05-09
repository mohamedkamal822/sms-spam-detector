# 📱 SMS Spam Detector

An end-to-end **Natural Language Processing** project that detects spam SMS messages using a full text preprocessing pipeline and a Multinomial Naive Bayes classifier — deployed as an interactive web application with Streamlit.

---

## 🎯 Project Overview

SMS spam is a persistent problem — unsolicited messages ranging from prize scams to phishing attempts. This project builds a complete NLP pipeline that automatically classifies any SMS message as **Spam** or **Ham (legitimate)** with high accuracy.

The project covers the full machine learning lifecycle: raw data → exploratory analysis → preprocessing → feature engineering → model training → evaluation → deployment.

---

## 📊 Dataset

**SMS Spam Collection** — a public benchmark dataset widely used in NLP research.

| Property | Value |
|----------|-------|
| Total messages | 5,572 |
| Ham (legitimate) | 4,825 (86.6%) |
| Spam | 747 (13.4%) |
| Language | English |
| Source | UCI Machine Learning Repository |

The dataset is heavily imbalanced (≈6.5:1 ham-to-spam ratio), which is handled via **stratified train/test splitting** to preserve the class distribution in both sets.

---

## 🧠 NLP Pipeline

```
Raw SMS Message
      │
      ▼  [1] Punctuation Removal   — keeps $ and ! as spam signals
      │
      ▼  [2] Lowercasing           — unifies case variants
      │
      ▼  [3] Tokenization          — splits into word tokens (NLTK)
      │
      ▼  [4] Stop Word Removal     — drops filler words
      │
      ▼  [5] Lemmatization         — reduces words to base form
      │
      ▼  [6] Normalization         — fixes SMS abbreviations (n→and, wat→what)
      │
      ▼  [7] BoW Vectorization     — binary presence/absence matrix
      │
      ▼  [8] Naive Bayes Classifier
      │
      ▼
  SPAM 🚨  or  HAM ✅
```

### Why Binary Bag-of-Words?
Spam messages often repeat keywords aggressively. Binary BoW reduces the impact of that repetition and works particularly well with Naive Bayes on short texts.

### Why Multinomial Naive Bayes?
- Trains in milliseconds even on large vocabularies
- Proven baseline for text classification since the 1990s
- Naturally handles high-dimensional sparse feature spaces
- Uses prior class probabilities — well-suited for imbalanced data

---

## 🔬 Linguistic Feature Extraction (Bonus)

Beyond basic BoW features, the project includes advanced NLP analysis using **spaCy**:

### Part-of-Speech (POS) Tagging
Every token is assigned a grammatical role (noun, verb, adjective, etc.). Spam messages tend to use more imperative verbs, proper nouns, and numbers compared to ham. spaCy is chosen over NLTK for its context-aware neural tagger — significantly more accurate on informal SMS text.

### Named Entity Recognition (NER)
Real-world entities are identified and classified. Spam frequently references monetary values (`MONEY`), phone numbers (`CARDINAL`), and organizations (`ORG`) — all strong discriminative signals.

| NER Label | Spam Relevance | Example |
|-----------|---------------|---------|
| `MONEY` | 🔴 High | "Win $500" |
| `CARDINAL` | 🔴 High | "Call 08001234" |
| `ORG` | 🟡 Moderate | Company names |
| `DATE/TIME` | 🟡 Moderate | Urgency cues |

---

## 📈 Model Performance

Evaluated on a stratified 20% held-out test set:

| Metric | Ham | Spam |
|--------|-----|------|
| Precision | ~0.99 | ~0.97 |
| Recall | ~0.99 | ~0.94 |
| F1-Score | ~0.99 | ~0.96 |
| **Accuracy** | **~98.5%** | |

> Spam **recall** is the most critical metric — missing a phishing message is more harmful than a false alarm.

---

## 🖥️ Web Application

The Streamlit app has three pages:

**🔍 Classifier**
- Single-message classification with spam probability gauge
- Confidence scores for both classes
- Batch classification (one message per line) with CSV export
- Built-in example messages to try instantly

**📊 Model Metrics**
- KPI cards: Accuracy, Precision, Recall, F1
- Interactive confusion matrix heatmap
- Full per-class classification report

**📈 Data Explorer**
- Class distribution bar chart
- Message length histogram (spam vs. ham overlay)
- Searchable and filterable dataset table

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.10+ |
| NLP | NLTK, spaCy (`en_core_web_sm`) |
| ML | scikit-learn (Naive Bayes, CountVectorizer) |
| Visualization | Plotly |
| Web App | Streamlit |
| Data | pandas |

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/mohamedkamal822/sms-spam-detector.git
cd sms-spam-detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download spaCy model
python -m spacy download en_core_web_sm

# 4. Run the app
streamlit run app.py
```

---

## 📁 File Structure

```
sms-spam-detector/
├── app.py               ← Streamlit web application
├── NLP_Project.ipynb    ← Full analysis notebook
├── spam.csv             ← SMS Spam Collection dataset
├── requirements.txt     ← Python dependencies
├── config.toml          ← Streamlit dark theme config
└── README.md
```

---

## 👨‍💻 Author

**Mohamed Kamal Rashed**  
Computer Science Student · AI Major  
Faculty of Computers and Artificial Intelligence, Banha University  
DEPI Data Analytics & BI Program Graduate
