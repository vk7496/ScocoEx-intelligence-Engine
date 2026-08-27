import json
import os
import time
from pathlib import Path

import streamlit as st
from groq import Groq

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="SCOCOEX Global Week 2028",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Global styling: RTL + Persian font
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"]  {
    font-family: 'Vazirmatn', sans-serif !important;
    direction: rtl;
}
.main .block-container { direction: rtl; text-align: right; }
section[data-testid="stSidebar"] { direction: rtl; text-align: right; }
.stChatMessage { direction: rtl; text-align: right; }

.scocoex-header { text-align: center; padding: 1.5rem 0 1rem 0; border-bottom: 1px solid #1e293b; margin-bottom: 1.5rem; }
.scocoex-badge {
    background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 0.3rem 1rem; border-radius: 999px; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.scocoex-title {
    font-size: 2.2rem; font-weight: 900;
    background: linear-gradient(90deg, #fde68a, #fbbf24, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0.6rem 0 0.2rem 0;
}
.kpi-card { background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b; border-radius: 1rem; padding: 1.1rem 1.2rem; }
.kpi-label { color: #94a3b8; font-size: 0.75rem; }
.kpi-value { color: #ffffff; font-size: 1.3rem; font-weight: 900; margin-top: 0.2rem; }
.kpi-tag   { font-size: 0.7rem; margin-top: 0.4rem; display: block; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Knowledge base — loaded from markdown files that live in this same
# GitHub repo, under /knowledge/. Edit those .md files to update what
# the AI is allowed to know; you never need to touch this Python file
# to change the content.
# ------------------------------------------------------------------
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

TENANT_META = {
    "golrang": {
        "label": "گروه صنعتی گلرنگ",
        "file": "golrang.md",
        "kpis": [
            ("کریدورهای فعال", "۴ هاب منطقه‌ای", "عمان و GCC"),
            ("مدل توسعه بازار", "Export → JV", "پایدار و امن"),
            ("هدف مقیاس", "Fortune Global 500", "بین‌المللی"),
        ],
        "metrics": [
            ("ضریب نفوذ در هاب‌های منطقه‌ای (عمان و GCC)", 78),
            ("آمادگی زیرساخت لجستیک و زنجیره تامین بین‌المللی", 85),
            ("انتقال از مدل صادراتی به سرمایه‌گذاری مشترک (JV)", 64),
        ],
    },
    "nicico": {
        "label": "صنایع ملی مس ایران (NICICO)",
        "file": "nicico.md",
        "kpis": [
            ("اتاق‌های تخصصی", "۴ اتاق کلیدی", "فعال در اجلاس"),
            ("میزهای مذاکره B2B", "۱۲ میز هدفمند", "بین‌المللی"),
            ("پنجره بازار", "سال ۲۰۲۸", "برقی‌سازی و AI"),
        ],
        "metrics": [
            ("قراردادهای خریداران بلندمدت (Offtake Agreements)", 92),
            ("یکپارچه‌سازی فناوری و هوش مصنوعی در استخراج", 70),
        ],
    },
    "bonyad": {
        "label": "بنیاد مستضعفان",
        "file": "bonyad.md",
        "kpis": [
            ("شرکت‌های پورتفو", "۳۰ شرکت", "ارزیابی‌شده"),
            ("شرکت‌های خارجی هدف", "۳۰۰ شرکت", "دعوت‌شده"),
            ("موتورهای توسعه‌ای", "۵ موتور", "فعال"),
        ],
        "metrics": [
            ("ارزیابی و آماده‌سازی ۳۰ شرکت برتر پورتفو", 95),
            ("جذب شرکای خارجی و دعوت از هلدینگ‌های جهانی", 60),
        ],
    },
}


@st.cache_data(show_spinner=False)
def load_knowledge(filename: str) -> str:
    """Read a knowledge markdown file from the repo. Cached so the file
    is only read from disk once per session (edit + git push + redeploy
    to update it, no code change needed)."""
    path = KNOWLEDGE_DIR / filename
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


PARTNERS_TEXT = load_knowledge("partners.md")

# ------------------------------------------------------------------
# Docs center — real PDF/Word files that live in /docs in this same
# repo. Metadata (title, description, status) comes from
# docs/manifest.json so you never touch this Python file to add a
# new document: just drop the file in /docs and add one JSON entry.
# ------------------------------------------------------------------
DOCS_DIR = Path(__file__).parent / "docs"


@st.cache_data(show_spinner=False)
def load_docs_manifest() -> list[dict]:
    manifest_path = DOCS_DIR / "manifest.json"
    if not manifest_path.exists():
        return []
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

# ------------------------------------------------------------------
# Groq client
# ------------------------------------------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)
GROQ_MODEL = "llama-3.3-70b-versatile"  # free-tier Groq model; swap for llama-3.1-8b-instant if you want faster/cheaper

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def ask_groq(tenant_key: str, question: str) -> str:
    """Answer strictly from the tenant's knowledge file. If the client
    isn't configured, return a clear message instead of failing."""
    if client is None:
        return (
            "⚠️ کلید Groq API تنظیم نشده است. لطفاً GROQ_API_KEY را در "
            "Streamlit secrets یا متغیر محیطی قرار دهید."
        )

    context = load_knowledge(TENANT_META[tenant_key]["file"])

    system_prompt = f"""شما دستیار هوشمند SCOCOEX Global Week 2028 هستید.
فقط و فقط بر اساس اطلاعات زیر پاسخ بده. اگر پاسخ سوال در این اطلاعات نبود،
صادقانه بگو که این اطلاعات در پایگاه داده موجود نیست و حدس نزن.
پاسخ‌ها را کوتاه، حرفه‌ای و به زبان فارسی رسمی بنویس.

--- اطلاعات مرجع ---
{context}
---------------------
"""

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ خطا در ارتباط با Groq API: {e}"


# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
if "tenant" not in st.session_state:
    st.session_state.tenant = "golrang"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {k: [] for k in TENANT_META}

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ انتخاب هلدینگ و بخش‌ها")
    for key, t in TENANT_META.items():
        if st.button(t["label"], key=f"btn_{key}", use_container_width=True,
                     type="primary" if st.session_state.tenant == key else "secondary"):
            st.session_state.tenant = key
            st.rerun()

    st.markdown("---")
    status_color = "#34d399" if client else "#f87171"
    status_text = "موتور Groq فعال است" if client else "کلید Groq API یافت نشد"
    st.markdown(
        f"<div style='background:#0f172a;border:1px solid #1e293b;padding:1rem;border-radius:0.8rem;'>"
        f"<span style='color:{status_color};font-size:0.75rem;font-weight:700;'>● {status_text}</span>"
        "<p style='color:#94a3b8;font-size:0.7rem;margin-top:0.4rem;'>"
        "پاسخ‌های هوش مصنوعی فقط بر اساس فایل‌های دانش موجود در پوشه knowledge/ تولید می‌شوند.</p></div>",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown("""
<div class="scocoex-header">
    <span class="scocoex-badge">Smart & Spatial Cooperation Organizing Conference & Exhibition</span>
    <div class="scocoex-title">SCOCOEX GLOBAL WEEK 2028</div>
    <div style="color:#cbd5e1;font-size:0.95rem;font-weight:600;">
        موتور هوش اقتصادی و دیپلماسی تجاری ۲۰۲۸ | Smart & Spatial Cooperation
    </div>
    <div style="color:#94a3b8;font-size:0.75rem;margin-top:0.4rem;">
        🕊️ HUMANITY &nbsp;•&nbsp; 🤝 PEACE &nbsp;•&nbsp; 🌍 GLOBAL ECONOMY
    </div>
</div>
""", unsafe_allow_html=True)

current_key = st.session_state.tenant
current = TENANT_META[current_key]

tab1, tab2, tab3 = st.tabs(["🏢 پروفایل هلدینگ", "🌐 شرکا و شرکت‌های بین‌المللی", "📄 مرکز اسناد"])

# --- TAB 1 ---
with tab1:
    context_text = load_knowledge(current["file"])
    # First line of the markdown file is used as the on-screen title/desc
    lines = [l for l in context_text.splitlines() if l.strip()]
    title = lines[0].lstrip("# ").strip() if lines else current["label"]

    st.markdown(f"### {title}")

    cols = st.columns(len(current["kpis"]))
    for col, (label, value, tag) in zip(cols, current["kpis"]):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-label">{label}</span>
                <div class="kpi-value">{value}</div>
                <span class="kpi-tag" style="color:#34d399;">{tag}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("#### 📊 شاخص‌های پیشرفت")
    for label, pct in current["metrics"]:
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#94a3b8;'>"
            f"<span>{label}</span><span style='color:#60a5fa;font-weight:700;'>{pct}%</span></div>",
            unsafe_allow_html=True,
        )
        st.progress(pct / 100)

    with st.expander("📚 مشاهده منبع اطلاعات (knowledge file)"):
        st.markdown(context_text)

    st.markdown("#### 💬 اتاق پرسش و پاسخ هوشمند (مبتنی بر Groq)")

    for msg in st.session_state.chat_history[current_key]:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    prompt = st.chat_input("سوال خود را تایپ کنید...")
    if prompt:
        st.session_state.chat_history[current_key].append({"role": "user", "text": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("در حال تحلیل پاسخ..."):
                reply = ask_groq(current_key, prompt)
            st.write(reply)
        st.session_state.chat_history[current_key].append({"role": "assistant", "text": reply})

# --- TAB 2 ---
with tab2:
    st.markdown(PARTNERS_TEXT)

# --- TAB 3 ---
with tab3:
    st.markdown("### 📄 مرکز اسناد و ترجمه رسمی")
    st.caption(
        "برای افزودن سند جدید، فایل را در پوشه‌ی docs/ ریپازیتوری قرار دهید و یک "
        "رکورد در docs/manifest.json اضافه کنید — نیازی به تغییر این کد نیست."
    )

    docs = load_docs_manifest()

    if not docs:
        st.warning("هنوز هیچ سندی در docs/manifest.json ثبت نشده است.")
    else:
        for entry in docs:
            filename = entry.get("file", "")
            title = entry.get("title", filename)
            desc = entry.get("desc", "")
            status = entry.get("status", "")
            file_path = DOCS_DIR / filename
            file_exists = file_path.exists()

            col_info, col_action = st.columns([4, 1])
            with col_info:
                st.markdown(f"""
                <div class="kpi-card" style="margin-bottom:0.5rem;">
                    <div style="color:#60a5fa;font-weight:700;font-size:0.85rem;">📁 {title}</div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:0.2rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_action:
                if file_exists:
                    st.download_button(
                        label=f"⬇️ دانلود ({status})" if status else "⬇️ دانلود",
                        data=file_path.read_bytes(),
                        file_name=filename,
                        use_container_width=True,
                        key=f"dl_{filename}",
                    )
                else:
                    st.markdown(
                        "<div style='color:#fbbf24;font-size:0.75rem;text-align:center;padding-top:0.8rem;'>"
                        "⏳ فایل آپلود نشده</div>",
                        unsafe_allow_html=True,
                    )
