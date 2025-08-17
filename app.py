# app.py
import streamlit as st
import time
import pandas as pd
import json
from datetime import datetime, timedelta
from streamlit.components.v1 import html

# Import project components
from config.syllabus import GATE_CSE_SYLLABUS
from core.orchestrator import generate_test_concurrently, generate_full_mock_test
from core.llm_client import check_and_pull_model
from components.analytics import initialize_db, save_test_result, get_test_history
from components.vector_store import search_questions

# --- Page & State Management ---
st.set_page_config(page_title="GATE AI Exam System", layout="wide")

# --- UI & Styling Functions ---
def load_css(file_name):
    """Loads a CSS file and injects it into the Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found. Ensure 'styles.css' is in the root directory.")

# --- NEW: JavaScript Timer Component ---
def render_javascript_timer(seconds_left):
    """Renders a client-side countdown timer in the browser."""
    timer_js = f"""
    <script>
    var timeLeft = {seconds_left};
    var timerId = setInterval(countdown, 1000);

    function countdown() {{
      if (timeLeft <= 0) {{
        clearTimeout(timerId);
        // The Python logic will handle the timeout on the next interaction.
        document.getElementById("time").innerHTML = "00:00";
      }} else {{
        var minutes = Math.floor(timeLeft / 60).toString().padStart(2, '0');
        var seconds = (timeLeft % 60).toString().padStart(2, '0');
        document.getElementById("time").innerHTML = minutes + ":" + seconds;
        timeLeft--;
      }}
    }}
    </script>
    """
    html(timer_js, height=0, width=0)


# --- NEW: Scoring Function ---
def calculate_score():
    """Calculates the final score based on user answers."""
    score = 0
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.user_answers.get(i)
        correct_ans_list = json.loads(q.get('answer', '[]')) if isinstance(q.get('answer'), str) else q.get('answer', [])
        
        is_correct = False
        # Normalize user answer for comparison
        user_ans_list = []
        if user_ans is not None:
            user_ans_list = user_ans if isinstance(user_ans, list) else [user_ans]

        if q.get('type') in ['MCQ', 'MSQ']:
            is_correct = sorted(user_ans_list) == sorted(correct_ans_list)
        elif q.get('type') == 'NAT':
            try:
                is_correct = user_ans is not None and abs(float(user_ans) - float(correct_ans_list[0])) < 1e-4
            except (ValueError, TypeError, IndexError):
                is_correct = False
        
        if is_correct:
            score += 1 # You can add custom marks here (e.g., +2 for MSQ)
    return score

# --- Callbacks for State Management ---
def start_test(duration_minutes):
    """Initializes test state and timer."""
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.start_time = datetime.now()
    st.session_state.end_time = st.session_state.start_time + timedelta(minutes=duration_minutes)
    st.session_state.exam_view = "test"

def show_results():
    """Calculates the real score and switches to the results page."""
    # FIX: Calls the new scoring function
    score = calculate_score()
    st.session_state.score = score
    save_test_result(st.session_state.test_topic, score, len(st.session_state.questions))
    st.session_state.exam_view = "results"

def reset_to_main_menu():
    """Clears all test-related state."""
    st.session_state.clear()
    st.session_state.page = "generate"
    st.rerun()

def initialize_session_state():
    """Runs the main initialization logic once per session."""
    if 'page' not in st.session_state:
        st.session_state.page = "generate"
    # FIX: Ensure one-time setup runs only once per session
    if 'app_initialized' not in st.session_state:
        with st.spinner("Initializing system..."):
            initialize_db()
            check_and_pull_model()
        st.session_state.app_initialized = True

# --- Main App ---
load_css("styles.css")
initialize_session_state()

st.title(" GATE AI Exam System")
st.markdown("---")

# --- Persistent Tab Structure ---
tab_new_test, tab_live_exam, tab_history, tab_search = st.tabs(["🎯 New Test", "📝 Live Exam", "📊 Test History", "🔍 Search Questions"])

# --- Tab 1: Test Configuration ---
with tab_new_test:
    if st.session_state.get("test_in_progress"):
        st.warning("A test is in progress. Please complete it in the 'Live Exam' tab.")
    else:
        practice_tab, mock_tab = st.tabs(["Practice Test", "Full Mock Test"])
        with practice_tab:
            st.header("Configure Your Practice Test")
            col1, col2, col3 = st.columns(3)
            with col1: subject = st.selectbox("Subject", options=GATE_CSE_SYLLABUS.keys(), key="p_subj")
            with col2: topic = st.selectbox("Topic", options=GATE_CSE_SYLLABUS[subject], key="p_top")
            with col3: num_q = st.number_input("Questions", min_value=1, max_value=20, value=5, key="p_num")
            if st.button("Generate Practice Test", type="primary", key="p_btn"):
                st.session_state.test_topic = topic
                with st.spinner(f"Generating {num_q} questions..."):
                    qs = [q for q in generate_test_concurrently(topic, num_q) if q]
                if qs:
                    st.session_state.questions = qs
                    st.session_state.test_in_progress = True
                    st.session_state.exam_view = "instructions"
                    st.rerun()

        with mock_tab:
            st.header("Configure Full Syllabus Mock Test")
            num_q_mock = st.slider("Total Questions", 10, 65, 30, 5, key="m_num")
            if st.button("Generate Full Mock Test", type="primary", key="m_btn"):
                st.session_state.test_topic = "Full Syllabus Mock Test"
                with st.spinner(f"Generating a {num_q_mock}-question test..."):
                    qs = generate_full_mock_test(num_q_mock)
                if qs:
                    st.session_state.questions = qs
                    st.session_state.test_in_progress = True
                    st.session_state.exam_view = "instructions"
                    st.rerun()

# --- Tab 2: The Live Exam ---
with tab_live_exam:
    if not st.session_state.get("test_in_progress"):
        st.info("Please generate a test from the 'New Test' tab to begin.")
    else:
        # View 1: Instructions
        if st.session_state.exam_view == "instructions":
            st.title("Test Instructions")
            num_qs = len(st.session_state.questions)
            duration = num_qs * 1.5
            st.info(f"Topic: {st.session_state.test_topic} | Questions: {num_qs} | Time: {int(duration)} mins")
            agree = st.checkbox("I have read the instructions.")
            if st.button("Start Test", type="primary", disabled=not agree):
                start_test(duration)
                st.rerun()

        # View 2: The Live Test
        elif st.session_state.exam_view == "test":
            # FIX: Remove st_autorefresh and use JS timer
            remaining_time = st.session_state.end_time - datetime.now()
            if remaining_time.total_seconds() < 1:
                st.warning("Time's up! Submitting your test.")
                time.sleep(1)
                show_results()
                st.rerun()
            
            # Display Header with JS Timer
            st.markdown(f'<div class="exam-header"><div class="exam-title">{st.session_state.test_topic}</div><div class="timer">⏳ <span id="time"></span></div></div>', unsafe_allow_html=True)
            render_javascript_timer(int(remaining_time.total_seconds()))

            left_col, right_col = st.columns([3, 1])
            with right_col:
                with st.container(border=True):
                    st.subheader("Question Palette")
                    cols = st.columns(5)
                    for i in range(len(st.session_state.questions)):
                        with cols[i % 5]:
                            if st.button(f"{i+1}", key=f"pal_{i}"):
                                st.session_state.current_question = i
                                st.rerun()
                    st.markdown("---")
                    if st.button("Finish Test", type="primary", use_container_width=True, on_click=show_results):
                        st.rerun()

            with left_col:
                q_data = st.session_state.questions[st.session_state.current_question]
                with st.container(border=True, height=600):
                    st.subheader(f"Question {st.session_state.current_question + 1}")
                    st.markdown(q_data['question'])
                    st.markdown("---")
                    answer = None
                    key_prefix = f"q_{st.session_state.current_question}"
                    options = q_data.get('options', [])
                    if q_data['type'] == 'MCQ':
                        answer = st.radio("Options", options, key=f"{key_prefix}_mcq", label_visibility="collapsed")
                    elif q_data['type'] == 'MSQ':
                        selected = []
                        st.write("Select all correct options:")
                        for opt in options:
                            if st.checkbox(opt, key=f"{key_prefix}_{opt}"): selected.append(opt)
                        answer = selected
                    elif q_data['type'] == 'NAT':
                        answer = st.number_input("Your Answer", key=f"{key_prefix}_nat", value=None, format="%.2f")
                    
                    st.session_state.user_answers[st.session_state.current_question] = answer
                    
                    nav_cols = st.columns([1, 1, 5, 2])
                    if st.session_state.current_question > 0:
                        if nav_cols[0].button("Previous"): st.session_state.current_question -= 1; st.rerun()
                    if st.session_state.current_question < len(st.session_state.questions) - 1:
                        if nav_cols[1].button("Next"): st.session_state.current_question += 1; st.rerun()

        # View 3: Results
        elif st.session_state.exam_view == "results":
            st.title("Test Results")
            st.balloons()
            st.header(f"Final Score: {st.session_state.get('score', 0)}/{len(st.session_state.questions)}")
            st.markdown("---")
            
            for i, q in enumerate(st.session_state.questions):
                with st.expander(f"Question {i+1}: Review"):
                    user_ans = st.session_state.user_answers.get(i)
                    correct_ans_list = json.loads(q.get('answer', '[]')) if isinstance(q.get('answer'), str) else q.get('answer', [])
                    is_correct = False
                    user_ans_list = []
                    if user_ans is not None:
                        user_ans_list = user_ans if isinstance(user_ans, list) else [user_ans]

                    if q.get('type') in ['MCQ', 'MSQ']:
                        is_correct = sorted(user_ans_list) == sorted(correct_ans_list)
                    elif q.get('type') == 'NAT':
                        try:
                            is_correct = user_ans is not None and abs(float(user_ans) - float(correct_ans_list[0])) < 1e-4
                        except (ValueError, TypeError, IndexError):
                            is_correct = False
                    
                    st.markdown(f"**Q:** {q['question']}")
                    if is_correct:
                        st.success(f"**Your Answer:** `{user_ans}` (Correct)")
                    else:
                        st.error(f"**Your Answer:** `{user_ans if user_ans is not None else 'Not Answered'}` (Incorrect)")
                    
                    st.success(f"**Correct Answer:** `{correct_ans_list}`")
                    st.markdown(f"**Explanation:**\n{q['explanation']}")
            
            st.button("Back to Main Menu", type="primary", on_click=reset_to_main_menu)

# --- Other Tabs ---
with tab_history:
    st.header("Test History")
    df = get_test_history()
    if df.empty: st.info("No test history found.")
    else: st.dataframe(df, use_container_width=True)

with tab_search:
    st.header("Search Questions")
    query = st.text_input("Enter a keyword to search for")
    if st.button("Search"):
        if query:
            results = search_questions(query)
            if results:
                st.success(f"Found {len(results)} relevant questions:")
                for res in results:
                    with st.container(border=True):
                        st.markdown(f"**Q:** {res['question_text']}")
                        options = json.loads(res.get('options', '[]'))
                        if options:
                            st.markdown("Options:")
                            for opt in options:
                                st.markdown(f"- {opt}")
            else:
                st.warning("No matching questions found.")