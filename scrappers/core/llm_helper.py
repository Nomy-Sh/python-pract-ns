"""
LLM Helper - Adapter for local LLM service using Ollama
"""
import logging
from local_llm import OllamaClient
from local_llm.exceptions import LocalLLMError, OllamaNotRunningError, ModelNotFoundError

logger = logging.getLogger(__name__)


class LLMHelper:
    """
    Helper class for LLM-powered operations.

    Thin adapter that wraps local_llm.OllamaClient to maintain compatibility
    with existing scrappers code while using local Ollama models instead of
    Anthropic's Claude API.
    """

    def __init__(self, api_key=None):
        """
        Initialize LLM helper with local Ollama client.

        Args:
            api_key: Ignored (kept for backward compatibility). Local LLM doesn't need API keys.
        """
        try:
            self.client = OllamaClient()
            logger.info("Initialized local LLM client (Ollama)")
        except Exception as e:
            raise ValueError(
                f"Failed to initialize local LLM client: {str(e)}\n"
                "Make sure Ollama is running and models are installed:\n"
                "  1. Start Ollama (open app or run 'ollama serve')\n"
                "  2. Run 'local-llm-setup' to pull models\n"
                "  3. Run 'local-llm-health' to verify"
            )

    def natural_language_to_sql(self, user_query, schema_info=None, database_type="MySQL"):
        """
        Convert natural language query to SQL.

        Args:
            user_query: Natural language query (e.g., "show me all cars sold last month")
            schema_info: Database schema information (tables, columns, relationships)
            database_type: Type of database (MySQL, PostgreSQL, etc.)

        Returns:
            SQL query string
        """
        try:
            sql_query = self.client.natural_language_to_sql(
                user_query=user_query,
                schema_info=schema_info or "",
                database_type=database_type
            )

            # Remove markdown code blocks if present (same as original)
            if sql_query.startswith('```'):
                sql_query = sql_query.split('```')[1]
                if sql_query.startswith('sql'):
                    sql_query = sql_query[3:]
                sql_query = sql_query.strip()

            logger.info(f"Generated SQL: {sql_query}")
            return sql_query

        except (OllamaNotRunningError, ModelNotFoundError) as e:
            logger.error(f"Local LLM error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            raise

    def analyze_query_results(self, data, question):
        """
        Analyze query results using LLM.

        Args:
            data: Query results (as string or dict)
            question: Question to answer about the data

        Returns:
            Analysis/answer string
        """
        try:
            analysis = self.client.analyze_query_results(
                data=data,
                question=question
            )

            logger.info("Analysis completed")
            return analysis

        except (OllamaNotRunningError, ModelNotFoundError) as e:
            logger.error(f"Local LLM error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error analyzing data: {e}")
            raise

    def understand_page_context(self, page_content, question):
        """
        Use LLM to understand page content and make decisions.

        Args:
            page_content: Text content from webpage
            question: What to determine from the content

        Returns:
            LLM's response/decision
        """
        try:
            answer = self.client.understand_page_context(
                page_content=page_content,
                question=question
            )

            return answer

        except (OllamaNotRunningError, ModelNotFoundError) as e:
            logger.error(f"Local LLM error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error understanding context: {e}")
            raise
