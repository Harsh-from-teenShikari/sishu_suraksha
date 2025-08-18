# app.py
# Import the necessary libraries
import streamlit as st
import google.generativeai as genai
import os

# --- Securely Configure the API Key ---
# When deploying, Streamlit will read this key from the app's secrets.
# For local testing, you can put it in .streamlit/secrets.toml
try:
    # Use st.secrets to access the API key securely
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API key not found. Please set the GOOGLE_API_KEY as a Streamlit secret.")
    st.stop()

# Use a reliable model name for generating content.
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# This list will store all the symptoms the user provides
all_symptoms = []

# Define the core logic function with your knowledge base
def get_newborn_health_advice(user_input_list):
    """
    Analyzes user-provided symptoms against a specific list of newborn danger signs
    and provides a safety-focused, non-diagnostic recommendation.
    """
    symptoms_string = " and ".join(user_input_list)

    prompt = f"""
    You are a chatbot designed to provide direct, non-diagnostic information about newborn health concerns.
    Your sole purpose is to determine if a reported symptom is a potential sign of a serious issue that requires immediate medical attention.
    You must NEVER provide specific diagnoses, recommend treatments, or tell parents to perform any actions on the child.
    Your responses must be clear, concise, and focused on safety.

    Your knowledge base for newborn danger signs and their probable problems is as follows:
    - Lethargy/poor feeding: A very important and sensitive indicator of neonatal illness.
    - Prolonged Capillary Refill Time (CRT) > 3 seconds: Indicates poor perfusion.
    - Respiratory problems: A fast breathing rate (>60/min) or chest retractions.
    - Temperature instability: Hypothermia (<36.5°C) or fever (>37.5°C) is a very important danger sign.
    - Failure to pass meconium by 24 hours or urine by 48 hours: Indicates intestinal obstruction or obstructive uropathy.
    - Persistent or bile-stained vomiting: May indicate intestinal obstruction.
    - Diarrhea: Change in established bowel pattern.
    - Central cyanosis (bluish lips/tongue): Indicates underlying cardiac or respiratory disease.
    - Pathological jaundice (appears on day 1, on palms/soles, or persists >2 weeks): Can lead to kernicterus.
    - Choking/cyanosis during first feed: May be due to Tracheo-esophageal fistula.
    - Signs of cardiac disease: Significant distress with cyanosis, tachycardia, murmur and hepatomegaly.
    - Excessive weight loss: >10% in a term baby.

    Based on the following symptoms provided by a parent, identify the most probable problem from your knowledge base.

    Parent's description (all symptoms): "{symptoms_string}"

    Please provide a concise summary of the probable problem based on all the symptoms listed. Then, give a recommendation on whether to seek medical attention.

    Your response must be in one of the following two formats:
    1. **Probable Problem: [A very brief, non-diagnostic summary based on the knowledge base]. Seek Immediate Medical Attention.** [A brief reason].
    2. **Probable Problem: [A very brief, non-diagnostic summary based on the knowledge base]. Consult a Medical Professional.** [A brief reason].
    """
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---
#st.title("👶 Shishu Suraksha")
st.markdown("This is an AI assistant to help you identify potential signs of serious problems in newborns.")
#st.warning("⚠️ **Disclaimer:** This is an AI assistant, not a medical professional. Always consult a real doctor for medical advice.")

if "all_symptoms" not in st.session_state:
    st.session_state.all_symptoms = []

def add_symptom():
    symptom = st.session_state.symptom_input
    if symptom:
        st.session_state.all_symptoms.append(symptom)
        st.session_state.symptom_input = "" # Clear the input box

st.text_area("List all symptoms your newborn is experiencing:", key="symptom_input", on_change=add_symptom)
st.button("Add Symptom")

if st.session_state.all_symptoms:
    st.subheader("Symptoms provided:")
    for symptom in st.session_state.all_symptoms:
        st.markdown(f"- {symptom}")

    if st.button("Get Advice"):
        if st.session_state.all_symptoms:
            with st.spinner("Analyzing symptoms..."):
                response = get_newborn_health_advice(st.session_state.all_symptoms)
                st.success("Analysis complete!")
                st.subheader("Assistant's Advice:")
                st.markdown(response)
        else:
            st.warning("Please add at least one symptom.")
