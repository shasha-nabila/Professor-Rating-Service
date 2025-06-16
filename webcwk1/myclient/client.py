import requests
import json

BASE_URL = "https://sc22snba.pythonanywhere.com/" 

session = requests.Session()
TOKEN = None 

def safe_request(method, url, **kwargs):
    global TOKEN
    headers = kwargs.get("headers", {})

    if TOKEN and "rate" in url:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    kwargs["headers"] = headers

    try:
        response = session.request(method, url, **kwargs)
        response.raise_for_status() 
        return response

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Check the URL and your internet connection.")
    
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Try again later.")
    
    except requests.exceptions.HTTPError:
        if response is not None:
            print(f"HTTP Error {response.status_code}: {response.text}")
        else:
            print("HTTP Error: Unknown error occurred (no response received).")
    
    except requests.exceptions.RequestException as e:
        print(f"General Request Error: {str(e)}")
    
    return None  

def register():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    data = {"username": username, "email": email, "password": password}
    response = safe_request("POST", f"{BASE_URL}/api/register/", json=data)

    if response:
        print("Registration successful!")
    else:
        print("Registration failed.")

def login(url):
    global TOKEN, BASE_URL
    
    if TOKEN:
        print("Logging out previous user before logging in...")
        logout()
    
    BASE_URL = url
    username = input("Enter username: ")
    password = input("Enter password: ")

    response = safe_request("POST", f"{BASE_URL}/api/login/", json={"username": username, "password": password})

    if response and response.status_code == 200:
        TOKEN = response.json().get("access", "")
        print("Login successful!")
    else:
        print("Login failed. Check credentials.")

def logout():
    global TOKEN
    if not TOKEN:
        print("You are not logged in.")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = safe_request("POST", f"{BASE_URL}/api/logout/", headers=headers, json={})

    if response:
        TOKEN = None 
        print("Logout successful!")
    else:
        print("Error logging out.")

def list_modules():
    response = safe_request("GET", f"{BASE_URL}/api/modules/")
    if response:
        try:
            for module in response.json():
                print(f"\nModule: {module['code']} - {module['name']} ({module['year']}, Semester {module['semester']})")
                print(f"Taught by: {', '.join(module['professors'])}")
        except (KeyError, TypeError):
            print("Error: Unexpected response format.")

def view_professors():
    response = safe_request("GET", f"{BASE_URL}/api/professors/")
    if response:
        try:
            for prof in response.json():
                professor_name = prof.get("name", "Unknown")
                professor_id = prof.get("identifier", "Unknown")
                average_rating = prof.get("average_rating")

                rating_display = "No ratings yet" if average_rating is None else "*" * int(average_rating)
                
                print(f"Professor {professor_name} ({professor_id}): {rating_display}")

        except (KeyError, TypeError):
            print("Error: Unexpected response format.")

def average_rating():
    professor_id = input("Enter professor ID: ")
    module_code = input("Enter module code: ")
    response = safe_request("GET", f"{BASE_URL}/api/average/{professor_id}/{module_code}/")

    if response:
        try:
            data = response.json()
            if "errors" in data:
                for key, message in data["errors"].items():
                    print(f"Error: {message}")
            elif "error" in data:
                print(f"Error: {data['error']}")
            else:
                avg_rating = data.get("average_rating", None)
                print(f"Average rating for {professor_id} in {module_code}: {'*' * avg_rating if avg_rating else 'No ratings yet'}")
        except (KeyError, TypeError):
            print("Error: Unexpected response format.")

def rate_professor():
    if not TOKEN:
        print("Error: You must be logged in to rate a professor. Use 'login <URL>' first.")
        return

    professor_id = input("Enter professor ID: ")
    module_code = input("Enter module code: ")
    year = input("Enter year: ")
    semester = input("Enter semester: ")

    while True:
        try:
            rating = int(input("Enter rating (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Invalid rating. Must be between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 5.")

    data = {
        "professor_id": professor_id,
        "module_code": module_code,
        "year": year,
        "semester": semester,
        "rating": rating
    }
    response = safe_request("POST", f"{BASE_URL}/api/rate/", json=data)

    if response:
        print("Rating submitted successfully!")
    else:
        print("Error submitting rating.")

def main():
    while True:
        command = input("\nEnter command (register, login [URL], logout, list, view, average, rate, exit): ").strip().lower()
        parts = command.split()

        if parts[0] == "login":
            if len(parts) < 2:
                print("Usage: login <URL>")
            else:
                login(parts[1])
        elif command == "register":
            register()
        elif command == "logout":
            logout()
        elif command == "list":
            list_modules()
        elif command == "view":
            view_professors()
        elif command == "average":
            average_rating()
        elif command == "rate":
            rate_professor()
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
