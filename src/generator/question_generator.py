from langchain.output_parsers import PydanticOutputParser
from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()  # Initialize Groq LLM
        self.logger = get_logger(self.__class__.__name__)  # Logger for class

    # 🔁 Retry logic and LLM parsing
    def _retry_and_parse(self, prompt, parser, topic, difficulty):
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(
                    f"Generating question for topic: {topic}, difficulty: {difficulty}"
                )

                # Invoke LLM with formatted prompt
                response = self.llm.invoke(
                    prompt.format(topic=topic, difficulty=difficulty)
                )

                # Parse LLM output to Pydantic model
                parsed = parser.parse(response.content)

                self.logger.info("Successfully parsed the question")
                return parsed

            except Exception as e:
                self.logger.error(f"Error during generation: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(
                        f"Generation failed after {settings.MAX_RETRIES} attempts", e
                    )

    # ❓ Generate a multiple-choice question
    def generate_mcq(self, topic: str, difficulty: str = "medium") -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self._retry_and_parse(
                mcq_prompt_template, parser, topic, difficulty
            )

            # ✅ Validate structure
            if (
                len(question.options) != 4
                or question.correct_answer not in question.options
            ):
                raise ValueError("Invalid MCQ structure")

            self.logger.info("Generated a valid MCQ question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)

    # 📝 Generate a fill-in-the-blank question
    def generate_fill_blank(
        self, topic: str, difficulty: str = "medium"
    ) -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self._retry_and_parse(
                fill_blank_prompt_template, parser, topic, difficulty
            )

            # ✅ Validate that blank exists in question
            if "___" not in question.question:
                raise ValueError("Fill-in-the-blank question must contain '___'")

            self.logger.info("Generated a valid fill-in-the-blank question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate fill-in-the-blank: {str(e)}")
            raise CustomException("Fill-in-the-blank generation failed", e)
