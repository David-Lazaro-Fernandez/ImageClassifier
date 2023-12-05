import json
import requests

def get_user_bills(type_of_bill: str, user: str) -> json:
    """Returns a list of bills of a given type for a given user"""

    if not type_of_bill:
        return json.dumps({"error": "No bill type provided"})
    
    if not type_of_bill.lower() in ["emitida", "recibida"]:
        return json.dumps({"error": "Invalid bill type"})

    if not user:
        return json.dumps({"error": "No user provided"})

    # Get all users with the name provided
    response = requests.get(f"http://localhost:5000/users?name={user}")
    users = response.json()

    if not users:
        return json.dumps({"error": "No user found"})

    # Return all the found users and ask the user to select one
    return json.dumps({"users": users})

def get_all_bills(type_of_bill: str, user:str) -> json:
    """Returns all the bills of all the users"""

    if not type_of_bill:
        return json.dumps({"error": "No bill type provided"})
    
    if not type_of_bill:
        return json.dumps({"error": "Invalid bill type"})

    """TODO: Get all the users and download all the bills for each one of them"""
    
    return json.dumps({"response": "All bills downloaded successfully for the following users: David, Juan, María, Pedro, Ana, Luis, Carlos, Marta, Javier, Antonio"})

    