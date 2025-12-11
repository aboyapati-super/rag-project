import unittest
import os
from langchain_openai import ChatOpenAI
from config import Config

class TestRAGApplication(unittest.TestCase):
    """
    Test suite for the RAG application components.
    """

    def test_environment_variables(self):
        """
        Test that critical environment variables effectively loaded.
        """
        # We ensure that Config can run validate_env_vars without error
        try:
            Config.validate_env_vars()
        except EnvironmentError as e:
            self.fail(f"Environment validation failed: {e}")

    def test_llm_initialization(self):
        """
        Test that the LLM can be initialized with the config settings.
        """
        try:
            llm = ChatOpenAI(
                model=Config.LLM_MODEL_NAME, 
                temperature=Config.LLM_TEMPERATURE
            )
            self.assertIsNotNone(llm)
        except Exception as e:
            self.fail(f"LLM initialization failed: {e}")

    def test_paths_integrity(self):
        """
        Test that configured paths are valid strings (not necessarily that they exist, 
        but that the config logic is sound).
        """
        self.assertTrue(isinstance(Config.DB_PATH, str))
        self.assertTrue(isinstance(Config.DATA_PATH, str))

if __name__ == '__main__':
    unittest.main()