import streamlit as st
import time
from model import predict_disease
from send_email import send_email
from db_operations import add_data, get_data, delete_data
from pdf_generator import generate_pdf
from symptoms_options import unique_symptoms
import scheduler,schedule
import gen_ai

#scheduler.main()

# Init session_state 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False


def login_page():
    st.title("Login")
    user_email = st.text_input("Email")
    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.user_email = user_email
        st.rerun()


def display_report(user_record):
    st.write('Predicted Health Report')
    st.write(f"Name: {user_record['name']}")
    st.write(f"Predicted Disease: {user_record['disease']}")
    st.write(f"Description: {user_record['description']}")
    st.write(f"Precautions: {user_record['precautions']}")
    st.write(f"Medications: {user_record['medications']}")
    st.write(f"Diet: {user_record['diet']}")
    st.write(f"Workout: {user_record['workout']}")
    st.subheader("Personalized Advice:")
    st.write(f"{user_record['Personalized Advice']}")


def details_page():
    st.title("Disease prediction System")

    if st.session_state.logged_in:
        user_record = {}

        with st.form("details_form"):
            name = st.text_input('Name')
            age = st.number_input('Age', min_value=1,max_value=100)
            symptoms = st.selectbox('Select your primary symptom', options=unique_symptoms)
            sleep_cycle = st.selectbox('What is your sleep cycle?', ['4 hours', '6 hours', '8 hours'])
            activity_level = st.selectbox('How is your life activity level?', ['active', 'very active', 'less active', 'lazy'])
            medical_history = st.selectbox('Do you have a medical history of any of the following diseases?',
                                           ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Cancer", "Arthritis", "Thyroid Disorder", "None of the above"])
            submitted = st.form_submit_button("Submit")
            
            if submitted and name and age and symptoms:
                st.session_state.form_submitted = True
                disease, description, precautions, medications, diet, workout = predict_disease(symptoms)
                questions=gen_ai.generate_questions(disease, symptoms)
                st.session_state.answers = []
                st.session_state.questions=questions
                for i in st.session_state.questions:
                    answer = st.selectbox(i, ["Yes", "No"],key=i)
                    time.sleep(2)
                    if answer:
                        st.session_state.answers.append(answer)
                        time.sleep(2)
                print(st.session_state)
                severity = "High" if st.session_state.answers.count('Yes') >= 2 else "Low"
                advice = gen_ai.generate_personalized_advice(sleep_cycle, activity_level, medical_history, symptoms, st.session_state.answers, severity, disease)
                user_record = {
                    "name": name,
                    "age": age,
                    "email": st.session_state.user_email,
                    "disease": disease,
                    "description": description,
                    "precautions": precautions,
                    "medications": medications,
                    "diet": diet,
                    "workout": workout,
                    'Personalized Advice': advice
                }

                # Add to database
                add_data(user_record)

                # send-email
                send_email(user_record)
                st.write("Health report is sent to your email. Do check out!")

                # Display on-screen
                display_report(user_record)

                # Generate pdf and save as "medical_report.pdf"
                generate_pdf(user_record)


        if st.session_state.form_submitted:
            with open("medical_report.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()

            st.download_button(
                label="Download your report",
                data=PDFbyte,
                file_name="medical_report.pdf",
                mime='application/octet-stream'
            )


def display_existing_user(user_record):
    st.write("You are already been diagnosed with a disease.")
    st.write(f"Have you recovered from {user_record['disease']}?")
    if st.button("Yes, recovered!"):
        delete_data({"email": user_record['email']})
        st.write("Response recieved! You will no longer recieve emails regarding this disease")
        st.rerun()
    
    if st.button("No"):
        st.write("Get well soon :-)")
        display_report(user_record)


def main():
    if st.session_state.logged_in:
       # user already has a running process - stop_process()
        user_record = get_data({"email": st.session_state.user_email})
        if user_record:
            display_existing_user(user_record)

        # new user - display details_page()
        else:
            details_page()
    else:
        login_page()


if __name__ == "__main__":
    main()                
    
