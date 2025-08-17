# core/agents.py
from ddgs import DDGS # Updated import
from .llm_client import generate_json_response
import json

def topic_analysis_agent(topic: str) -> list:
    """Academic Decomposer: Breaks a topic into specific, researchable sub-concepts."""
    system_prompt = """
    You are an expert GATE CSE Academic Decomposer. Your task is to break down a high-level syllabus topic
    into a list of 5-7 specific, granular, and distinct sub-concepts. Each sub-concept must be suitable for
    targeted research to create a single, high-quality exam question. Focus on core principles, landmark algorithms,
    key definitions, and problem-solving scenarios relevant to the GATE exam.
    Output ONLY a JSON object with a single key "sub_concepts" which is a list of strings.
    """
    user_prompt = f"Decompose this GATE CSE topic: '{topic}'"
    response = generate_json_response(system_prompt, user_prompt)
    return response.get("sub_concepts", []) if response else []

def research_agent(sub_concept: str) -> str:
    """Diligent Research Assistant: Gathers rich context for a sub-concept from the web."""
    print(f"🔬 Researching: {sub_concept}")
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(f"in-depth academic explanation of {sub_concept} for computer science students", max_results=4)]
            context = "\n\n---\n\n".join(results)
            return context if context else f"No search results found for {sub_concept}."
    except Exception as e:
        print(f"Error during web search for '{sub_concept}': {e}")
        return f"An error occurred during web search for {sub_concept}."

def question_drafting_agent(context: str, topic: str) -> dict | None:
    """Creative Junior Professor: Drafts a GATE-level question from the provided context."""
    system_prompt = f"""
    You are a Creative Junior Professor specializing in GATE CSE question creation. Your task is to draft a single,
    complex, GATE-style question (MCQ, MSQ, or NAT) strictly based on the provided research context. The question must
    be original and not a direct copy. It should require understanding and application of concepts, not simple recall.

    Topic: {topic}

    Output a single JSON object with this exact structure:
    {{
      "question": "The full question text.",
      "type": "MCQ or MSQ or NAT",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": ["B"],
      "explanation": "A detailed, step-by-step explanation."
    }}
    - For NAT questions, "options" must be an empty list and "answer" a list with one numeric string (e.g., ["5.75"]).
    - For MSQ questions, "answer" can have multiple values (e.g., ["A", "C"]).
    """
    user_prompt = f"Draft a question based on this context:\n\n{context}"
    return generate_json_response(system_prompt, user_prompt)

def critique_agent(draft_question: dict, context: str) -> dict | None:
    """Ruthless Senior Moderator: Critiques the draft question for flaws."""
    system_prompt = """
    You are a Ruthless Senior Moderator for the GATE CSE exam committee. Your task is to critically evaluate a draft question.
    Check for:
    1. Factual accuracy based on the provided context.
    2. Clarity and lack of ambiguity.
    3. Plausibility and quality of distractors (incorrect options).
    4. Correctness of the answer and the depth of the explanation.
    5. Appropriateness of the difficulty for the GATE exam.

    Provide your critique as a JSON object with two keys:
    "is_exam_ready": boolean (true if perfect, false if it needs changes)
    "critique": "A concise, actionable list of required improvements. If none are needed, say 'The question is exam-ready.'"
    """
    user_prompt = f"Context:\n---\n{context}\n---\nDraft Question JSON:\n---\n{json.dumps(draft_question, indent=2)}\n---"
    return generate_json_response(system_prompt, user_prompt)

def refinement_agent(draft_question: dict, critique: dict, context: str) -> dict | None:
    """Senior Professor & Editor: Rewrites the question to address the critique."""
    system_prompt = """
    You are a Senior Professor and Editor-in-Chief of the GATE CSE exam committee. Your task is to revise and finalize
    a draft question based on a senior moderator's critique. Address every point in the critique to create a polished,
    unambiguous, and factually correct exam-ready question.

    The final JSON output must have this exact structure:
    {{
      "question": "string",
      "type": "MCQ/MSQ/NAT/FIGURE",
      "options": ["A", "B", "C", "D"],
      "answer": ["B"],
      "explanation": "string",
      "difficulty": "GATE-level",
      "topic": "string"
    }}
    """
    user_prompt = f"Original Context:\n---\n{context}\n---\nDraft Question:\n---\n{json.dumps(draft_question, indent=2)}\n---\nCritique:\n---\n{json.dumps(critique, indent=2)}\n---\nPlease provide the final, refined question JSON."
    return generate_json_response(system_prompt, user_prompt)