import streamlit as st
from streamlit_ace import st_ace
from utils.code_executor import CodeExecutor
from utils.progress_tracker import ProgressTracker
import time

# Page configuration
st.set_page_config(page_title="ملعب الكود", page_icon="🎮", layout="wide")

# Initialize utilities
if 'code_executor' not in st.session_state:
    st.session_state.code_executor = CodeExecutor()

if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()

if 'code_history' not in st.session_state:
    st.session_state.code_history = []

st.title("🎮 ملعب الكود")
st.write("مساحة حرة لتجربة وكتابة أكواد بايثون")

# Sidebar with examples and history
st.sidebar.title("🔧 أدوات مساعدة")

# Code templates
st.sidebar.subheader("📝 قوالب جاهزة")
templates = {
    "مرحباً بالعالم": "print('مرحباً بالعالم!')",
    "متغيرات أساسية": "name = 'أحمد'\nage = 25\nprint(f'اسمي {name} وعمري {age} سنة')",
    "حلقة for": "for i in range(1, 6):\n    print(f'الرقم: {i}')",
    "حلقة while": "count = 1\nwhile count <= 5:\n    print(count)\n    count += 1",
    "قائمة": "fruits = ['تفاح', 'موز', 'برتقال']\nfor fruit in fruits:\n    print(fruit)",
    "دالة بسيطة": "def greet(name):\n    return f'مرحباً {name}!'\n\nresult = greet('سارة')\nprint(result)",
    "قاموس": "student = {'name': 'أحمد', 'age': 20, 'grade': 85}\nprint(f\"الطالب: {student['name']}\")\nprint(f\"العمر: {student['age']}\")",
    "جملة شرطية": "number = 15\nif number > 10:\n    print('العدد أكبر من 10')\nelse:\n    print('العدد أصغر من أو يساوي 10')"
}

selected_template = st.sidebar.selectbox(
    "اختر قالب:",
    ["اختر قالب..."] + list(templates.keys())
)

if selected_template != "اختر قالب...":
    if st.sidebar.button("📋 استخدام القالب"):
        st.session_state.playground_code = templates[selected_template]
        st.rerun()

# Code history
st.sidebar.subheader("📚 تاريخ الأكواد")
if st.session_state.code_history:
    history_options = [f"كود {i+1}" for i in range(len(st.session_state.code_history))]
    selected_history = st.sidebar.selectbox("الأكواد السابقة:", ["اختر كود..."] + history_options)
    
    if selected_history != "اختر كود...":
        history_index = history_options.index(selected_history)
        if st.sidebar.button("📥 استرجاع الكود"):
            st.session_state.playground_code = st.session_state.code_history[history_index]['code']
            st.rerun()
        
        # Preview of the selected code
        st.sidebar.code(st.session_state.code_history[history_index]['code'][:100] + "..." if len(st.session_state.code_history[history_index]['code']) > 100 else st.session_state.code_history[history_index]['code'])

else:
    st.sidebar.info("لا توجد أكواد محفوظة بعد")

# Clear history
if st.session_state.code_history and st.sidebar.button("🗑️ مسح التاريخ"):
    st.session_state.code_history = []
    st.rerun()

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Code editor
    st.subheader("💻 محرر الكود")
    
    # Get initial code
    initial_code = st.session_state.get('playground_code', 
        "# مرحباً بك في ملعب الكود!\n# اكتب كودك هنا وجربه\n\nprint('مرحباً بك في عالم بايثون!')")
    
    user_code = st_ace(
        value=initial_code,
        language='python',
        theme='github',
        font_size=16,
        tab_size=4,
        wrap=True,
        height=400,
        key="playground_editor",
        auto_update=True
    )
    
    # Update session state
    st.session_state.playground_code = user_code
    
    # Control buttons
    col_run, col_save, col_clear, col_share = st.columns([2, 1, 1, 1])
    
    with col_run:
        if st.button("▶️ تشغيل الكود", type="primary", use_container_width=True):
            if user_code.strip():
                # Validate code
                is_valid, validation_msg = st.session_state.code_executor.validate_code(user_code)
                
                if is_valid:
                    with st.spinner("جاري تشغيل الكود..."):
                        result = st.session_state.code_executor.execute_code(user_code)
                        st.session_state.progress_tracker.increment_code_runs()
                    
                    # Display results
                    if result['success']:
                        st.success("✅ تم تشغيل الكود بنجاح!")
                        
                        if result['output']:
                            st.subheader("📤 المخرجات:")
                            st.code(result['output'], language='text')
                        else:
                            st.info("الكود تم تنفيذه بنجاح ولكن لا توجد مخرجات للعرض")
                        
                        # Execution info
                        col_time, col_lines = st.columns(2)
                        with col_time:
                            st.metric("وقت التنفيذ", f"{result['execution_time']:.3f} ثانية")
                        with col_lines:
                            lines_count = len(user_code.split('\n'))
                            st.metric("عدد الأسطر", lines_count)
                    else:
                        st.error("❌ حدث خطأ أثناء تشغيل الكود:")
                        st.code(result['error'], language='text')
                        
                        # Helpful tips based on error
                        if "SyntaxError" in result['error']:
                            st.info("💡 نصيحة: تحقق من الأقواس والفواصل وعلامات الاقتباس")
                        elif "NameError" in result['error']:
                            st.info("💡 نصيحة: تأكد من تعريف جميع المتغيرات قبل استخدامها")
                        elif "IndentationError" in result['error']:
                            st.info("💡 نصيحة: تحقق من المسافات في بداية الأسطر")
                else:
                    st.error(f"❌ {validation_msg}")
            else:
                st.warning("⚠️ الرجاء كتابة بعض الكود أولاً")
    
    with col_save:
        if st.button("💾 حفظ", use_container_width=True):
            if user_code.strip():
                # Save to history
                code_entry = {
                    'code': user_code,
                    'timestamp': time.time(),
                    'lines': len(user_code.split('\n'))
                }
                st.session_state.code_history.append(code_entry)
                # Keep only last 10 codes
                if len(st.session_state.code_history) > 10:
                    st.session_state.code_history = st.session_state.code_history[-10:]
                st.success("تم حفظ الكود!")
            else:
                st.warning("لا يوجد كود للحفظ")
    
    with col_clear:
        if st.button("🗑️ مسح", use_container_width=True):
            st.session_state.playground_code = "# اكتب كودك هنا\n\n"
            st.rerun()
    
    with col_share:
        if st.button("📤 مشاركة", use_container_width=True):
            if user_code.strip():
                st.text_area(
                    "انسخ الكود للمشاركة:",
                    user_code,
                    height=100,
                    key="share_code"
                )
            else:
                st.warning("لا يوجد كود للمشاركة")

with col2:
    # Statistics and tips
    st.subheader("📊 إحصائيات")
    
    # User statistics
    stats = st.session_state.progress_tracker.get_progress_stats()
    st.metric("عدد مرات التشغيل", stats['total_code_runs'])
    st.metric("الأكواد المحفوظة", len(st.session_state.code_history))
    
    # Current code info
    if user_code:
        lines = len(user_code.split('\n'))
        chars = len(user_code)
        st.metric("أسطر الكود الحالي", lines)
        st.metric("عدد الأحرف", chars)
    
    # Tips section
    st.subheader("💡 نصائح")
    tips = [
        "استخدم print() لعرض النتائج",
        "تأكد من المسافات الصحيحة",
        "اختبر الكود قطعة قطعة",
        "استخدم التعليقات لتوضيح الكود",
        "جرب القوالب الجاهزة للتعلم",
        "احفظ الأكواد المفيدة للرجوع إليها"
    ]
    
    for tip in tips:
        st.write(f"• {tip}")
    
    # Quick references
    st.subheader("📖 مراجع سريعة")
    
    with st.expander("العمليات الأساسية"):
        st.code("""
# الطباعة
print("مرحباً")

# المتغيرات
name = "أحمد"
age = 25

# العمليات الحسابية
result = 10 + 5
        """)
    
    with st.expander("الحلقات"):
        st.code("""
# حلقة for
for i in range(5):
    print(i)

# حلقة while
count = 0
while count < 5:
    print(count)
    count += 1
        """)
    
    with st.expander("الشروط"):
        st.code("""
# جملة شرطية
if age >= 18:
    print("بالغ")
else:
    print("قاصر")
        """)

# Footer navigation
st.markdown("---")
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("🏠 الصفحة الرئيسية"):
        st.switch_page("app.py")

with col_nav2:
    if st.button("📚 الدروس"):
        st.switch_page("pages/1_الدروس.py")

with col_nav3:
    if st.button("💪 التمارين"):
        st.switch_page("pages/3_التمارين.py")
