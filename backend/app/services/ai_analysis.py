import json
import os


def _fallback(base: dict, job_description: str) -> dict:
    focus = "the target role" if job_description.strip() else "your next application"
    score = base["overall_score"]
    assessment = f"Your resume currently scores {score}/100. Prioritize the highest-impact edits before tailoring it for {focus}."
    actions = base["improvements"][:3]
    return {
        "executive_assessment": assessment,
        "priority_actions": actions,
        "rewritten_bullet": "Improved [process or product] by [specific action], resulting in [measurable outcome].",
        "ai_enabled": False,
    }


def enrich_analysis(resume_text: str, job_description: str, base: dict) -> dict:
    """Return structured AI guidance when an API key is configured; otherwise use useful local guidance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback(base, job_description)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        schema = {
            "type": "object", "additionalProperties": False,
            "properties": {
                "executive_assessment": {"type": "string"},
                "priority_actions": {"type": "array", "items": {"type": "string"}},
                "rewritten_bullet": {"type": "string"},
            },
            "required": ["executive_assessment", "priority_actions", "rewritten_bullet"],
        }
        prompt = f"""You are a candid resume coach. Use only the supplied resume facts. Never invent skills, employers, metrics, or achievements. Give practical advice for the candidate.\n\nResume:\n{resume_text[:14000]}\n\nJob description:\n{job_description[:8000] or 'Not supplied'}\n\nMeasured signals:\n{json.dumps(base, default=str)}"""
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            input=prompt,
            text={"format": {"type": "json_schema", "name": "resume_coaching", "strict": True, "schema": schema}},
        )
        result = json.loads(response.output_text)
        return {**result, "priority_actions": result["priority_actions"][:3], "ai_enabled": True}
    except Exception:
        return _fallback(base, job_description)
