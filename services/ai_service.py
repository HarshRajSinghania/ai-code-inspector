# app/services/ai_service.py
from google import genai
from config import settings

# Initialize Gemini Client with API key from settings
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def inspect_code_diff(diff_text: str) -> str:
    """
    Sends the git diff payload to Gemini 1.5 Flash for domain-specific code analysis.
    """
    prompt = f"""
    You are an expert Senior Developer and AI Code Security Inspector.
    Analyze the following git diff for a Pull Request and provide feedback on:

    1. **Critical Bugs & Logic Errors**: Point out edge cases, unhandled exceptions, or potential crashes.
    2. **Security Vulnerabilities**: Detect hardcoded keys, unsafe DB calls, or improper authorization checks.
    3. **Performance & Code Quality**: Suggest quick optimizations or cleaner Pythonic code style.

    Rules:
    - Keep feedback concise, actionable, and formatted in clean Markdown.
    - Reference specific filenames and line changes where relevant.
    - If no major issues are found, confirm the changes look good.

    Git Diff Payload:
    ```diff
    {diff_text}
    ```
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error running AI Code Inspection: {str(e)}"