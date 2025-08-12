# Import the necessary libraries
import google.generativeai as genai
from google.colab import userdata

# Configure the API with the key from Colab's secrets
GOOGLE_API_KEY = "AIzaSyCaff7NptusA0Tdaa_d03U86T4_YK5Lz_E"
#GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
#genai.configure(api_key=GOOGLE_API_KEY)

# Use a reliable model name for generating content.
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# This list will store all the symptoms the user provides
all_symptoms = []

# Define the core logic function with the new knowledge base prompt
def get_newborn_health_advice(all_symptoms):
    """
    Analyzes all user-provided symptoms against a specific list of newborn danger signs
    and provides a safety-focused, non-diagnostic recommendation.
    """
    symptoms_string = " and ".join(all_symptoms)

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
    - Signs of cardiac disease: Significant distress with cyanosis, tachycardia, murmur, and hepatomegaly.
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

# Create a simplified function to run the chatbot
def main():
    """
    The main function to interact with the user via a simple terminal interface.
    """
    print("Welcome to the SHISHU SURAKSHA. I can help you identify potential signs of serious problems.")
   # print("Note: This is an AI assistant, not a medical professional. Always consult a real doctor.")
    print("-----------------------------------------------------------------------------------------------------")

    while True:
        user_input = input("Please describe a symptom (or type 'done' to finish): ")
        if user_input.lower() == 'done':
            if all_symptoms:
                response = get_newborn_health_advice(all_symptoms)
                print(f"\nAssistant: {response}")
            else:
                print("No symptoms provided. Thank you for using the assistant.")
            break
        elif user_input:
            all_symptoms.append(user_input)
            print(f"Symptom added: '{user_input}'.")
        else:
            print("Please provide a symptom or type 'done'.")

# Run the main function
if __name__ == "__main__":
    main()
