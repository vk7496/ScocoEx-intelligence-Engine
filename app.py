import streamlit as st
import os
from docx import Document

# تنظیمات صفحه
st.set_page_config(
    page_title="SCOCOEX Global Week 2028 | Intelligent Dashboard",
    page_icon="🌍",
    layout="wide"
)

# تابع کمکی برای خواندن متن فایل‌های ورد (.docx)
def load_docx_text(file_name):
    if os.path.exists(file_name):
        try:
            doc = Document(file_name)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            return "\n\n".join(full_text)
        except Exception as e:
            return f"خطا در خواندن فایل: {e}"
    else:
        return f"⚠️ فایل `{file_name}` در پوشه اصلی یافت نشد. لطفاً بررسی کنید که فایل در کنار app.py آپلود شده باشد."

# هدر اصلی داشبورد
st.markdown("<h1 style='text-align: center; color: #f59e0b;'>SCOCOEX GLOBAL WEEK 2028</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #94a3b8; font-size: 16px;'>موتور هوش اقتصادی، دیپلماسی تجاری و اسناد راهبردی</h3>", unsafe_allow_html=True)
st.markdown("---")

# منوی ناوبری در سایدبار
st.sidebar.markdown("### 🎛️ انتخاب بخش و اسناد راهبردی")
menu_option = st.sidebar.radio(
    "مشاهده محتوا:",
    [
        "🌍 معرفی عمومی و اهداف کلان",
        "🏢 گروه صنعتی گلرنگ",
        "⛏️ صنایع ملی مس ایران (NICICO)",
        "🏛️ بنیاد مستضعفان",
        "💰 مدل تامین سرمایه و پروپوزال‌ها",
        "📅 برنامه اجرایی ۱۲ روزه"
    ]
)

# بخش ۱: معرفی عمومی
if menu_option == "🌍 معرفی عمومی و اهداف کلان":
    st.header("🌍 معرفی عمومی و اهداف کلان اقتصادی")
    st.write("محتوای استخراج‌شده از اسناد رسمی معرفی و بازارهای کلان:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("مقدمه عمومی")
        content_gen = load_docx_text("general introduction.docx")
        st.text_area("general introduction.docx", content_gen, height=300)
    
    with col2:
        st.subheader("بازار و اهداف کلان اقتصادی")
        content_macro = load_docx_text("بازار و اهداف اقتصادی کلان اسکوکواکس 5.docx")
        st.text_area("بازار و اهداف کلان", content_macro, height=300)

# بخش ۲: گروه صنعتی گلرنگ
elif menu_option == "🏢 گروه صنعتی گلرنگ":
    st.header("🏢 هلدینگ گروه صنعتی گلرنگ")
    st.write("بررسی و تحلیل استراتژی‌های توسعه بین‌المللی گلرنگ:")
    
    tab1, tab2 = st.tabs(["بخش اول گلرنگ", "بخش دوم گلرنگ"])
    with tab1:
        st.markdown("### سند شماره ۱ گلرنگ")
        st.write(load_docx_text("1.گلرنگ.docx"))
    with tab2:
        st.markdown("### سند شماره ۲ گلرنگ")
        st.write(load_docx_text("2.گلرنگ.docx"))

# بخش ۳: صنایع ملی مس ایران
elif menu_option == "⛏️ صنایع ملی مس ایران (NICICO)":
    st.header("⛏️ صنایع ملی مس ایران")
    st.write("برنامه پیشنهادی اتاق‌های تخصصی مس و زنجیره تامین:")
    st.markdown(load_docx_text("برنامه پیشنهادی برای صنایع ملی مس ایران.docx"))

# بخش ۴: بنیاد مستضعفان
elif menu_option == "🏛️ بنیاد مستضعفان":
    st.header("🏛️ بنیاد مستضعفان انقلاب اسلامی")
    st.write("پروپوزال‌ها و ارزیابی شرکت‌های پورتفوی بنیاد:")
    st.markdown(load_docx_text("پيشنهاد به بنياد مستضعفان.docx"))

# بخش ۵: مدل تامین سرمایه و پروپوزال‌ها
elif menu_option == "💰 مدل تامین سرمایه و پروپوزال‌ها":
    st.header("💰 مدل‌های تامین مالی و پروپوزال‌های شرکای استراتژیک")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### مدل تامین سرمایه")
        st.write(load_docx_text("مدل خاص تامین سرمایه برای اسکوکواکس 111.docx"))
    with c2:
        st.markdown("### پروپوزال شرکای استراتژیک و تعرفه")
        st.write(load_docx_text("پروپوزال جدید شرکای استراتژیک و تعرفه 2028.docx"))

# بخش ۶: برنامه اجرایی
elif menu_option == "📅 برنامه اجرایی ۱۲ روزه":
    st.header("📅 تقویم و برنامه اجرایی")
    st.markdown(load_docx_text("برنامه اجرایی ۱۲ روزه.docx"))

# فوتر
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 12px;'>SCOCOEX 2028 Intelligence Engine • Powered by Streamlit</p>", unsafe_allow_html=True)
