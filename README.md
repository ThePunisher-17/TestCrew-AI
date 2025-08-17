
# TestCrew AI 🧠✨

**An advanced, AI-powered exam generation system for GATE Computer Science (CSE) using a multi-agent architecture.**

TestCrew AI is an intelligent platform designed to provide GATE CSE aspirants with a limitless supply of high-quality, unique practice questions. It moves beyond static question banks by generating complex, GATE-style questions in real-time, tailored to specific subjects or a full-syllabus mock test format.

-----

## 🚀 Key Features

  * **Real-Time Question Generation:** Creates fresh questions on demand for any topic in the GATE CSE syllabus.
  * **Multi-Agent Architecture:** Inspired by CrewAI, it uses a "Peer-Review Panel" of specialized AI agents (Decomposer, Researcher, Drafter, Critic, Refiner) to ensure every question is complex, accurate, and unambiguous.
  * **Topic & Full-Syllabus Tests:** Generate a focused practice test for a specific topic or a full-fledged mock test that mirrors the GATE exam's subject distribution.
  * **Guaranteed Uniqueness:** Utilizes a RAG (Retrieval-Augmented Generation) system with a vector database (ChromaDB) to check for semantic similarity, ensuring generated questions are unique.
  * **Immersive Exam UI:** A clean, professional interface with a live countdown timer and a question navigation palette provides an authentic, distraction-free exam experience.
  * **Performance Analytics:** Automatically tracks your test history, allowing you to monitor your progress over time.
  * **Searchable Question Bank:** All generated questions are saved and can be searched, allowing you to review specific concepts.
  * **Local & Private:** Runs entirely on your local machine using Ollama, ensuring your data and usage are private.

-----

## 🏛️ Architectural Overview

The system's core is a **Peer-Review Panel** where multiple AI agents collaborate to create and validate each question. This mimics the rigorous process of an academic exam committee.

1.  **Topic Analysis Agent (Academic Decomposer):** Receives a high-level topic (e.g., "Operating System") and breaks it down into specific, researchable sub-concepts (e.g., "Deadlock Prevention").
2.  **Research Agent (Diligent Researcher):** Gathers rich, academic-quality context for a specific sub-concept.
3.  **Question Drafting Agent (Junior Professor):** Creates a draft GATE-level question (MCQ, MSQ, or NAT) strictly from the provided context.
4.  **Critique Agent (Senior Moderator):** Ruthlessly reviews the draft for any flaws, such as ambiguity, factual errors, or poor-quality options.
5.  **Refinement Agent (Editor-in-Chief):** Rewrites the question based on the critique to produce a final, polished, exam-ready version.

This pipeline ensures a high standard of quality for every single question generated.

-----

## 💻 Tech Stack

  * **Framework:** Streamlit
  * **AI Backend:** Python Multi-Agent System
  * **LLM Service:** Ollama (for running local models like Llama 3, Mistral, DeepSeek)
  * **Vector Database:** ChromaDB (for RAG and uniqueness checks)
  * **Data Handling:** Pandas
  * **Core Libraries:** `requests`, `ddgs`, `sentence-transformers`

-----

## ⚙️ Setup and Installation

Follow these steps to get TestCrew AI running on your local machine.

### Prerequisites

  * **Python 3.8+**
  * **Ollama:** Make sure you have [Ollama](https://ollama.com/) installed and running.
  * **A Local LLM:** Pull a capable instruction-tuned model. We recommend `deepseek-llm:7b-chat`.
    ```bash
    ollama pull deepseek-llm:7b-chat
    ```

### Installation Steps

1.  **Clone the repository (or download the source code):**

    ```bash
    git clone https://github.com/your-username/testcrew-ai.git
    cd testcrew-ai
    ```

2.  **Create and activate a Python virtual environment:**

      * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
      * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

The application should now be open and running in your web browser\!

-----

## 📖 How to Use

1.  **Generate a Test:**
      * Navigate to the **"New Test"** tab.
      * For a **Practice Test**, select a subject and topic, choose the number of questions, and click "Generate Practice Test".
      * For a **Full Mock Test**, select the total number of questions and click "Generate Full Mock Test".
2.  **Start the Exam:**
      * You will be taken to the **"Live Exam"** tab.
      * Read the instructions, check the box, and click **"Start Test"**.
3.  **Take the Test:**
      * Answer questions using the radio buttons (MCQ) or checkboxes (MSQ).
      * Use the **Question Palette** on the right to navigate.
      * Keep an eye on the **timer** in the header.
4.  **Review Results:**
      * After finishing, the view will switch to the results page, where you can review your answers and see detailed explanations.
5.  **Check History:**
      * Go to the **"Test History"** tab to see a summary of all your past tests.

-----

## ✨ Future Enhancements

  * **Adaptive Difficulty:** Adjust question difficulty based on user performance.
  * **True Figure-Based Questions:** Integrate libraries like Matplotlib or Graphviz to generate and display diagrams for questions.
  * **Advanced Scoring:** Implement GATE's official scoring rules (e.g., negative marking, marks for MSQs).
  * **Fine-Tuned Model:** Fine-tune a smaller model specifically on GATE-style questions for even better performance and speed.

-----

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
