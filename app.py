
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


# Check whether input contains recognizable words
def is_meaningful_input(text):
    common_words = {
        "what", "why", "how", "when", "where", "who",
        "is", "are", "was", "were", "the", "a", "an",
        "explain", "define", "describe", "tell", "me",
        "about", "please", "help", "with", "for",
        "artificial", "intelligence", "python", "java",
        "programming", "computer", "science", "ai",
        "html", "css", "javascript", "machine", "learning",
        "can", "you", "do", "does", "in", "of", "to",
        "and", "or", "on", "it", "this", "that",
        "data", "database", "technology", "cloud",
        "web", "development", "code", "write", "give",
        "me", "difference", "between", "example", "list",
        "advantages", "disadvantages", "meaning", "use",
        "work", "works", "make", "create", "explain"
    }

    words = re.findall(r"[a-zA-Z]+", text.lower())

    if not words:
        return False

    # Accept input if it contains at least one recognized word
    return any(word in common_words for word in words)


# Configure webpage
st.set_page_config(
    page_title="AI Agent Validation",
    page_icon="🤖"
)

st.title("🤖 AI Agent with Input Validation")
st.write("Enter your question below.")

# User input
question = st.text_input(
    "Enter your question",
    max_chars=500,
    placeholder="Example: Explain Artificial Intelligence"
)

if st.button("Submit"):

    cleaned_question = question.strip()

    # 1. Empty input validation
    if not cleaned_question:
        st.warning("Please enter a valid question.")

    # 2. Numeric validation
    elif cleaned_question.isdigit():
        st.warning("Please enter a question, not only numbers.")

    # 3. Character validation
    elif not re.search(r"[A-Za-z]", cleaned_question):
        st.warning("Question must contain alphabetic characters.")

    # 4. Length validation
    elif len(cleaned_question) < 3:
        st.warning("Question must contain at least 3 characters.")

    elif len(cleaned_question) > 500:
        st.warning("Question must not exceed 500 characters.")

    # 5. Meaningful-word validation
    elif not is_meaningful_input(cleaned_question):
        st.warning(
            "Your input does not contain recognizable words. "
            "Please enter a meaningful question."
        )

    # 6. API key validation
    elif not api_key:
        st.error("API key not found. Please check your .env file.")

    # 7. Generate AI response
    else:
        try:
            client = genai.Client(api_key=api_key)

            with st.spinner("Generating response..."):
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=cleaned_question
                )

            if response.text:
                st.success("Question accepted!")
                st.write("**Your Question:**", cleaned_question)
                st.write("**AI Response:**")
                st.write(response.text)
            else:
                st.warning("The AI returned an empty response.")

        # 8. Exception handling
        except Exception as e:
            st.error("Unable to process your question.")
            st.caption(f"Error details: {e}")
