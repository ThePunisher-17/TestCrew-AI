# core/llm_client.py
import ollama
import json
import streamlit as st

# --- Configuration ---
# This is the model the application intends to use.
MODEL = 'deepseek-llm:7b-chat'

def check_and_pull_model():
    """
    Checks if the base model is available locally and pulls it if not.
    This is a more robust check that ignores tags.
    """
    try:
        # 💡 NEW LOGIC: We get the base name of the model we want.
        # For "deepseek-llm:7b-chat", this will be "deepseek-llm".
        target_base_model = MODEL.split(':')[0]
        
        # Get the list of all model names from Ollama.
        local_models = [m['name'] for m in ollama.list()['models'] if 'name' in m]
        
        # Check if any of our local models start with the target base name.
        model_is_present = any(name.startswith(target_base_model) for name in local_models)

        if not model_is_present:
            st.info(f"Base model for '{MODEL}' not found locally. Pulling from Ollama Hub...")
            with st.spinner(f"Downloading {MODEL}... (This may take several minutes)"):
                ollama.pull(MODEL)
            st.success(f"Model '{MODEL}' has been downloaded successfully!")

    except Exception as e:
        st.error(f"Error communicating with Ollama. Details: {e}")
        st.stop()

def generate_json_response(system_prompt: str, user_prompt: str) -> dict | None:
    """Sends prompts to the Ollama model and expects a JSON response."""
    try:
        response = ollama.chat(
            model=MODEL,
            format='json',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ]
        )
        response_content = response['message']['content']
        return json.loads(response_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM: {e}")
        print(f"Raw LLM response: {response_content}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred with Ollama: {e}")
        return None