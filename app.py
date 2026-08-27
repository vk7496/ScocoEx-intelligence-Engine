import streamlit as st
import os
from docx import Document
from pypdf import PdfReader

# تنظیمات صفحه
st.set_page_config(
    page_title="SCOCOEX Global Week 2028 | Intelligent Dashboard",
    page_icon="🌍",
    layout="wide"
)

# استایل‌دهی و زیبایی‌بخش ظاهری
st.markdown("""
    <style>
    .main { background-color: #030712; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; color: #f8fafc; border-radius: 8px; padding: 10px 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #2563eb !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# هدر صفحه
st.markdown("<h1 style='text-align: center; color: #f59e0b; font-weight: 900;'>SCOCOEX GLOBAL WEEK 2028</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #94a3b8; font-size: 16px;'>موتور هوش اقتصادی، دیپلماسی تجاری و تحلیل پیشرفته</h3>", unsafe_allow_html=True)
st.markdown("---")

# تابع هوشمند برای خواندن همزمان فایل‌های Word (.docx) و PDF (.pdf)
def load_file_content(filename):
    if not os.path.exists(filename):
        return f"⚠️ فایل `{filename}` یافت نشد. لطفاً بررسی کنید که فایل در کنار app.py آپلود شده باشد."
    
    try:
        # اگر فایل ورد باشد
        if filename.endswith(".docx"):
            doc = Document(filename)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        
        # اگر فایل PDF باشد
        elif filename.endswith(".pdf"):
            reader = PdfReader(filename)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text if text.strip() else "⚠️ فایل PDF خالی است یا متنی در آن تشخیص داده نشد."
        
        else:
            return "فرمت فایل پشتیبانی نمی‌شود."
            
    except Exception as e:
        return f"خطا در خواندن فایل: {e}"

# منوی ناوبری سایدبار
st.sidebar.markdown("### 🎛️ انتخاب بخش و تحلیل‌ها")
menu = st.sidebar.radio(
    "مشاهده بخش‌ها:",
    [
        "🏢 گروه صنعتی گلرنگ و نمودارها",
        "⛏️ صنایع ملی مس (NICICO)",
        "🏛️ بنیاد مستضعفان",
        "💬 چت‌بات هوشمند اسکوکواکس",
        "📄 اسناد و فایل‌های پروژه (Word & PDF)"
    ]
)

# ----------------- تب ۱: گلرنگ و نمودارها -----------------
if menu == "🏢 گروه صنعتی گلرنگ و نمودارها":
    st.subheader("🏢 هلدینگ گروه صنعتی گلرنگ: اکوسیستم تجاری و مقیاس جهانی")
    st.write("بررسی و تحلیل استراتژی‌های توسعه بین‌المللی و هاب‌های منطقه‌ای.")

    col1, col2, col3 = st.columns(3)
    col1.metric("ضریب نفوذ منطقه‌ای (عمان/GCC)", "78%", "+12% رشد")
    col2.metric("آمادگی زنجیره تامین لجستیک", "85%", "بهینه")
    col3.metric("پروژه‌های سرمایه‌گذاری مشترک", "12 هاب", "فعال")

    st.markdown("#### 📊 شاخص‌های کلیدی عملکرد و توسعه بازار ۲۰۲۸")
    st.progress(0.78, text="ضریب نفوذ در بازارهای هدف (78%)")
    st.progress(0.85, text="آمادگی زیرساخت زنجیره تامین (85%)")
    st.progress(0.64, text="تغییر مدل از صادرات به JV (64%)")

    st.markdown("---")
    st.markdown("### 📄 متن اسناد مربوط به گلرنگ:")
    c1, c2 = st.columns(2)
    with c1:
        st.info("سند شماره ۱ گلرنگ")
        st.write(load_file_content("1.گلرنگ.docx"))
    with c2:
        st.info("سند شماره ۲ گلرنگ")
        st.write(load_file_content("2.گلرنگ.docx"))

# ----------------- تب ۲: مس -----------------
elif menu == "⛏️ صنایع ملی مس (NICICO)":
    st.subheader("⛏️ صنایع ملی مس ایران: اتاق‌های تخصصی مس")
    
    col1, col2 = st.columns(2)
    col1.metric("قراردادهای Offtake بلندمدت", "92%", "تایید شده")
    col2.metric("میزهای مذاکره B2B هدفمند", "12 میز", "فعال")

    st.markdown("#### پایش عملکرد اتاق‌های تخصصی هوش و مواد اولیه")
    st.progress(0.92, text="پیشرفت قراردادهای Offtake (92%)")

    st.markdown("---")
    st.markdown("### 📄 جزئیات برنامه پیشنهادی:")
    st.write(load_file_content("برنامه پیشنهادی برای صنایع ملی مس ایران.docx"))

# ----------------- تب ۳: بنیاد -----------------
elif menu == "🏛️ بنیاد مستضعفان":
    st.subheader("🏛️ بنیاد مستضعفان: پورتفوی هلدینگ و موتورهای توسعه‌ای")
    st.metric("شرکت‌های ارزیابی‌شده پورتفو", "۳۰ شرکت کلیدی", "آماده برای بازار جهانی")
    st.progress(0.95, text="آمادگی ساختار بین‌المللی (95%)")
    
    st.markdown("---")
    st.markdown("### 📄 متن پروپوزال بنیاد:")
    st.write(load_file_content("پيشنهاد به بنياد مستضعفان.docx"))

# ----------------- تب ۴: چت بات هوشمند -----------------
elif menu == "💬 چت‌بات هوشمند اسکوکواکس":
    st.subheader("💬 اتاق پرسش و پاسخ هوشمند SCOCOEX 2028")
    st.write("هر سوالی درباره استراتژی‌ها، هلدینگ‌ها یا هاب‌های منطقه‌ای دارید بپرسید:")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("سوال خود را اینجا تایپ کنید..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = f"تحلیل هوش مصنوعی اسکوکواکس برای پرسش «{prompt}»: این موضوع با سند چشم‌انداز ۲۰۲۸ و هاب‌های منطقه‌ای عمان همراستا است. پیشنهاد می‌شود جزئیات بیشتر در میز B2B بررسی گردد."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ----------------- تب ۵: اسناد و فایل‌های پروژه -----------------
elif menu == "📄 اسناد و فایل‌های پروژه (Word & PDF)":
    st.subheader("📄 مخزن فایل‌ها (پشتیبانی از Word و PDF)")
    
    # مثال برای خواندن یک فایل PDF یا ورد دلخواه
    target_file = st.text_input("نام دقیق فایل همراه با پسوند را وارد کنید (مثلا file.pdf یا text.docx):", "general introduction.docx")
    
    if target_file:
        st.markdown(f"**محتوای فایل `{target_file}`:**")
        st.text_area("خروجی متن:", load_file_content(target_file), height=350)

# فوتر
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 12px;'>SCOCOEX 2028 Intelligence Engine • Powered by Streamlit</p>", unsafe_allow_html=True)
