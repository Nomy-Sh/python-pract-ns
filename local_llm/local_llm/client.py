"""Core OllamaClient for LLM operations."""
from typing import Optional, Dict, Any, List
from openai import OpenAI

from .config import (
    OLLAMA_API_BASE,
    DEFAULT_GENERAL_MODEL,
    DEFAULT_SQL_MODEL,
    DEFAULT_FAST_MODEL,
    DEFAULT_CODE_MODEL,
    DEFAULT_TIMEOUT,
    DEFAULT_TEMPERATURE,
)
from .exceptions import CompletionError, ModelNotFoundError
from .health import check_ollama_running, get_available_models


class OllamaClient:
    """
    High-level client for Ollama LLM operations.

    Uses OpenAI-compatible API for portability while providing
    task-specific methods for common use cases.
    """

    def __init__(
        self,
        base_url: str = OLLAMA_API_BASE,
        timeout: int = DEFAULT_TIMEOUT,
        temperature: float = DEFAULT_TEMPERATURE,
    ):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama API base URL (OpenAI-compatible endpoint)
            timeout: Request timeout in seconds
            temperature: Default temperature for completions (0.0-1.0)
        """
        self.base_url = base_url
        self.timeout = timeout
        self.temperature = temperature

        # Initialize OpenAI client pointed at Ollama
        self.client = OpenAI(
            base_url=base_url,
            api_key="ollama",  # Ollama doesn't require real API key
            timeout=timeout,
        )

    def _check_model_available(self, model: str) -> None:
        """Verify model is available before using it."""
        try:
            available = get_available_models()
            if model not in available:
                raise ModelNotFoundError(
                    f"Model '{model}' not found. Available models: {', '.join(available)}\n"
                    f"Run 'local-llm-setup' to pull recommended models."
                )
        except Exception as e:
            # If we can't check, let the request fail naturally
            pass

    def chat(
        self,
        message: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        General chat completion.

        Args:
            message: User message/prompt
            system: Optional system message to set context
            model: Model to use (defaults to general model)
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens in response

        Returns:
            Model's response text

        Raises:
            CompletionError: If completion fails
        """
        model = model or DEFAULT_GENERAL_MODEL
        temperature = temperature if temperature is not None else self.temperature

        self._check_model_available(model)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            raise CompletionError(f"Chat completion failed: {str(e)}")

    def natural_language_to_sql(
        self,
        user_query: str,
        schema_info: str,
        database_type: str = "MySQL",
        model: Optional[str] = None,
    ) -> str:
        """
        Convert natural language to SQL query.

        Args:
            user_query: Natural language question
            schema_info: Database schema information
            database_type: Type of database (MySQL, PostgreSQL, etc.)
            model: Model to use (defaults to SQL model)

        Returns:
            Generated SQL query
        """
        model = model or DEFAULT_SQL_MODEL

        system_prompt = f"""You are an expert {database_type} developer. Convert natural language questions to SQL queries.

Database Schema:
{schema_info}

Rules:
- Generate valid {database_type} syntax
- Return ONLY the SQL query, no explanations
- Use proper table and column names from the schema
- Include appropriate WHERE, JOIN, ORDER BY, LIMIT clauses as needed
- For ambiguous queries, make reasonable assumptions based on schema"""

        return self.chat(
            message=user_query,
            system=system_prompt,
            model=model,
            temperature=0.1,  # Low temperature for consistent SQL
        )

    def analyze_query_results(
        self,
        data: Any,
        question: str,
        model: Optional[str] = None,
    ) -> str:
        """
        Analyze query results and answer questions about the data.

        Args:
            data: Query results (list of dicts, DataFrame, etc.)
            question: Question about the data
            model: Model to use (defaults to general model)

        Returns:
            Natural language analysis
        """
        model = model or DEFAULT_GENERAL_MODEL

        # Convert data to string representation
        if hasattr(data, 'to_dict'):  # pandas DataFrame
            data_str = str(data.to_dict(orient='records'))
        else:
            data_str = str(data)

        system_prompt = """You are a data analyst. Analyze the provided data and answer questions clearly and concisely.

Focus on:
- Direct answers to the question
- Key insights from the data
- Relevant statistics or patterns
- Clear, non-technical language"""

        prompt = f"""Question: {question}

Data:
{data_str}

Please analyze the data and provide a clear answer."""

        return self.chat(
            message=prompt,
            system=system_prompt,
            model=model,
        )

    def understand_page_context(
        self,
        page_content: str,
        question: str,
        model: Optional[str] = None,
    ) -> str:
        """
        Understand webpage context to answer questions about it.

        Args:
            page_content: HTML or text content of the page
            question: Question about the page
            model: Model to use (defaults to fast model for quick analysis)

        Returns:
            Answer based on page content
        """
        model = model or DEFAULT_FAST_MODEL

        system_prompt = """You are a web page analyzer. Extract relevant information from page content to answer questions.

Focus on:
- Key elements and structure
- Relevant text and data
- Actionable information
- Concise, clear answers"""

        # Truncate very long content to avoid token limits
        max_content_length = 8000
        if len(page_content) > max_content_length:
            page_content = page_content[:max_content_length] + "\n... (content truncated)"

        prompt = f"""Question: {question}

Page Content:
{page_content}

Please analyze the page and answer the question."""

        return self.chat(
            message=prompt,
            system=system_prompt,
            model=model,
        )

    def generate_sql_schema_description(
        self,
        schema_info: Dict[str, Any],
        model: Optional[str] = None,
    ) -> str:
        """
        Generate a natural language description of database schema.

        Args:
            schema_info: Schema information (tables, columns, relationships)
            model: Model to use

        Returns:
            Human-readable schema description
        """
        model = model or DEFAULT_GENERAL_MODEL

        system_prompt = """You are a database documentation expert. Create clear, concise descriptions of database schemas.

Include:
- Table purposes
- Key columns and their meanings
- Relationships between tables
- Common query patterns"""

        prompt = f"""Describe this database schema in clear, natural language:

{schema_info}"""

        return self.chat(
            message=prompt,
            system=system_prompt,
            model=model,
        )

    def generate_code(
        self,
        task: str,
        language: str = "python",
        context: Optional[str] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate code based on natural language description.

        Args:
            task: Description of what the code should do
            language: Programming language (python, javascript, etc.)
            context: Optional context (existing code, requirements, etc.)
            model: Model to use (defaults to code model)

        Returns:
            Generated code

        Example:
            code = client.generate_code(
                task="Create a function to calculate fibonacci numbers",
                language="python"
            )
        """
        model = model or DEFAULT_CODE_MODEL

        system_prompt = f"""You are an expert {language} developer. Generate clean, efficient, well-documented code.

Guidelines:
- Write production-ready code
- Include docstrings/comments
- Follow {language} best practices
- Handle edge cases
- Return ONLY the code, no explanations unless asked"""

        prompt = f"Task: {task}"
        if context:
            prompt += f"\n\nContext:\n{context}"

        return self.chat(
            message=prompt,
            system=system_prompt,
            model=model,
            temperature=0.2,  # Low temperature for consistent code
        )

    def review_code(
        self,
        code: str,
        focus: str = "general",
        model: Optional[str] = None,
    ) -> str:
        """
        Review code and provide feedback.

        Args:
            code: Code to review
            focus: What to focus on (general, security, performance, style)
            model: Model to use (defaults to code model)

        Returns:
            Code review with suggestions

        Example:
            review = client.review_code(
                code="def add(a,b): return a+b",
                focus="style"
            )
        """
        model = model or DEFAULT_CODE_MODEL

        focus_prompts = {
            "general": "overall code quality, readability, and best practices",
            "security": "security vulnerabilities and potential exploits",
            "performance": "performance issues and optimization opportunities",
            "style": "code style, naming conventions, and formatting",
        }

        focus_text = focus_prompts.get(focus, focus)

        system_prompt = f"""You are an expert code reviewer. Analyze code focusing on {focus_text}.

Provide:
- Issues found (if any)
- Specific suggestions
- Improved code examples (if needed)
- Severity levels (critical, warning, info)"""

        prompt = f"""Review this code:

```
{code}
```

Focus on: {focus_text}"""

        return self.chat(
            message=prompt,
            system=system_prompt,
            model=model,
            temperature=0.3,
        )

    def explain_code(
        self,
        code: str,
        detail_level: str = "concise",
        model: Optional[str] = None,
    ) -> str:
        """
        Explain what code does in natural language.

        Args:
            code: Code to explain
            detail_level: Level of detail (concise, detailed, beginner)
            model: Model to use (defaults to code model)

        Returns:
            Natural language explanation

        Example:
            explanation = client.explain_code(
                code="lambda x: x**2",
                detail_level="beginner"
            )
        """
        model = model or DEFAULT_CODE_MODEL

        level_prompts = {
            "concise": "Provide a brief, high-level explanation",
            "detailed": "Provide a detailed explanation with step-by-step breakdown",
            "beginner": "Explain in simple terms for beginners, avoiding jargon",
        }

        instruction = level_prompts.get(detail_level, level_prompts["concise"])

        system_prompt = f"""You are a code educator. {instruction}.

Focus on:
- What the code does
- How it works
- Why certain approaches are used
- Any gotchas or edge cases"""

        prompt = f"""Explain this code:

```
{code}
```"""

        return self.chat(
            message=prompt,
            system=system_prompt,
            model=model,
        )
