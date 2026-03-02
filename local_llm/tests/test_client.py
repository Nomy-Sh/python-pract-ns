"""Smoke tests for OllamaClient."""
import pytest
from local_llm import OllamaClient, check_ollama_running
from local_llm.exceptions import CompletionError


@pytest.fixture
def client():
    """Create a test client."""
    return OllamaClient()


def test_client_initialization():
    """Test that client can be initialized."""
    client = OllamaClient()
    assert client is not None
    assert client.client is not None


@pytest.mark.skipif(not check_ollama_running(), reason="Ollama not running")
def test_chat_basic(client):
    """Test basic chat completion."""
    response = client.chat(
        message="Say 'test successful' and nothing else.",
        temperature=0.1,
    )
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.skipif(not check_ollama_running(), reason="Ollama not running")
def test_natural_language_to_sql(client):
    """Test SQL generation."""
    schema = """
    Table: users
    - id (INT, PRIMARY KEY)
    - name (VARCHAR)
    - email (VARCHAR)
    """

    response = client.natural_language_to_sql(
        user_query="Get all users",
        schema_info=schema,
    )
    assert response is not None
    assert isinstance(response, str)
    assert "SELECT" in response.upper()


@pytest.mark.skipif(not check_ollama_running(), reason="Ollama not running")
def test_analyze_query_results(client):
    """Test data analysis."""
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]

    response = client.analyze_query_results(
        data=data,
        question="What is the average age?",
    )
    assert response is not None
    assert isinstance(response, str)


@pytest.mark.skipif(not check_ollama_running(), reason="Ollama not running")
def test_understand_page_context(client):
    """Test page understanding."""
    page_content = """
    <html>
    <body>
        <h1>Welcome</h1>
        <p>This is a test page.</p>
    </body>
    </html>
    """

    response = client.understand_page_context(
        page_content=page_content,
        question="What is the main heading?",
    )
    assert response is not None
    assert isinstance(response, str)
