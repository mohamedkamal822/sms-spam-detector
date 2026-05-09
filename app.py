import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import string
import re
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background: #0d0f14;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #13161f !important;
    border-right: 1px solid #1e2130;
}

/* Header */
.main-header {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.main-sub {
    font-size: 0.95rem;
    color: #6b7280;
    margin-top: 0.3rem;
    font-weight: 300;
}

/* Result cards */
.result-spam {
    background: linear-gradient(135deg, #1a0a0a 0%, #2d0f0f 100%);
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    text-align: center;
}
.result-ham {
    background: linear-gradient(135deg, #071a0f 0%, #0c2e1a 100%);
    border: 1px solid #14532d;
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    text-align: center;
}
.result-label {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 0.1em;
}
.result-desc {
    font-size: 0.9rem;
    color: #9ca3af;
    margin-top: 0.3rem;
}

/* Metric cards */
.metric-card {
    background: #13161f;
    border: 1px solid #1e2130;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #a78bfa;
}
.metric-label {
    font-size: 0.8rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* Badges */
.badge-spam {
    display: inline-block;
    background: #450a0a;
    color: #fca5a5;
    border: 1px solid #7f1d1d;
    border-radius: 6px;
    padding: 0.2rem 0.7rem;
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.badge-ham {
    display: inline-block;
    background: #052e16;
    color: #86efac;
    border: 1px solid #14532d;
    border-radius: 6px;
    padding: 0.2rem 0.7rem;
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* Section titles */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #6b7280;
    margin-bottom: 1rem;
    border-bottom: 1px solid #1e2130;
    padding-bottom: 0.5rem;
}

/* Textarea */
.stTextArea textarea {
    background: #13161f !important;
    border: 1px solid #1e2130 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.15) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a78bfa) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #13161f;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #6b7280 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: #1e2130 !important;
    color: #e8eaf0 !important;
}

/* Divider */
hr {
    border-color: #1e2130 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #13161f !important;
    border-radius: 8px !important;
    color: #9ca3af !important;
    font-size: 0.88rem !important;
}

/* Info/warning boxes */
.stAlert {
    background: #13161f !important;
    border-color: #1e2130 !important;
}

/* Hide default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Load model (cached) ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    import nltk
    import spacy
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        accuracy_score, classification_report, confusion_matrix
    )

    # NLTK downloads
    for pkg in ['punkt', 'punkt_tab', 'stopwords', 'wordnet']:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    stop_words   = set(stopwords.words('english'))
    lemmatizer_  = WordNetLemmatizer()

    # ── Preprocessing helpers ────────────────────────────────────────────────
    def remove_punctuation(text):
        keep = {'$', '!'}
        return "".join(c for c in text if c not in string.punctuation or c in keep)

    def preprocess(text):
        text   = remove_punctuation(text)
        text   = text.lower()
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in stop_words]
        tokens = [lemmatizer_.lemmatize(t) for t in tokens]
        text   = " ".join(tokens)
        text   = text.replace(' n ', ' and ').replace(' wat ', ' what ').replace(' la ', ' ')
        return text

    # ── Load dataset ─────────────────────────────────────────────────────────
    try:
        data = pd.read_csv('spam.csv', encoding='latin-1')[['v1', 'v2']]
        data.columns = ['label', 'message']
    except FileNotFoundError:
        # Fallback: tiny built-in sample so app still runs without the CSV
        samples = [
            ('ham',  'Hey, are we still on for tomorrow?'),
            ('ham',  'Can you pick up some groceries on your way home?'),
            ('ham',  'Great meeting today, talk soon.'),
            ('spam', 'WINNER!! Claim your free prize now! Call 08001234.'),
            ('spam', 'Urgent! You have won a $1000 gift card. Text WIN to 80800.'),
            ('spam', 'FREE entry into our $250 weekly competition. Text COMP to 87575.'),
        ] * 60
        data = pd.DataFrame(samples, columns=['label', 'message'])

    data['label_num']  = data['label'].map({'spam': 1, 'ham': 0})
    data['clean_text'] = data['message'].apply(preprocess)

    X_tr, X_te, y_tr, y_te = train_test_split(
        data['clean_text'], data['label_num'],
        test_size=0.2, random_state=42, stratify=data['label_num']
    )

    vec = CountVectorizer(binary=True)
    X_train_v = vec.fit_transform(X_tr)
    X_test_v  = vec.transform(X_te)

    clf = MultinomialNB()
    clf.fit(X_train_v, y_tr)

    y_pred  = clf.predict(X_test_v)
    acc     = accuracy_score(y_te, y_pred)
    report  = classification_report(y_te, y_pred, target_names=['Ham', 'Spam'], output_dict=True)
    cm      = confusion_matrix(y_te, y_pred)

    return {
        'model':      clf,
        'vectorizer': vec,
        'preprocess': preprocess,
        'data':       data,
        'metrics': {
            'accuracy': acc,
            'report':   report,
            'cm':       cm,
            'y_test':   y_te,
            'y_pred':   y_pred,
        }
    }


# ── Predict helper ────────────────────────────────────────────────────────────
def predict(text, bundle):
    cleaned = bundle['preprocess'](text)
    vec     = bundle['vectorizer'].transform([cleaned])
    pred    = bundle['model'].predict(vec)[0]
    proba   = bundle['model'].predict_proba(vec)[0]
    return pred, proba, cleaned


# ── Chart helpers ─────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9ca3af', family='DM Sans'),
    margin=dict(l=10, r=10, t=40, b=10),
)

def cm_chart(cm):
    fig = px.imshow(
        cm, text_auto=True,
        color_continuous_scale='Purp',
        labels=dict(x='Predicted', y='Actual'),
        x=['Ham', 'Spam'], y=['Ham', 'Spam'],
        title='Confusion Matrix',
    )
    fig.update_layout(**PLOT_LAYOUT, title_font_color='#e8eaf0',
                      coloraxis_showscale=False)
    fig.update_traces(textfont_size=16)
    return fig

def dist_chart(data):
    vc  = data['label'].value_counts().reset_index()
    fig = px.bar(vc, x='label', y='count', title='Class Distribution',
                 color='label',
                 color_discrete_map={'ham': '#22c55e', 'spam': '#ef4444'},
                 text_auto=True)
    fig.update_layout(**PLOT_LAYOUT, title_font_color='#e8eaf0',
                      showlegend=False, xaxis_title='', yaxis_title='Count')
    fig.update_traces(textposition='outside')
    return fig

def proba_gauge(spam_prob):
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=spam_prob * 100,
        number={'suffix': '%', 'font': {'color': '#e8eaf0', 'size': 28,
                                         'family': 'Space Mono'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#6b7280',
                     'tickfont': {'color': '#6b7280'}},
            'bar':  {'color': '#ef4444' if spam_prob > 0.5 else '#22c55e'},
            'steps': [
                {'range': [0, 40],  'color': '#052e16'},
                {'range': [40, 60], 'color': '#1c1917'},
                {'range': [60, 100],'color': '#450a0a'},
            ],
            'threshold': {'line': {'color': '#a78bfa', 'width': 2},
                          'thickness': 0.75, 'value': 50},
        },
        title={'text': 'Spam Probability', 'font': {'color': '#6b7280', 'size': 13}},
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      font_color='#9ca3af', height=220,
                      margin=dict(l=20, r=20, t=30, b=10))
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  APP LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem'>
        <div style='font-family:Space Mono,monospace;font-size:1.1rem;
                    font-weight:700;color:#e8eaf0'>📱 SMS Spam<br>Detector</div>
        <div style='font-size:0.78rem;color:#4b5563;margin-top:0.3rem'>
            NLP · Naive Bayes · v1.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        '', ['🔍 Classifier', '📊 Model Metrics', '📈 Data Explorer'],
        label_visibility='collapsed'
    )

    st.markdown('<div class="section-title" style="margin-top:2rem">Pipeline</div>',
                unsafe_allow_html=True)
    steps = [
        ('1', 'Punctuation Removal'),
        ('2', 'Lowercasing'),
        ('3', 'Tokenization'),
        ('4', 'Stop Word Removal'),
        ('5', 'Lemmatization'),
        ('6', 'BoW Vectorization'),
        ('7', 'Naive Bayes'),
    ]
    for num, label in steps:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:0.6rem;
                    padding:0.3rem 0;border-bottom:1px solid #1e2130'>
            <span style='font-family:Space Mono,monospace;font-size:0.7rem;
                         color:#a78bfa;width:16px;text-align:right'>{num}</span>
            <span style='font-size:0.8rem;color:#9ca3af'>{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:2rem;font-size:0.75rem;color:#374151;
                border-top:1px solid #1e2130;padding-top:1rem'>
        Dataset: SMS Spam Collection<br>
        5,572 messages · NLTK · spaCy
    </div>
    """, unsafe_allow_html=True)


# ── Load ──────────────────────────────────────────────────────────────────────
with st.spinner('Loading model…'):
    bundle = load_model()

data    = bundle['data']
metrics = bundle['metrics']


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — CLASSIFIER
# ══════════════════════════════════════════════════════════════════════════════
if page == '🔍 Classifier':
    st.markdown("""
    <div style='padding: 0.5rem 0 2rem'>
        <div class='main-header'>SMS Spam Detector</div>
        <div class='main-sub'>Paste any SMS message to classify it as spam or legitimate</div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_result = st.columns([1.1, 0.9], gap='large')

    with col_input:
        st.markdown('<div class="section-title">Input Message</div>',
                    unsafe_allow_html=True)
        user_text = st.text_area(
            '', height=160,
            placeholder='Type or paste an SMS message here…',
            label_visibility='collapsed'
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            classify_btn = st.button('CLASSIFY →', use_container_width=True)
        with c2:
            examples = {
                'Spam example': "WINNER!! You've been selected. Call 08001234 to claim $500 prize NOW!",
                'Ham example':  "Hey, can we reschedule our meeting to Thursday afternoon?",
            }
            choice = st.selectbox('Load example', ['—'] + list(examples.keys()),
                                  label_visibility='collapsed')
            if choice != '—':
                user_text = examples[choice]
                st.rerun()

        # Batch section
        st.markdown('<div class="section-title" style="margin-top:2rem">Batch Classify</div>',
                    unsafe_allow_html=True)
        batch_input = st.text_area(
            '', height=110,
            placeholder='One message per line…',
            label_visibility='collapsed',
            key='batch'
        )
        batch_btn = st.button('RUN BATCH →', use_container_width=True)

    with col_result:
        st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)

        if classify_btn and user_text.strip():
            with st.spinner('Analysing…'):
                time.sleep(0.3)
                pred, proba, cleaned = predict(user_text, bundle)

            spam_p = proba[1]
            ham_p  = proba[0]

            if pred == 1:
                st.markdown(f"""
                <div class='result-spam'>
                    <div class='result-label' style='color:#ef4444'>🚨 SPAM</div>
                    <div class='result-desc'>This message is likely unsolicited spam</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-ham'>
                    <div class='result-label' style='color:#22c55e'>✅ HAM</div>
                    <div class='result-desc'>This message appears to be legitimate</div>
                </div>
                """, unsafe_allow_html=True)

            st.plotly_chart(proba_gauge(spam_p), use_container_width=True,
                            config={'displayModeBar': False})

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value' style='color:#22c55e'>{ham_p:.1%}</div>
                    <div class='metric-label'>Ham confidence</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value' style='color:#ef4444'>{spam_p:.1%}</div>
                    <div class='metric-label'>Spam confidence</div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander('Show preprocessed text'):
                st.code(cleaned, language=None)

        elif classify_btn:
            st.warning('Please enter a message first.')
        else:
            st.markdown("""
            <div style='display:flex;align-items:center;justify-content:center;
                        height:300px;color:#374151;font-size:0.9rem;
                        border:1px dashed #1e2130;border-radius:12px;
                        text-align:center;line-height:1.8'>
                Enter a message and click<br>
                <strong style='color:#a78bfa;font-family:Space Mono,monospace'>
                CLASSIFY →</strong>
            </div>
            """, unsafe_allow_html=True)

    # Batch results
    if batch_btn and batch_input.strip():
        st.markdown('---')
        st.markdown('<div class="section-title">Batch Results</div>',
                    unsafe_allow_html=True)
        lines = [l.strip() for l in batch_input.splitlines() if l.strip()]
        rows  = []
        for msg in lines:
            p, prb, _ = predict(msg, bundle)
            rows.append({
                'Message':     msg[:80] + ('…' if len(msg) > 80 else ''),
                'Prediction':  'SPAM' if p == 1 else 'HAM',
                'Spam %':      f"{prb[1]:.1%}",
                'Ham %':       f"{prb[0]:.1%}",
            })
        df_batch = pd.DataFrame(rows)

        def color_row(row):
            c = '#1a0a0a' if row['Prediction'] == 'SPAM' else '#071a0f'
            return [f'background-color:{c}'] * len(row)

        st.dataframe(
            df_batch.style.apply(color_row, axis=1),
            use_container_width=True, hide_index=True
        )
        csv = df_batch.to_csv(index=False).encode()
        st.download_button('⬇ Download CSV', csv, 'batch_results.csv',
                           'text/csv', use_container_width=False)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — MODEL METRICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == '📊 Model Metrics':
    st.markdown("""
    <div style='padding: 0.5rem 0 2rem'>
        <div class='main-header'>Model Metrics</div>
        <div class='main-sub'>Evaluation results on 20% held-out test set</div>
    </div>
    """, unsafe_allow_html=True)

    rep = metrics['report']
    acc = metrics['accuracy']

    # Top KPI row
    kpis = [
        ('Accuracy',  f"{acc:.2%}",                      '#a78bfa'),
        ('Spam Prec', f"{rep['Spam']['precision']:.2%}",  '#ef4444'),
        ('Spam Rec',  f"{rep['Spam']['recall']:.2%}",     '#f97316'),
        ('Spam F1',   f"{rep['Spam']['f1-score']:.2%}",   '#22c55e'),
    ]
    cols = st.columns(4)
    for col, (label, val, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:{color}'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('')

    col_cm, col_rep = st.columns(2, gap='large')

    with col_cm:
        st.markdown('<div class="section-title">Confusion Matrix</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(cm_chart(metrics['cm']),
                        use_container_width=True,
                        config={'displayModeBar': False})

    with col_rep:
        st.markdown('<div class="section-title">Classification Report</div>',
                    unsafe_allow_html=True)
        for cls in ['Ham', 'Spam']:
            r = rep[cls]
            color = '#22c55e' if cls == 'Ham' else '#ef4444'
            st.markdown(f"""
            <div style='background:#13161f;border:1px solid #1e2130;
                        border-left:3px solid {color};border-radius:10px;
                        padding:1rem 1.3rem;margin-bottom:0.8rem'>
                <div style='font-family:Space Mono,monospace;font-size:0.85rem;
                             color:{color};font-weight:700;margin-bottom:0.6rem'>
                    {cls.upper()}
                </div>
                <div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0.5rem'>
                    {''.join(f"""
                    <div style='text-align:center'>
                        <div style='font-size:1.1rem;font-weight:600;
                                    font-family:Space Mono,monospace;color:#e8eaf0'>
                            {r[k]:.2f}
                        </div>
                        <div style='font-size:0.7rem;color:#6b7280;
                                    text-transform:uppercase;letter-spacing:0.05em'>
                            {k.replace('-score','').replace('f1','F1')}
                        </div>
                    </div>
                    """ for k in ['precision','recall','f1-score','support'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Macro / weighted
        for avg in ['macro avg', 'weighted avg']:
            r = rep[avg]
            st.markdown(f"""
            <div style='background:#0d0f14;border:1px solid #1e2130;border-radius:8px;
                        padding:0.7rem 1.3rem;margin-bottom:0.5rem;
                        display:flex;align-items:center;gap:1rem'>
                <span style='font-size:0.78rem;color:#6b7280;
                              font-family:Space Mono,monospace;min-width:100px'>
                    {avg.upper()}
                </span>
                <span style='font-size:0.85rem;color:#9ca3af'>
                    P: <b style='color:#e8eaf0'>{r['precision']:.3f}</b> &nbsp;
                    R: <b style='color:#e8eaf0'>{r['recall']:.3f}</b> &nbsp;
                    F1: <b style='color:#e8eaf0'>{r['f1-score']:.3f}</b>
                </span>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DATA EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif page == '📈 Data Explorer':
    st.markdown("""
    <div style='padding: 0.5rem 0 2rem'>
        <div class='main-header'>Data Explorer</div>
        <div class='main-sub'>SMS Spam Collection — 5,572 labeled messages</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.markdown('<div class="section-title">Class Distribution</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(dist_chart(data),
                        use_container_width=True,
                        config={'displayModeBar': False})

    with col2:
        st.markdown('<div class="section-title">Message Length Distribution</div>',
                    unsafe_allow_html=True)
        data['msg_len'] = data['message'].str.len()
        fig = px.histogram(
            data, x='msg_len', color='label', nbins=50,
            color_discrete_map={'ham': '#22c55e', 'spam': '#ef4444'},
            barmode='overlay', opacity=0.75,
            title='', labels={'msg_len': 'Characters', 'count': 'Messages'},
        )
        fig.update_layout(**PLOT_LAYOUT, showlegend=True,
                          legend=dict(x=0.75, y=0.95,
                                      font=dict(color='#9ca3af')))
        st.plotly_chart(fig, use_container_width=True,
                        config={'displayModeBar': False})

    # Dataset sample
    st.markdown('<div class="section-title" style="margin-top:1rem">Dataset Sample</div>',
                unsafe_allow_html=True)

    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        label_filter = st.selectbox('Filter by label', ['All', 'Ham', 'Spam'],
                                    label_visibility='collapsed')
    with search_col:
        search_term = st.text_input('', placeholder='Search messages…',
                                    label_visibility='collapsed')

    display_df = data[['label', 'message']].copy()
    if label_filter != 'All':
        display_df = display_df[display_df['label'] == label_filter.lower()]
    if search_term:
        display_df = display_df[display_df['message'].str.contains(
            search_term, case=False, na=False)]

    def style_label(val):
        if val == 'spam':
            return 'color: #ef4444; font-weight: 600'
        return 'color: #22c55e; font-weight: 600'

    st.dataframe(
        display_df.head(50).style.applymap(style_label, subset=['label']),
        use_container_width=True, hide_index=True, height=350
    )
    st.caption(f'Showing {min(50, len(display_df))} of {len(display_df)} messages')
