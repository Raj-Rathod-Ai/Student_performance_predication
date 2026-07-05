import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Student GPA Predictor",
    page_icon="🎓",
    layout="centered"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Top Header override for Deploy button visibility */
    header[data-testid="stHeader"] {
        background-color: rgba(9, 13, 22, 0.8) !important;
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    header[data-testid="stHeader"] * {
        color: #f8fafc !important;
        fill: #f8fafc !important;
    }

    /* Dark glassmorphism background style */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        color: #f8fafc;
    }
    
    /* Center container */
    .main-container {
        background: rgba(17, 24, 39, 0.7);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Header style */
    .app-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Question styling */
    .question-box {
        font-size: 1.35rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1.2rem;
        border-left: 5px solid #6366f1;
        padding-left: 1rem;
        letter-spacing: -0.01em;
    }
    
    /* Input Styling Override */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: rgba(31, 41, 55, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div[data-baseweb="input"]:hover, div[data-baseweb="select"]:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.2) !important;
        background-color: rgba(31, 41, 55, 0.7) !important;
    }
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 16px rgba(99, 102, 241, 0.4) !important;
        background-color: rgba(31, 41, 55, 0.85) !important;
    }
    
    /* Input and Selectbox text color and background correction */
    input, .stNumberInput input, .stTextInput input {
        color: #f8fafc !important;
        background-color: transparent !important;
    }
    
    /* Make all nested divs inside input controls transparent to show the dark parent background */
    .stNumberInput div, .stTextInput div, .stSelectbox div {
        background-color: transparent !important;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"], .stNumberInput > div, .stSelectbox > div {
        background-color: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] div, div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }
    
    /* Labels and helper text */
    label, .stWidgetLabel, .stWidgetLabel p, .stWidgetLabel div {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    
    /* Dropdown list customization */
    ul[role="listbox"] {
        background-color: #1f2937 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    li[role="option"] {
        color: #f8fafc !important;
        background-color: #1f2937 !important;
        transition: background-color 0.2s ease !important;
    }
    
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
    }
    
    /* Custom buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
        color: #ffffff !important;
    }
    
    div.stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.4) !important;
    }
    
    /* Secondary Button (Reset) */
    div.stButton > button[key*="Reset"] {
        background: rgba(31, 41, 55, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #cbd5e1 !important;
        box-shadow: none !important;
    }
    
    div.stButton > button[key*="Reset"]:hover {
        background: rgba(31, 41, 55, 0.8) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Result card */
    .result-card {
        background: radial-gradient(circle at top left, rgba(79, 70, 229, 0.18), rgba(17, 24, 39, 0.85));
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 2.2rem;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Load Model and Scaler
@st.cache_resource
def load_assets():
    with open('knn_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

try:
    model, scaler = load_assets()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# Title
st.markdown("<h1 class='app-title'>🎓 Student GPA Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Interactive Q&A assessment to forecast academic achievement using KNN Regression</p>", unsafe_allow_html=True)

# GPA Definition Callout
st.info("💡 **What is GPA?**  \nThe full form of GPA is **Grade Point Average**. It is a standardized numerical score used by educational institutions to measure a student's overall academic performance over a specific term or semester. It is typically calculated on a 4.0 or 10.0 scale.")


# Session State for Question Navigation
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Questions Metadata
questions = [
    {
        "id": "StudyTimeWeekly",
        "question": "How many hours per week does the student spend studying?",
        "helper": "Enter a value between 0 and 20 hours.",
        "type": "numeric",
        "min": 0.0,
        "max": 20.0,
        "default": 10.0,
        "step": 0.5
    },
    {
        "id": "Absences",
        "question": "How many school absences does the student have in the semester?",
        "helper": "Enter a number between 0 and 30 days.",
        "type": "numeric",
        "min": 0,
        "max": 30,
        "default": 2,
        "step": 1
    },
    {
        "id": "Tutoring",
        "question": "Does the student receive regular tutoring support?",
        "type": "choice",
        "options": ["No", "Yes"],
        "values": [0, 1]
    },
    {
        "id": "ParentalSupport",
        "question": "What is the level of parental involvement and support?",
        "type": "choice",
        "options": ["None / Very Low", "Low", "Medium", "High", "Very High"],
        "values": [0, 1, 2, 3, 4]
    },
    {
        "id": "Extracurricular",
        "question": "Does the student participate in extracurricular activities?",
        "type": "choice",
        "options": ["No", "Yes"],
        "values": [0, 1]
    },
    {
        "id": "Sports",
        "question": "Is the student involved in school or club sports?",
        "type": "choice",
        "options": ["No", "Yes"],
        "values": [0, 1]
    },
    {
        "id": "Music",
        "question": "Does the student participate in music activities?",
        "type": "choice",
        "options": ["No", "Yes"],
        "values": [0, 1]
    },
    {
        "id": "GradeClass",
        "question": "What is the student's Grade Class category?",
        "helper": "0.0 corresponds to highest classification, 4.0 to lowest classification.",
        "type": "choice",
        "options": [
            "Class 0 (A Grade Class / Excellent)",
            "Class 1 (B Grade Class / Good)",
            "Class 2 (C Grade Class / Average)",
            "Class 3 (D Grade Class / Below Average)",
            "Class 4 (F Grade Class / Needs Improvement)"
        ],
        "values": [0.0, 1.0, 2.0, 3.0, 4.0]
    }
]

total_steps = len(questions)

# Display Form inside a styled container
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

if st.session_state.step < total_steps:
    current_q = questions[st.session_state.step]
    
    # Progress Bar
    st.progress(st.session_state.step / total_steps)
    st.write(f"**Question {st.session_state.step + 1} of {total_steps}**")
    
    st.markdown(f"<div class='question-box'>{current_q['question']}</div>", unsafe_allow_html=True)
    
    # Input field based on question type
    if current_q["type"] == "numeric":
        val = st.number_input(
            label=current_q["helper"],
            min_value=current_q["min"],
            max_value=current_q["max"],
            value=st.session_state.answers.get(current_q["id"], current_q["default"]),
            step=current_q["step"],
            key=f"input_{current_q['id']}"
        )
        st.session_state.answers[current_q["id"]] = val
    elif current_q["type"] == "choice":
        default_idx = 0
        if current_q["id"] in st.session_state.answers:
            saved_val = st.session_state.answers[current_q["id"]]
            if saved_val in current_q["values"]:
                default_idx = current_q["values"].index(saved_val)
                
        choice = st.selectbox(
            label=current_q.get("helper", "Select one option:"),
            options=current_q["options"],
            index=default_idx,
            key=f"input_{current_q['id']}"
        )
        # Store corresponding value
        st.session_state.answers[current_q["id"]] = current_q["values"][current_q["options"].index(choice)]

    # Navigation Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.session_state.step > 0:
            if st.button("⬅️ Previous"):
                st.session_state.step -= 1
                st.rerun()
    with col2:
        button_label = "Finish & Predict 🎯" if st.session_state.step == total_steps - 1 else "Next ➡️"
        if st.button(button_label):
            st.session_state.step += 1
            st.rerun()

else:
    # Prediction Screen
    st.markdown("### 🎉 Review & GPA Prediction")
    
    # Show summary of answers in an expander
    with st.expander("🔍 Review Student Profile"):
        for q in questions:
            ans_val = st.session_state.answers.get(q["id"])
            if q["type"] == "choice":
                ans_lbl = q["options"][q["values"].index(ans_val)]
            else:
                ans_lbl = f"{ans_val} hours" if q["id"] == "StudyTimeWeekly" else f"{ans_val} days"
            st.write(f"**{q['question']}**: {ans_lbl}")

    # Prepare input for prediction
    # Scaler feature names: ['StudyTimeWeekly' 'Absences' 'Tutoring' 'ParentalSupport' 'Extracurricular' 'Sports' 'Music' 'GradeClass']
    features_ordered = ['StudyTimeWeekly', 'Absences', 'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 'GradeClass']
    input_values = [st.session_state.answers[feat] for feat in features_ordered]
    
    # Scale and Predict
    input_df = pd.DataFrame([input_values], columns=features_ordered)
    try:
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]
        
        # Display GPA Card showing both 4.0 and 10.0 scales
        predicted_gpa_4 = max(0.0, min(4.0, float(prediction)))
        predicted_gpa_10 = predicted_gpa_4 * 2.5
        
        st.markdown(f"""
        <div class="result-card">
            <h2 style="color: #818cf8; margin-bottom: 1.5rem;">Predicted Student GPA</h2>
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div>
                    <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{predicted_gpa_4:.2f}</h1>
                    <p style="color: #94a3b8; font-size: 1rem; margin-top: 0.2rem; margin-bottom: 0;">4.0 Scale</p>
                </div>
                <div style="border-left: 1px solid rgba(255, 255, 255, 0.15); height: 80px;"></div>
                <div>
                    <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(to right, #fb7185, #f43f5e); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{predicted_gpa_10:.2f}</h1>
                    <p style="color: #94a3b8; font-size: 1rem; margin-top: 0.2rem; margin-bottom: 0;">10.0 Scale</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # What-if Optimization / Scenario Analysis
        st.markdown("### 🔍 What-If Optimization Analysis")
        study_time = st.session_state.answers['StudyTimeWeekly']
        absences = st.session_state.answers['Absences']
        
        col_opt1, col_opt2 = st.columns(2)
        
        # 1. Absence Optimization
        with col_opt1:
            if absences > 0:
                opt_abs_vals = input_values.copy()
                opt_abs_vals[features_ordered.index('Absences')] = 0
                opt_abs_df = pd.DataFrame([opt_abs_vals], columns=features_ordered)
                opt_abs_pred = model.predict(scaler.transform(opt_abs_df))[0]
                opt_abs_gpa = max(0.0, min(4.0, float(opt_abs_pred)))
                gpa_diff = opt_abs_gpa - predicted_gpa_4
                
                if gpa_diff > 0.01:
                    st.metric(
                        label="GPA with 0 Absences",
                        value=f"{opt_abs_gpa:.2f}",
                        delta=f"+{gpa_diff:.2f} increase",
                        delta_color="normal"
                    )
                else:
                    st.write("📉 *Absences are already low, minimizing them has negligible impact.*")
            else:
                st.write("🎉 **Perfect Attendance!** (0 Absences)")
                
        # 2. Study Time Optimization
        with col_opt2:
            if study_time < 15.0:
                opt_study_vals = input_values.copy()
                opt_study_vals[features_ordered.index('StudyTimeWeekly')] = 15.0
                opt_study_df = pd.DataFrame([opt_study_vals], columns=features_ordered)
                opt_study_pred = model.predict(scaler.transform(opt_study_df))[0]
                opt_study_gpa = max(0.0, min(4.0, float(opt_study_pred)))
                study_gpa_diff = opt_study_gpa - predicted_gpa_4
                
                if study_gpa_diff > 0.01:
                    st.metric(
                        label="GPA with 15h Study/Week",
                        value=f"{opt_study_gpa:.2f}",
                        delta=f"+{study_gpa_diff:.2f} increase",
                        delta_color="normal"
                    )
                else:
                    st.write("📉 *Study hours are already high, increasing has negligible impact.*")
            else:
                st.write("📚 **Highly Dedicated!** (>15h study time/week)")
        
        # Actionable insights
        st.markdown("### 📈 Tailored Recommendations")
        tutoring = st.session_state.answers['Tutoring']
        
        recs = []
        if study_time < 10:
            recs.append("📚 **Increase Study Time**: Encourage targeting at least 10-15 hours of weekly study time to improve retention.")
        if absences > 4:
            recs.append("🏫 **Improve Attendance**: Absences strongly impact grades. Try to keep absences under 3 days per semester.")
        if tutoring == 0:
            recs.append("🤝 **Tutoring Support**: Seeking external tutoring or peer study groups can provide valuable guidance.")
            
        if recs:
            for rec in recs:
                st.info(rec)
        else:
            st.success("🌟 The student has excellent academic habits! Keep maintaining this structure to achieve peak performance.")

    except Exception as e:
        st.error(f"Error during GPA calculation: {e}")

    if st.button("🔄 Reset Questionnaire"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
