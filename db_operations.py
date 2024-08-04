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

# Function to update an existing data record
# def update_data(query, new_values):
#     result = collection.update_one(query, {"$set": new_values})
#     return result.modified_count

# Function to delete a data record
def delete_data(query):
    result = collection.delete_one(query)
    return result.deleted_count

# Example usage
if __name__ == "__main__":
    # Add a data record
    new_record = {
        "email": "john.doe@example.com",
        "name": "John Doe", 
        "disease": "fever",
        "description": "xyz",
        "precautions": "don't go out",
        "medications": "paracitamol",
        "diet": "rice",
        "workout": "jogging"
    }
    # record_id = add_data(new_record)
    # print(f"Added record with ID: {record_id}")

    # Get an existing data record
    query = {"email": "john.do@example.com"}
    record = get_data(query)
    print(f"Fetched record: {record}")

    # Update an existing data record
    # new_values = {"age": 31}
    # updated_count = update_data(query, new_values)
    # print(f"Number of records updated: {updated_count}")

    # Delete a data record
    # deleted_count = delete_data(query)
    # print(f"Number of records deleted: {deleted_count}")
