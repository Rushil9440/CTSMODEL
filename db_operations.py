from pymongo import MongoClient
import streamlit as st

# Connect to MongoDB

client = MongoClient(st.secrets['connection_string'])  # Update the URI as needed
db = client["patientDB"]
collection = db["patient_records"]

# Function to add a data record
def add_data(record):
    result = collection.insert_one(record)
    return result.inserted_id

# Function to get an existing data record
def get_data(query):
    result = collection.find_one(query)
    return result

def get_all_data():
    result = collection.find()
    return result

# Function to delete a data record
def delete_data(query):
    result = collection.delete_one(query)
    return result.deleted_count
