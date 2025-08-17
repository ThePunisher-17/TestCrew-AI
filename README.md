\<div align="center"\>
\<img src="[https://raw.githubusercontent.com/your-username/testcrew-ai/main/assets/logo.png](https://www.google.com/search?q=https://raw.githubusercontent.com/your-username/testcrew-ai/main/assets/logo.png)" alt="TestCrew AI Logo" width="150"/\>
\<h1\>TestCrew AI 🧠✨\</h1\>
\<p\>
\<b\>An advanced, AI-powered exam generation system for GATE Computer Science (CSE) using a multi-agent architecture.\</b\>
\</p\>
\<p\>
\<a href="\#-key-features"\>Features\</a\> •
\<a href="\#-architectural-overview"\>Architecture\</a\> •
\<a href="\#-tech-stack"\>Tech Stack\</a\> •
\<a href="\#-setup-and-installation"\>Installation\</a\> •
\<a href="\#-how-to-use"\>Usage\</a\>
\</p\>

\</div\>

**TestCrew AI** is an intelligent platform designed to provide GATE CSE aspirants with a limitless supply of high-quality, unique practice questions. It moves beyond static question banks by generating complex, GATE-style questions in real-time, tailored to specific subjects or a full-syllabus mock test format.

---

## 🚀 Key Features

- **🤖 Real-Time Question Generation:** Creates fresh questions on demand for any topic in the GATE CSE syllabus.
- **🤝 Multi-Agent Architecture:** Inspired by CrewAI, it uses a "Peer-Review Panel" of specialized AI agents to ensure every question is complex, accurate, and unambiguous.
- **🎯 Topic & Full-Syllabus Tests:** Generate a focused practice test for a specific topic or a full-fledged mock test that mirrors the GATE exam's subject distribution.
- **🛡️ Guaranteed Uniqueness:** Utilizes a RAG system with a vector database (ChromaDB) to check for semantic similarity, ensuring generated questions are unique.
- **💻 Immersive Exam UI:** A clean, professional interface with a live countdown timer and a question navigation palette provides an authentic, distraction-free exam experience.
- **📈 Performance Analytics:** Automatically tracks your test history, allowing you to monitor your progress over time.
- **🔍 Searchable Question Bank:** All generated questions are saved and can be searched, allowing you to review specific concepts.
- **🔒 Local & Private:** Runs entirely on your local machine using Ollama, ensuring your data and usage are private.

---

## 🏛️ Architectural Overview

The system's core is a **Peer-Review Panel** where multiple AI agents collaborate to create and validate each question. This mimics the rigorous process of an academic exam committee.

1.  **Topic Analysis Agent (Decomposer):** Breaks down a high-level topic into specific, researchable sub-concepts.
2.  **Research Agent (Researcher):** Gathers rich, academic-quality context for a specific sub-concept.
3.  **Question Drafting Agent (Drafter):** Creates a draft GATE-level question (MCQ, MSQ, or NAT) from the context.
4.  **Critique Agent (Critic):** Ruthlessly reviews the draft for any flaws, such as ambiguity or factual errors.
5.  **Refinement Agent (Refiner):** Rewrites the question based on the critique to produce a final, polished, exam-ready version.

---

## 💻 Tech Stack

- **Framework:** Streamlit
- **AI Backend:** Python Multi-Agent System
- **LLM Service:** Ollama (for running local models)
- **Vector Database:** ChromaDB
- **Data Handling:** Pandas
- **Core Libraries:** `requests`, `ddgs`, `sentence-transformers`

---

## ⚙️ Setup and Installation

Follow these steps to get TestCrew AI running on your local machine.

### Prerequisites

- **Python 3.8+**
- **Ollama:** Make sure you have [Ollama](https://ollama.com/) installed and running.
- **A Local LLM:** Pull a capable instruction-tuned model. We recommend `deepseek-llm:7b-chat`.
  ```bash
  ollama pull deepseek-llm:7b-chat
  ```

### Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/testcrew-ai.git
    cd testcrew-ai
    ```

2.  **Create and activate a Python virtual environment:**

    - **Windows:**
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - **macOS / Linux:**
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

---

## 📖 How to Use

1.  **Generate a Test:**
    - Navigate to the **"New Test"** tab.
    - Choose between a **Practice Test** (for a specific topic) or a **Full Mock Test**.
    - Configure the options and click the "Generate" button.
2.  **Start the Exam:**
    - You will be taken to the **"Live Exam"** tab.
    - Read the instructions, check the box, and click **"Start Test"**.
3.  **Take the Test:**
    - Answer questions using the provided inputs.
    - Use the **Question Palette** on the right to navigate between questions.
    - Keep an eye on the **timer** in the header.
4.  **Review Results:**
    - After finishing, the view will switch to the results page, where you can review your answers and see detailed explanations.

---

## ✨ Future Enhancements

- **Adaptive Difficulty:** Adjust question difficulty based on user performance.
- **Figure-Based Questions:** Integrate libraries to generate and display diagrams.
- **Advanced Scoring:** Implement GATE's official scoring rules (e.g., negative marking).
- **Fine-Tuned Model:** Fine-tune a smaller model specifically on GATE-style questions.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
