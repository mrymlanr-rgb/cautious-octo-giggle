import streamlit as st
import json
import os
from utils.progress_tracker import ProgressTracker

# Configure page
st.set_page_config(
    page_title="منصة تعلم بايثون",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize progress tracker
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()

# Main page content
st.title("🐍 منصة تعلم بايثون للمبتدئين")
st.markdown("### مرحباً بك في رحلة تعلم لغة البرمجة بايثون!")

# Welcome section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## ماذا ستتعلم؟
    
    📚 **الأساسيات**: المتغيرات، أنواع البيانات، والعمليات الأساسية
    
    🔄 **التكرار والشروط**: الحلقات والجمل الشرطية
    
    🔧 **الدوال**: كيفية كتابة وإستخدام الدوال
    
    📊 **هياكل البيانات**: القوائم، القواميس، والمجموعات
    
    🎯 **المشاريع العملية**: تطبيق ما تعلمته في مشاريع حقيقية
    """)

with col2:
    st.markdown("### 📊 إحصائياتك")
    progress = st.session_state.progress_tracker.get_overall_progress()
    st.metric("نسبة الإنجاز", f"{progress:.1f}%")
    
    completed_lessons = st.session_state.progress_tracker.get_completed_lessons_count()
    st.metric("الدروس المكتملة", completed_lessons)
    
    st.markdown("---")
    st.markdown("### 🚀 ابدأ الآن")
    if st.button("الذهاب إلى الدروس", type="primary"):
        st.switch_page("pages/1_الدروس.py")

# Features section
st.markdown("---")
st.markdown("## ✨ مميزات المنصة")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 💻 محرر كود تفاعلي
    اكتب وجرب الكود مباشرة في المتصفح مع تنفيذ فوري للنتائج
    """)

with col2:
    st.markdown("""
    ### 📖 دروس تدريجية
    تعلم خطوة بخطوة من البداية حتى الاحتراف
    """)

with col3:
    st.markdown("""
    ### 🎯 تمارين عملية
    طبق ما تعلمته من خلال تمارين متنوعة ومفيدة
    """)

# Quick start section
st.markdown("---")
st.markdown("## 🏃‍♂️ البدء السريع")

quick_start_col1, quick_start_col2 = st.columns(2)

with quick_start_col1:
    st.markdown("""
    ### للمبتدئين الجدد:
    1. ابدأ بصفحة **الدروس** لتعلم الأساسيات
    2. جرب **ملعب الكود** لتجربة ما تعلمته
    3. حل **التمارين** لتطبيق المعرفة
    4. تابع **التقدم** لمعرفة مستواك
    """)

with quick_start_col2:
    st.markdown("""
    ### نصائح مهمة:
    - خذ وقتك في فهم كل مفهوم
    - جرب تعديل الأمثلة المعطاة
    - لا تتردد في العودة للدروس السابقة
    - تمرن كثيراً لترسيخ المعلومات
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>تم تطوير هذه المنصة لتعليم بايثون بطريقة تفاعلية وممتعة</p>
    <p>🐍 Happy Coding! 🐍</p>
</div>
""", unsafe_allow_html=True)
