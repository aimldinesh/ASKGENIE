# 🌐 Import required libraries
import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *  # Includes QuizManager and rerun()
from src.generator.question_generator import QuestionGenerator

# 🔧 Load environment variables from .env file
load_dotenv()


def main():
    # 🎨 Streamlit page configuration
    st.set_page_config(page_title="AskGenie 🎓", page_icon="🎓", layout="centered")

    # 🎨 Inject custom CSS for styling
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            color: #1e1e1e;
        }
        h1, h2, h3, h4 {
            font-weight: 600 !important;
        }
        .stButton > button {
            background-color: #1a73e8;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #1558b0;
        }
        .stSidebar {
            background-color: #f5f8fa;
        }
        label, div[data-testid="stFormLabel"], .stSelectbox label,
        .stTextInput label, .stSlider label {
            font-weight: 500 !important;
            color: #1e1e1e !important;
            font-size: 15px !important;
            display: block;
            margin-bottom: 6px;
        }
        .stExpanderHeader {
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 🔄 Initialize Streamlit session state variables
    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "rerun_trigger" not in st.session_state:
        st.session_state.rerun_trigger = False

    # 🧠 App Header
    st.markdown(
        """
        <div style="width:100%;text-align:center;padding:10px;
                    background:#f0f4f8;border-radius:10px;margin-bottom:20px">
            <h1 style="color:#1a73e8;margin:0;">🧠 AskGenie: AI Quiz Generator</h1>
            <p style="color:#444;font-size:16px;">Instantly generate quizzes using LLMs</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 📋 Sidebar configuration for quiz input
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 16px; background-color: #f5f8fa; 
                        border-radius: 12px; border: 1px solid #dbe4ed;
                        margin-bottom: 20px;">
                <h3 style="color: #1a73e8; margin-bottom: 18px;">⚙️ Quiz Configuration</h3>
            """,
            unsafe_allow_html=True,
        )

        # 🧩 Input widgets for quiz generation
        question_type = st.selectbox(
            "📄 Question Format", ["Multiple Choice", "Fill in the Blank"]
        )
        topic = st.text_input(
            "📘 Quiz Topic", placeholder="e.g. Python, Biology, Algebra"
        )
        difficulty = st.selectbox("🚦 Difficulty Level", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("🔢 Number of Questions", 1, 10, 5)

        # 🚀 Button to generate quiz
        generate_btn = st.button("🚀 Generate Quiz")
        st.markdown("</div>", unsafe_allow_html=True)

    # ⚙️ Handle quiz generation logic
    if generate_btn:
        if not topic.strip():
            st.warning("⚠️ Please enter a topic to generate the quiz.")
        else:
            st.session_state.quiz_submitted = False
            generator = QuestionGenerator()
            success = st.session_state.quiz_manager.generate_questions(
                generator, topic, question_type, difficulty, num_questions
            )
            st.session_state.quiz_generated = success
            rerun()

    # 📝 Display quiz to the user
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.markdown("## 📝 Quiz Time!")

        with st.expander("📄 Answer the following questions:", expanded=True):
            st.session_state.quiz_manager.attempt_quiz()

        # ✅ Submit quiz and trigger evaluation
        if st.button("✅ Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    # 📊 Show quiz results after submission
    if st.session_state.quiz_submitted:
        st.markdown("## 📊 Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct = results_df["is_correct"].sum()
            total = len(results_df)
            score = (correct / total) * 100

            st.success(f"🏆 Your Score: **{score:.2f}%** ({correct}/{total} correct)")
            st.markdown("---")

            # ✅ Show each question's correctness
            for _, row in results_df.iterrows():
                q_num = row["question_number"]
                question_text = row["question"]

                if row["is_correct"]:
                    st.success(f"✅ Q{q_num}: {question_text}")
                else:
                    st.error(f"❌ Q{q_num}: {question_text}")
                    st.markdown(f"**Your Answer:** `{row['user_answer']}`")
                    st.markdown(f"**Correct Answer:** `{row['correct_answer']}`")

                st.markdown("---")

            # 💾 Option to save and download results
            with st.expander("💾 Save and Download Results"):
                if st.button("📥 Save Results"):
                    saved_file = st.session_state.quiz_manager.save_to_csv()
                    if saved_file:
                        with open(saved_file, "rb") as f:
                            st.download_button(
                                label="⬇️ Download CSV",
                                data=f.read(),
                                file_name="AskGenie_Quiz_Results.csv",
                                mime="text/csv",
                            )
                    else:
                        st.warning("⚠️ No results available to save.")


# 🟢 Entry point for the Streamlit app
if __name__ == "__main__":
    main()
