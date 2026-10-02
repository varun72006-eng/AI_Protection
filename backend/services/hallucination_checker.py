import re


def check_hallucination(prompt, response):

    prompt_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", prompt.lower())
    )

    response_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", response.lower())
    )

    # Question ke important words response me kitne present hain
    if prompt_words:

        matched_words = prompt_words.intersection(response_words)

        relevance = len(matched_words) / len(prompt_words)

    else:

        relevance = 0


    # Basic heuristic score
    if relevance >= 0.5:

        hallucination_score = 5
        factual_consistency = "HIGH"
        issues = []

        explanation = (
            "The response appears relevant to the user question "
            "and no obvious unsupported information was detected "
            "by the local safety check."
        )

    elif relevance >= 0.25:

        hallucination_score = 30
        factual_consistency = "MEDIUM"
        issues = [
            "Response may contain information that is not directly related to the question."
        ]

        explanation = (
            "The response is partially related to the user question, "
            "but some content may require further verification."
        )

    else:

        hallucination_score = 60
        factual_consistency = "LOW"
        issues = [
            "Response appears weakly related to the user question."
        ]

        explanation = (
            "The response has limited overlap with the user question "
            "and may require additional factual verification."
        )


    return {
        "hallucination_score": hallucination_score,
        "factual_consistency": factual_consistency,
        "issues": issues,
        "explanation": explanation
    }