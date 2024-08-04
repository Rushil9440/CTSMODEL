import google.generativeai as genai

genai.configure(api_key='AIzaSyAt34rspP8VXiTb4HN0RGYD7osvAKXY5s4')
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]


model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def generate_questions(disease, symptoms):
    prompt = f"""
    Disease: {disease}
    Symptoms: {symptoms}
    Generate 3 yes/no questions to help diagnose this condition, considering the provided symptoms.
    Focus on symptoms and avoid general knowledge questions.
    Example output format:
    1. Do you have a persistent skin rash? (yes/no)
    2. Have you noticed itching in skin folds like armpits or groin? (yes/no)
    """
    response = model.generate_content(prompt)
    return response.text.split('\n')

def generate_personalized_advice(sleep_cycle, activity_level, medical_history, symptoms, disease_answers, severity, disease):
    prompt = f"""
    Based on the following information:
    - Sleep cycle: {sleep_cycle}
    - Activity level: {activity_level}
    - Medical history: {medical_history}
    - Reported symptoms: {symptoms}
    - Answers to disease-specific questions: {disease_answers}
    - Disease severity: {severity}
    - Potential disease: {disease}

    Generate 5 lines of personalized advice on what to improve, what can be done, and what is the next best action.
    Focus on practical, actionable advice tailored to the individual's situation.
    Consider that the patient has not yet seen a doctor and came here first.
    Include advice on whether and when to seek professional medical help based on the severity and symptoms.
    """
    response = model.generate_content(prompt)
    return response.text
