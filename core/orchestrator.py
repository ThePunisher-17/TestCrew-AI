# core/orchestrator.py
import concurrent.futures
import random
import json
import sqlite3
from .agents import (
    topic_analysis_agent,
    research_agent,
    question_drafting_agent,
    critique_agent,
    refinement_agent
)
from components.vector_store import find_similar_question, add_question_to_rag
from components.analytics import DB_FILE
from config.syllabus import GATE_CSE_SYLLABUS

# --- NEW: Blueprint for Full Mock Test ---
# Defines the approximate percentage of questions from each subject.
MOCK_TEST_BLUEPRINT = {
    "Engineering Mathematics": 0.15,
    "Computer Organization and Architecture": 0.10,
    "Programming and Data Structures": 0.15,
    "Algorithms": 0.15,
    "Operating System": 0.10,
    "Databases": 0.10,
    "Computer Networks": 0.10,
    "Digital Logic": 0.05,
    "Theory of Computation": 0.05,
    "Compiler Design": 0.05,
}

def save_question_to_db(q_data: dict) -> int:
    # This function is unchanged
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO question_bank (topic, question_type, question_text, options, answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                q_data['topic'],
                q_data['type'],
                q_data['question'],
                json.dumps(q_data.get('options', [])),
                json.dumps(q_data.get('answer', [])),
                q_data['explanation']
            )
        )
        conn.commit()
        return cursor.lastrowid

def generate_question_pipeline(topic: str, max_retries=3):
    # This function is unchanged
    for attempt in range(max_retries):
        print(f"\n🚀 Starting pipeline for topic: {topic} (Attempt {attempt + 1})")

        sub_concepts = topic_analysis_agent(topic)
        if not sub_concepts:
            print(f"  - Agent failed: TopicAnalysisAgent on '{topic}'.")
            continue
        selected_concept = random.choice(sub_concepts)

        context = research_agent(selected_concept)
        if "error" in context or "No search results" in context:
            print(f"  - Agent failed: ResearchAgent on '{selected_concept}'.")
            continue

        draft_question = question_drafting_agent(context, topic)
        if not draft_question:
            print("  - Agent failed: QuestionDraftingAgent returned nothing.")
            continue

        critique = critique_agent(draft_question, context)
        if not critique:
            print("  - Agent failed: CritiqueAgent returned nothing.")
            continue

        if not critique.get("is_exam_ready", False):
            final_question = refinement_agent(draft_question, critique, context)
        else:
            final_question = draft_question
            final_question['difficulty'] = 'GATE-level'

        if not final_question:
            print("  - Agent failed: RefinementAgent returned nothing.")
            continue
        
        final_question['topic'] = topic

        if not find_similar_question(final_question['question']):
            question_id = save_question_to_db(final_question)
            if question_id:
                add_question_to_rag(question_id, final_question['question'])
                print(f"✅ Unique question generated and saved with ID: {question_id}")
                return final_question
        
    print(f"🛑 Pipeline failed to generate a unique question for '{topic}' after {max_retries} retries.")
    return None

def generate_test_concurrently(topic: str, num_questions: int):
    # This function is unchanged
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_questions) as executor:
        futures = [executor.submit(generate_question_pipeline, topic) for _ in range(num_questions)]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result: yield result
            except Exception as e:
                print(f"Pipeline execution generated an exception: {e}")
                yield None

# --- NEW: Orchestrator for Full Mock Test ---
def generate_full_mock_test(total_questions: int):
    """Generates a full mock test based on the blueprint."""
    tasks = []
    # Calculate the number of questions for each subject based on the blueprint
    for subject, percentage in MOCK_TEST_BLUEPRINT.items():
        num_questions_for_subject = round(total_questions * percentage)
        if num_questions_for_subject > 0:
            # For each subject, pick random topics to generate questions from
            all_topics_in_subject = GATE_CSE_SYLLABUS[subject]
            for _ in range(num_questions_for_subject):
                # Add a generation task for a random topic within that subject
                tasks.append(random.choice(all_topics_in_subject))

    # Concurrently generate all questions from the task list
    questions = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = [executor.submit(generate_question_pipeline, task) for task in tasks]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result: questions.append(result)
            except Exception as e:
                print(f"A full mock test pipeline execution generated an exception: {e}")

    random.shuffle(questions)
    return questions