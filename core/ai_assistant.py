"""
AI Security Assistant.

Wraps the OpenAI API to answer security/phishing-related questions,
grounded in the current scan result when one is available. Scoped
via system prompt to stay on-topic and to only state facts that are
actually present in the provided scan data, rather than inventing
details.
"""

from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError


MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are the built-in Security Assistant for UzBank Shield, \
a phishing detection tool for Uzbek banking and payment websites.

Your role is strictly limited to:
- Explaining phishing, typosquatting, SSL/domain security, and scam tactics
- Explaining a specific scan result when one is provided, using ONLY the \
data given to you — never invent scores, domains, or findings not present \
in the provided result
- Answering general questions about online banking safety and how to \
verify legitimate websites

If asked about anything unrelated to security, phishing, or this app's \
purpose, politely decline and redirect the person back to what you can \
help with. Do not answer general knowledge, coding, or unrelated questions.

Keep answers concise and practical. You are not a substitute for official \
guidance from a person's bank."""


class AssistantError(Exception):
    """Raised for user-facing assistant failures (bad key, no connection, etc.)."""
    pass


def _format_scan_context(scan_result):
    """
    Build a compact, factual summary of a scan result to ground the
    assistant's answers. Only includes what's actually in the data.
    """

    if not scan_result:
        return None

    components = scan_result["components"]
    verification = scan_result["verification"]
    payment_verification = scan_result["payment_verification"]

    lines = [
        f"URL: {components['original_url']}",
        f"Risk score: {scan_result['score']}/100 ({scan_result['level']})",
        f"Bank verification: {'Verified — ' + verification['bank'] if verification['verified'] else 'Not verified'}",
    ]

    if verification["possible_typosquatting"]:
        lines.append(
            f"Possible typosquatting of: {verification['closest_domain']} "
            f"({verification['similarity']}% similar)"
        )

    if payment_verification["verified"]:
        lines.append(f"Payment processor verification: Verified — {payment_verification['processor']}")

    lines.append(f"HTTPS: {'Yes' if scan_result['connection']['https'] else 'No'}")
    lines.append(f"Suspicious TLD: {'Yes' if scan_result['suspicious_tld'] else 'No'}")

    if scan_result["page_analysis"]["requests_card_info"]:
        lines.append("Page requests payment card information")

    return "\n".join(lines)


def ask_assistant(api_key, question, scan_result=None, conversation_history=None):
    """
    Send a question to the AI assistant, optionally grounded in a
    scan result and prior conversation turns.

    Returns the assistant's text response.
    Raises AssistantError with a user-facing message on failure.
    """

    if not api_key:
        raise AssistantError("No OpenAI API key configured. Add one in Settings.")

    client = OpenAI(api_key=api_key)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    scan_context = _format_scan_context(scan_result)
    if scan_context:
        messages.append({
            "role": "system",
            "content": f"Current scan result for context:\n{scan_context}"
        })

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.3
        )

        return response.choices[0].message.content

    except AuthenticationError:
        raise AssistantError("Invalid OpenAI API key. Check it in Settings.")

    except RateLimitError:
        raise AssistantError("OpenAI rate limit or quota exceeded. Try again later.")

    except APIConnectionError:
        raise AssistantError("Could not connect to OpenAI. Check your internet connection.")

    except Exception as error:
        raise AssistantError(f"Assistant request failed: {error}")