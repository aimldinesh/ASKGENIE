import os
import streamlit as st
import pandas as pd
from src.generator.question_generator import QuestionGenerator


# 🔁 Forces Streamlit to rerun the script (used for refreshing UI state)
def rerun():
    st.session_state["rerun_trigger"] = not st.session_state.get("rerun_trigger", False)


# 🧠 QuizManager handles quiz generation, user input collection, evaluation, and result export
class QuizManager:
    def __init__(self):
        self.questions = []  # Holds all generated questions
        self.user_answers = []  # Stores user answers from input widgets
        self.results = []  # Stores evaluation output

    # 📋 Generate quiz questions using a specified generator, topic, type, and difficulty
    def generate_questions(
        self,
        generator: QuestionGenerator,
        topic: str,
        question_type: str,
        difficulty: str,
        num_questions: int,
    ):
        # Clear previous quiz data
        self.questions = []
        self.user_answers = []
        self.results = []

        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    # Generate MCQ using LLM
                    question = generator.generate_mcq(topic, difficulty.lower())

                    self.questions.append(
                        {
                            "type": "MCQ",
                            "question": question.question,
                            "options": question.options,
                            "correct_answer": question.correct_answer,
                        }
                    )
                else:
                    # Generate Fill-in-the-Blank question using LLM
                    question = generator.generate_fill_blank(topic, difficulty.lower())

                    self.questions.append(
                        {
                            "type": "Fill in the blank",
                            "question": question.question,
                            "correct_answer": question.answer,
                        }
                    )
        except Exception as e:
            st.error(f"Error generating question: {e}")
            return False

        return True

    # 🧑‍🏫 Display each quiz question and collect user answers
    def attempt_quiz(self):
        # Inject custom styles to ensure visibility in light/dark themes
        st.markdown(
            """
            <style>
                .question-block {
                    padding: 1rem;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #ffffff;
                    margin-bottom: 20px;
                }
                .question-text {
                    font-size: 18px;
                    font-weight: bold;
                    color: #000000;
                    margin-bottom: 10px;
                }
                div[data-baseweb="radio"] > div {
                    color: #000000 !important;
                    background-color: #ffffff !important;
                }
                /* ✅ Hover effect for MCQ options */
                div[data-baseweb="radio"] div:hover {
                    background-color: #f5f5f5 !important;
                    cursor: pointer;
                }
                div[data-baseweb="radio"] label span {
                    color: #000000 !important;
                    font-size: 16px;
                }
                label[data-testid="stRadioLabel"] {
                    color: #000000 !important;
                    font-weight: 600;
                    font-size: 16px;
                    margin-bottom: 8px;
                    display: block;
                }
                input[type="text"] {
                    background-color: #ffffff !important;
                    color: #000000 !important;
                    border: 1px solid #ccc !important;
                    padding: 8px;
                    border-radius: 5px;
                    font-size: 16px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Render all questions with appropriate input method
        for i, q in enumerate(self.questions):
            st.markdown(
                f'<div class="question-text">Question {i + 1}: {q["question"]}</div>',
                unsafe_allow_html=True,
            )

            if q["type"] == "MCQ":
                st.markdown("**📝 Select your answer:**", unsafe_allow_html=True)
                st.radio(
                    label="",
                    options=q["options"],
                    key=f"mcq_{i}",
                )
            else:
                st.text_input(
                    "✍️ Enter your answer:",
                    key=f"fill_blank_{i}",
                    label_visibility="visible",
                )

            st.markdown("</div>", unsafe_allow_html=True)

    # ✅ Compares user answers with correct ones and records results
    def evaluate_quiz(self):
        self.results = []
        self.user_answers = []  # Reset previous input cache

        for i, q in enumerate(self.questions):
            # Get user answer from Streamlit state
            user_ans = st.session_state.get(
                f"mcq_{i}" if q["type"] == "MCQ" else f"fill_blank_{i}", ""
            )

            self.user_answers.append(user_ans)

            result_dict = {
                "question_number": i + 1,
                "question": q["question"],
                "question_type": q["type"],
                "user_answer": user_ans,
                "correct_answer": q["correct_answer"],
                "options": q.get("options", []),
                "is_correct": False,
            }

            # Compare answers with normalization
            if q["type"] == "MCQ":
                result_dict["is_correct"] = user_ans == q["correct_answer"]
            else:
                result_dict["is_correct"] = (
                    user_ans.strip().lower() == q["correct_answer"].strip().lower()
                )

            self.results.append(result_dict)

    # 📊 Converts the quiz results to a pandas DataFrame
    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)

    # 💾 Saves quiz results to a timestamped CSV in the 'results' directory
    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.warning("No results to save !!")
            return None

        df = self.generate_result_dataframe()
        from datetime import datetime

        # Construct timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filename_prefix}_{timestamp}.csv"

        os.makedirs("results", exist_ok=True)
        full_path = os.path.join("results", unique_filename)

        try:
            df.to_csv(full_path, index=False)
            st.success("Results saved successfully....")
            return full_path
        except Exception as e:
            st.error(f"Failed to save results: {e}")
            return None
