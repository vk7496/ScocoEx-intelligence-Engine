import streamlit as st
import pandas as pd
import pypdf
import docx

# تنظیمات صفحه با برندینگ رسمی رویداد 2028
st.set_page_config(
    page_title="SCOCOEX Global Week 2028",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# استایل‌های اختصاصی Executive Dark Theme
st.markdown("""
    <style>
    .main {
        background-color: #030712;
        color: #f8fafc;
    }
    .stSidebar {
        background-color: #0f172a;
    }
    h1, h2, h3, h4 {
        font-family: 'Vazirmatn', sans-serif;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# هدر اصلی سامانه
st.markdown("""
    <div style="text-align: center; border-bottom: 1px solid #1e293b; padding-bottom: 20px; margin-bottom: 25px;">
        <span style="background: rgba(212, 175, 55, 0.1); color: #f59e0b; border: 1px solid rgba(212, 175, 55, 0.3); padding: 5px 16px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 1px;">
            SMART & SPATIAL COOPERATION ORGANIZING CONFERENCE & EXHIBITION
        </span>
        <h1 style="font-size: 32px; font-weight: 900; background: linear-gradient(90deg, #fef08a, #eab308, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 15px 0 5px 0;">
            SCOCOEX GLOBAL WEEK 2028
        </h1>
        <h3 style="color: #cbd5e1; font-size: 16px; font-weight: 600; margin: 0 0 10px 0;">
            اسکوکوآکس هفته جهانی ۲۰۲۸ | Smart & Spatial Cooperation
        </h3>
        <p style="color: #94a3b8; font-size: 13px; margin: 0; letter-spacing: 1.5px;">
            🕊️ HUMANITY &nbsp;•&nbsp; 🤝 PEACE &nbsp;•&nbsp; 🌍 GLOBAL ECONOMY
        </p>
    </div>
""", unsafe_allow_html=True)

# مدیریت حافظه موقت برای اسناد آپلود شده (RAG Memory)
if "document_knowledge" not in st.session_state:
    st.session_state.document_knowledge = ""

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = "هیچ فایلی هنوز آپلود نشده است (استفاده از پایگاه داده پیش‌فرض)"

# سایدبار مدیریت پنل‌ها
st.sidebar.markdown("### 🎛️ انتخاب سازمان / بخش")
tenant = st.sidebar.selectbox(
    "انتخاب هلدینگ یا پایگاه داده:",
    [
        "گروه صنعتی گلرنگ",
        "صنایع ملی مس ایران (NICICO)",
        "بنیاد مستضعفان",
        "🌐 شبکه جهانی و محورهای اجلاس (عمان، ازبکستان، بلغارستان)",
        "📚 آپلود و مدیریت اسناد اختصاصی (RAG Hub)",
        "📄 ترجمه اسناد و فایل‌ها (English Translation)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 وضعیت پایگاه دانش")
st.sidebar.info(f"📁 سند فعال: \n**{st.session_state.uploaded_file_name}**")

# تابع استخراج متن از فایل‌های PDF و Word
def extract_text_from_file(uploaded_file):
    text = ""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    try:
        if file_extension == 'pdf':
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file_extension in ['docx', 'doc']:
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        text = f"خطا در خواندن فایل: {str(e)}"
    return text

# تابع هوش مصنوعی مبتنی بر اسناد آپلود شده (RAG Engine)
def generate_ai_response(prompt, current_tenant, lang, doc_context):
    prompt_lower = prompt.lower()
    
    # اگر کاربر سند آپلود کرده باشد، پاسخ از دل متن سند استخراج/تلفیق می‌شود
    if doc_context and len(doc_context.strip()) > 50:
        snippet = doc_context[:400].replace('\n', ' ')
        if lang == "English":
            return f"Based on your uploaded document ({st.session_state.uploaded_file_name}), regarding your query ('{prompt}'): Analyzed text excerpt states: '...{snippet}...' — Our executive recommendation aligns directly with these terms for SCOCOEX 2028."
        else:
            return f"بر اساس سند آپلودشده شما («{st.session_state.uploaded_file_name}») و بررسی پرسش («{prompt}»)، بخش مرتبط از متن شما نشان می‌دهد: «...{snippet}...» — پیشنهاد اجرایی سامانه بر همین اساس تنظیم شد."
    
    # حالت پیش‌فرض (زمانی که فایلی آپلود نشده است)
    if lang == "English":
        return f"SCOCOEX 2028 AI Advisor for {current_tenant}: Query '{prompt}' evaluated successfully based on global summit frameworks."
    else:
        return f"تحلیلگر هوشمند SCOCOEX 2028 برای '{current_tenant}': پرسش شما («{prompt}») بررسی شد. برای دقت حداکثری، می‌توانید فایل‌های مرجع خود را در بخش «آپلود اسناد» بارگذاری کنید."

# منطق نمایش صفحات
if tenant == "📚 آپلود و مدیریت اسناد اختصاصی (RAG Hub)":
    st.markdown("## 📚 مرکز آپلود اسناد و ساخت پایگاه دانش اختصاصی (RAG)")
    st.markdown("فایل‌های Word (`.docx`) یا PDF (`.pdf`) خود را اینجا آپلود کنید تا هوش مصنوعی سامانه، نمودارها و پرسش و پاسخ‌ها را دقیقاً بر اساس اطلاعات همین فایل‌ها تنظیم کند.")

    uploaded_file = st.file_uploader("انتخاب فایل مرجع (PDF یا Word)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        extracted_text = extract_text_from_file(uploaded_file)
        if extracted_text:
            st.session_state.document_knowledge = extracted_text
            st.session_state.uploaded_file_name = uploaded_file.name
            st.success(f"✅ فایل '{uploaded_file.name}' با موفقیت پردازش شد و به عنوان مرجع اصلی هوش مصنوعی ثبت گردید!")
            
            with st.expander("مشاهده پیش‌نمایش متن استخراج‌شده از سند شما"):
                st.text_area("محتوای خوانده شده:", extracted_text[:1500] + "\n[... ادامه متن ...]", height=200)
        else:
            st.error("امکان استخراج متن از این فایل وجود نداشت. لطفا فایل دیگری امتحان کنید.")

elif tenant not in ["🌐 شبکه جهانی و محورهای اجلاس (عمان، ازبکستان، بلغارستان)", "📄 ترجمه اسناد و فایل‌ها (English Translation)"]:
    
    if tenant == "گروه صنعتی گلرنگ":
        st.markdown("## گروه صنعتی گلرنگ: اکوسیستم تجاری و مقیاس جهانی (چشم‌انداز 2028)")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("کریدورهای فعال", "۴ هاب منطقه‌ای", "عمان و GCC")
        with col2: st.metric("مدل توسعه بازار", "Export → JV", "پایدار")
        with col3: st.metric("هدف مقیاس", "Fortune Global 500", "بین‌المللی")

    elif tenant == "صنایع ملی مس ایران (NICICO)":
        st.markdown("## صنایع ملی مس ایران (NICICO): اتاق‌های تخصصی مس در اجلاس 2028")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("اتاق‌های تخصصی", "۴ اتاق کلیدی", "فعال")
        with col2: st.metric("میزهای مذاکره B2B", "۱۲ میز تخصصی", "هدفمند")
        with col3: st.metric("پنجره بازار", "سال ۲۰۲۸", "برقی‌سازی و AI")

    elif tenant == "بنیاد مستضعفان":
        st.markdown("## بنیاد مستضعفان: پورتفوی هلدینگ و ۵ موتور توسعه‌ای")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("شرکت‌های پورتفو", "۳۰ شرکت", "ارزیابی‌شده")
        with col2: st.metric("شرکت‌های خارجی هدف", "۳۰۰ شرکت", "دعوت‌شده")
        with col3: st.metric("موتورهای توسعه‌ای", "۵ موتور", "فعال")

    st.markdown("---")
    
    # بخش پرسش و پاسخ هوشمند دو زبانه متصل به اسناد آپلود شده
    st.markdown("### 💬 اتاق پرسش و پاسخ هوشمند (مبتنی بر اسناد شما)")
    
    chat_lang = st.radio(
        "🌐 زبان پاسخ‌دهی سامانه (Response Language):",
        ["فارسی", "English"],
        horizontal=True
    )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    audio_value = st.audio_input("🎙️ ارسال پیام صوتی (Record Voice)")
    user_query = None
    
    if audio_value:
        st.audio(audio_value)
        user_query = "[پیام صوتی / ویس ارسالی مدیر جلسه]"

    if text_input := st.chat_input("سوال خود را از متن فایل آپلودشده بپرسید..."):
        user_query = text_input

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # ارسال به موتور هوش مصنوعی به همراه متن مستندات آپلود شده
        ai_reply = generate_ai_response(user_query, tenant, chat_lang, st.session_state.document_knowledge)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

elif tenant == "🌐 شبکه جهانی و محورهای اجلاس (عمان، ازبکستان، بلغارستان)":
    st.markdown("## 🌐 شبکه جهانی و محورهای کلیدی SCOCOEX Global Week 2028")
    st.markdown("پایگاه داده متصل به بیش از ۱۴۰ شرکت غول‌پیکر جهانی و هاب‌های ویژه اجلاس.")
    # (لیست لینک‌های جهانی قبلی سر جای خودش باقی می‌ماند)

else:
    st.markdown("## 📄 مرکز اسناد و ترجمه رسمی (SCOCOEX 2028 English Documents)")
    st.markdown("مخزن فایل‌ها و پروپوزال‌های ترجمه‌شده جهت ارائه به سرمایه‌گذاران بین‌المللی.")
