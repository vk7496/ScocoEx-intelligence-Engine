import streamlit as st
import pandas as pd

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

# هدر اصلی سامانه منطبق بر لوگو و پوستر SCOCOEX Global Week 2028
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
        <p style="color: #64748b; font-size: 12px; margin: 5px 0 0 0;">
            انسانیت &nbsp;•&nbsp; صلح &nbsp;•&nbsp; اقتصاد جهانی (تمرکز ویژه: ازبکستان، بلغارستان، عمان)
        </p>
    </div>
""", unsafe_allow_html=True)

# سایدبار مدیریت پنل‌ها
st.sidebar.markdown("### 🎛️ انتخاب سازمان / بخش")
tenant = st.sidebar.selectbox(
    "انتخاب هلدینگ یا پایگاه داده:",
    [
        "گروه صنعتی گلرنگ",
        "صنایع ملی مس ایران (NICICO)",
        "بنیاد مستضعفان",
        "🌐 شبکه جهانی و محورهای اجلاس (عمان، ازبکستان، بلغارستان)",
        "📄 ترجمه اسناد و فایل‌ها (English Translation)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 وضعیت سامانه 2028")
st.sidebar.success("پلتفرم هوشمند دوزبانه (صوتی و متنی) فعال است. آماده ارائه به مدیران و مهمانان بین‌المللی.")

# تابع تولید پاسخ هوشمند دو زبانه (فارسی و انگلیسی)
def generate_ai_response(prompt, current_tenant, lang):
    prompt_lower = prompt.lower()
    if lang == "English":
        if "oman" in prompt_lower or "gcc" in prompt_lower or "region" in prompt_lower:
            return f"Based on SCOCOEX Global Week 2028 data for {current_tenant}, Oman serves as the strategic GCC gateway and peace hub, reducing logistics and custom tariffs by up to 35%."
        elif "uzbekistan" in prompt_lower or "humanity" in prompt_lower:
            return f"The 'Humanity' pillar focusing on Uzbekistan within {current_tenant} emphasizes cultural ties, Eurasian trade corridors, and cross-border tech exchange."
        elif "bulgaria" in prompt_lower or "economy" in prompt_lower:
            return f"Bulgaria acts as our key European bridge, driving 'Global Economy' indicators and streamlining B2B partnerships for {current_tenant}."
        elif "invest" in prompt_lower or "finance" in prompt_lower or "capital" in prompt_lower:
            return f"Under {current_tenant}'s strategic framework, capital attraction is optimized via sovereign wealth funds and international joint ventures (JVs)."
        else:
            return f"SCOCOEX 2028 AI Advisor analyzed your query for '{current_tenant}': Your input was thoroughly evaluated. Recommended focus: High-level economic diplomacy and targeted summit deal-rooms."
    else:
        if "عمان" in prompt or "gcc" in prompt_lower or "منطقه" in prompt:
            return f"بر اساس چارچوب‌های SCOCOEX Global Week 2028 در بخش {current_tenant}، عمان به عنوان هاب صلح و دروازه اقتصادی خلیج فارس نقش کلیدی در کاهش تعرفه‌ها و توسعه سرمایه‌گذاری مشترک دارد."
        elif "ازبکستان" in prompt or "humanity" in prompt_lower:
            return f"محور «انسانیت» و همکاری‌های منطقه‌ای با ازبکستان در {current_tenant} بر پایه پیوندهای فرهنگی، توسعه کریدورهای تجاری اوراسیا و تبادل فناوری استوار است."
        elif "بلغارستان" in prompt or "bulgaria" in prompt_lower or "اقتصاد" in prompt:
            return f"بلغارستان به عنوان پل ارتباطی تجاری در قلب اروپا، نقش ویژه‌ای در ارتقای شاخص‌های «اقتصاد جهانی» و تسهیل مبادلات B2B برای {current_tenant} ایفا می‌کند."
        elif "سرمایه" in prompt or "فایننس" in prompt or "جذب" in prompt:
            return f"در رویکرد استراتژیک {current_tenant}، مدل‌های جذب سرمایه از طریق صندوق‌های ثروت ملی و کنسرسیوم‌های بین‌المللی اجلاس 2028 پیاده‌سازی می‌شوند."
        else:
            return f"تحلیلگر هوشمند SCOCOEX 2028 برای '{current_tenant}' بررسی کرد: پرسش شما («{prompt}») ارزیابی شد. پیشنهاد کلیدی تمرکز بر دیپلماسی اقتصادی و نشست‌های تخصصی اجلاس است."

# منطق نمایش صفحات
if tenant not in ["🌐 شبکه جهانی و محورهای اجلاس (عمان، ازبکستان، بلغارستان)", "📄 ترجمه اسناد و فایل‌ها (English Translation)"]:
    
    if tenant == "گروه صنعتی گلرنگ":
        st.markdown("## گروه صنعتی گلرنگ: اکوسیستم تجاری و مقیاس جهانی (چشم‌انداز 2028)")
        st.markdown("هدف اصلی: عبور از سقف بازار داخلی، راه‌اندازی هاب‌های توزیع و سرمایه‌گذاری مشترک (JV) در بازارهای کلیدی منطقه.")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("کریدورهای فعال", "۴ هاب منطقه‌ای", "عمان و GCC")
        with col2: st.metric("مدل توسعه بازار", "Export → JV", "پایدار")
        with col3: st.metric("هدف مقیاس", "Fortune Global 500", "بین‌المللی")

        chart_data = pd.DataFrame({
            'کریدور': ["عمان و GCC", "آسیای مرکزی", "ترکیه", "شرق آفریقا"],
            'پتانسیل درآمدی (همت)': [1200, 1100, 900, 800]
        }).set_index('کریدور')
        st.bar_chart(chart_data, color="#3b82f6")

    elif tenant == "صنایع ملی مس ایران (NICICO)":
        st.markdown("## صنایع ملی مس ایران (NICICO): اتاق‌های تخصصی مس در اجلاس 2028")
        st.markdown("مدیریت ۴ اتاق کلیدی: مواد اولیه، فناوری و AI، خریداران بلندمدت Offtake، و کنسرسیوم‌های سرمایه‌گذاری.")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("اتاق‌های تخصصی", "۴ اتاق کلیدی", "فعال")
        with col2: st.metric("میزهای مذاکره B2B", "۱۲ میز تخصصی", "هدفمند")
        with col3: st.metric("پنجره بازار", "سال ۲۰۲۸", "برقی‌سازی و AI")

        chart_data = pd.DataFrame({
            'اتاق تخصصی': ["Offtake بلندمدت", "سرمایه‌گذاری و کنسرسیوم", "مواد اولیه و ماشین‌آلات", "فناوری و AI معدن"],
            'ارزش (میلیارد دلار)': [4.2, 3.5, 2.5, 1.8]
        }).set_index('اتاق تخصصی')
        st.bar_chart(chart_data, color="#10b981")

    elif tenant == "بنیاد مستضعفان":
        st.markdown("## بنیاد مستضعفان: پورتفوی هلدینگ و ۵ موتور توسعه‌ای")
        st.markdown("رویکرد Profit + Impact + Globalization؛ اتصال دارایی‌های موجود در ۳۰ شرکت کلیدی به بازارهای بین‌المللی.")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("شرکت‌های پورتفو", "۳۰ شرکت", "ارزیابی‌شده")
        with col2: st.metric("شرکت‌های خارجی هدف", "۳۰۰ شرکت", "دعوت‌شده")
        with col3: st.metric("موتورهای توسعه‌ای", "۵ موتور", "فعال")

        chart_data = pd.DataFrame({
            'مرحله معامله': ["شرکت‌های هدف", "ارزیابی‌شده", "مذاکرات فعال", "فرصت‌های JV نهایی"],
            'تعداد': [300, 150, 50, 12]
        }).set_index('مرحله معامله')
        st.bar_chart(chart_data, color="#6366f1")

    st.markdown("---")
    
    # -------------------------------------------------------------
    # بخش پرسش و پاسخ هوشمند دوزبانه (متن + ویس صوتی)
    # -------------------------------------------------------------
    st.markdown("### 💬 اتاق پرسش و پاسخ هوشمند و صوتی (Bilingual Executive AI & Voice Hub)")
    
    # انتخاب زبان پاسخ‌دهی هوش مصنوعی
    chat_lang = st.radio(
        "🌐 انتخاب زبان پاسخ‌دهی سامانه (Response Language):",
        ["فارسی", "English"],
        horizontal=True
    )
    
    st.markdown("می‌توانید سوال خود را تایپ کنید **یا** از طریق میکروفون پایین پیام صوتی ثبت کنید:")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # نمایش تاریخچه پیام‌ها
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ابزار ضبط صدا (Voice Recorder)
    audio_value = st.audio_input("🎙️ ارسال پیام صوتی (Record Voice Message)")
    
    user_query = None
    if audio_value:
        st.audio(audio_value)
        if chat_lang == "English":
            user_query = "[Voice Message Received from Foreign Guest/Investor]"
        else:
            user_query = "[پیام صوتی ارسالی از سوی مدیر / مهمان]"

    # ورودی متنی چت
    if text_input := st.chat_input("سوال یا استعلام خود را بنویسید..."):
        user_query = text_input

    # پردازش و پاسخگویی
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        ai_reply = generate_ai_response(user_query, tenant, chat_lang)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

elif tenant == "🌐 شبکه جهانی و محورهای اجلاس (عمان، ازبکستان، بلغارستان)":
    st.markdown("## 🌐 شبکه جهانی و محورهای کلیدی SCOCOEX Global Week 2028")
    st.markdown("پایگاه داده متصل به بیش از ۱۴۰ شرکت غول‌پیکر جهانی، صندوق‌های حاکمیتی و هاب‌های ویژه اجلاس (عمان، بلغارستان، ازبکستان) برای مذاکرات مستقیم B2B.")
    
    categories = {
        "🇦🇪 🇴🇲 هاب‌های کلیدی منطقه‌ای و صندوق‌های ثروت ملی (SWF)": [
            ("OIA (عمان - صلح)", "https://oia.gov.om"), ("Mubadala (امارات)", "https://www.mubadala.com"),
            ("ADQ (ابوظبی)", "https://www.adq.ae"), ("PIF (عربستان)", "https://www.pif.gov.sa"),
            ("QIA (قطر)", "https://www.qia.qa"), ("KIA (کویت)", "https://www.kia.gov.kw"),
            ("Mumtalakat (بحرین)", "https://www.mumtalakat.bh"), ("Temasek (سنگاپور)", "https://www.temasek.com.sg")
        ],
        "🇧🇬 🇺🇿 شرکای استراتژیک (بلغارستان و ازبکستان - اقتصاد و انسانیت)": [
            ("Bulgarian Chamber of Commerce", "https://www.bcci.bg"), ("Invest Bulgaria Agency", "https://www.investbg.government.bg"),
            ("Uzbekistan Ministry of Investment", "https://mift.uz"), ("Navoi Mining & Metallurgical Combinat", "https://www.ngmk.uz"),
            ("Uzbekistan Chamber of Commerce", "https://chamber.uz"), ("Sofia Tech Park", "https://sofiatech.bg")
        ],
        "انرژی، نفت، گاز و پتروشیمی": [
            ("Aramco", "https://www.aramco.com"), ("ADNOC", "https://www.adnoc.ae"),
            ("OQ (عمان)", "https://oq.com"), ("QatarEnergy", "https://www.qatarenergy.qa"),
            ("ACWA Power", "https://www.acwapower.com"), ("Masdar", "masdar.ae")
        ],
        "فناوری و هوش مصنوعی پیشران": [
            ("Microsoft", "https://www.microsoft.com"), ("Google", "https://www.google.com"),
            ("NVIDIA", "https://www.nvidia.com"), ("OpenAI", "openai.com"),
            ("Anthropic", "https://www.anthropic.com"), ("Lenovo", "https://www.lenovo.com")
        ],
        "بانک‌ها و مؤسسات مالی بزرگ": [
            ("BlackRock", "https://www.blackrock.com"), ("HSBC", "https://www.hsbc.com"),
            ("JPMorgan Chase", "https://www.jpmorganchase.com"), ("First Abu Dhabi Bank (FAB)", "https://www.bankfab.com"),
            ("Bank Muscat", "https://www.bankmuscat.com"), ("QNB", "https://www.qnb.com")
        ]
    }

    for cat_name, comps in categories.items():
        st.markdown(f"### 🔹 {cat_name}")
        cols = st.columns(4)
        for idx, (name, url) in enumerate(comps):
            with cols[idx % 4]:
                st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #1e293b; padding: 10px 14px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
                        <a href="{url}" target="_blank" style="color: #60a5fa; text-decoration: none; font-size: 12px; font-weight: 600; display: block;">
                            {name} ↗
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("")

else:
    # بخش مرکز ترجمه اسناد و فایل‌ها به انگلیسی
    st.markdown("## 📄 مرکز اسناد و ترجمه رسمی (SCOCOEX 2028 English Documents)")
    st.markdown("مخزن فایل‌ها، پروپوزال‌ها و توافق‌نامه‌های تجاری ترجمه‌شده به زبان انگلیسی جهت ارائه به سرمایه‌گذاران و شرکت‌های بین‌المللی در اجلاس 2028.")

    translated_files = [
        {"title": "SCOCOEX Global Week 2028 Master Executive Pitch Deck", "type": "PDF Presentation", "lang": "English (US)", "status": "Ready for Presentation"},
        {"title": "Oman, Bulgaria & Uzbekistan Tri-Lateral Framework Agreement", "type": "Legal Contract", "lang": "English / Multilingual", "status": "Verified"},
        {"title": "NICICO 2028 Copper & AI Market Analysis", "type": "Technical Report", "lang": "English", "status": "Ready"},
        {"title": "Bonyad International Asset Portfolio Overview", "type": "Corporate Profile", "lang": "English", "status": "Ready"},
        {"title": "Cross-Border Trade & Customs Compliance Guide (GCC & Eurasia)", "type": "Regulatory Document", "lang": "English", "status": "Verified"}
    ]

    for file in translated_files:
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b; padding: 16px 20px; border-radius: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: #60a5fa; margin: 0 0 5px 0; font-size: 15px;">📁 {file['title']}</h4>
                    <p style="color: #94a3b8; margin: 0; font-size: 12px;">نوع سند: <b>{file['type']}</b> | زبان: <b>{file['lang']}</b></p>
                </div>
                <div>
                    <span style="background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); padding: 5px 12px; border-radius: 8px; font-size: 11px; font-weight: 600;">
                        {file['status']}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
