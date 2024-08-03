def fetch_llm_completion(prompt):
    # Only OpenAI supported
    from django.conf import settings

    try:
        from openai import OpenAI

        client = OpenAI()

        completion = client.chat.completions.create(
            model=settings.BASE_OPENAI_MODEL,
            messages=[
                {"role": "system", "content": settings.SYSTEM_CONTENT},
                {"role": "user", "content": prompt,},
            ],
        )
        return str(completion.choices[0].message.content)
    except Exception as e:
        return str(e)


def extract_completion_boolean(analysis_text: str) -> bool | None:
    parsed_analysis_text = analysis_text.split()
    if (
        parsed_analysis_text[-2] == "Conclusion:"
        and parsed_analysis_text[-1].rstrip(".") == "Yes"
    ):
        return True
    elif (
        parsed_analysis_text[-2] == "Conclusion:"
        and parsed_analysis_text[-1].rstrip(".") == "No"
    ):
        return False
    else:
        return None


def extract_completion_float(analysis_text: str) -> float | None:
    parsed_analysis_text = analysis_text.split()
    if parsed_analysis_text[-2] == "Conclusion:":
        try:
            return float(parsed_analysis_text[-1].rstrip(".").lstrip("$"))
        except:
            return None
    else:
        return None
