import re

# очистка ответа llm от мусора
def extract_json(text: str) -> str:
    """
    Извлекает JSON из ответа LLM:
    - убирает ```json ```
    - убирает любой текст до/после {}
    """
    text = text.strip()

    # если markdown-блок
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    # на случай если LLM что-то написал до/после
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1:
        text = text[first:last + 1]

    return text
