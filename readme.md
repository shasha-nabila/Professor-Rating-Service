-------------------------------------------------------
|                                                     |
|         A RESTful API for Rating Professors         |
|                                                     |
-------------------------------------------------------


===================================
 Instructions for Using the Client
===================================

This command-line client allows users to interact with the Professor Rating API. Below is a list of available commands:


Option        | Description
---------------------------------------------------------------------------------------------
register      | Create a new user (prompts for username, email, password)
login <URL>   | Authenticate user (Example: `login https://sc22snba.pythonanywhere.com`)
logout        | Logs out the currently authenticated user
list          | View all module instances and their professors
view          | Shows each professor's overall average rating
average       | View the average rating of a professor in a specific module
rate          | Rate a professor's teaching in a specific module instance (1-5 scale)
exit          | Closes the application


===================================
    PythonAnywhere Domain Name
===================================

The API is hosted at: https://sc22snba.pythonanywhere.com

Note that:
- If you visit https://sc22snba.pythonanywhere.com, you will see a welcome message in JSON format
- If you visit https://sc22snba.pythonanywhere.com/api, you will be directed to the API root page, where you can explore the available endpoints


===================================
      Admin Login Credentials
===================================

Admin Panel URL: https://sc22snba.pythonanywhere.com/admin

	 Username: admin
	 Password: admin123


===================================
      Additional Information
===================================

- Ensure you are connected to the internet before using the client.
- API uses JWT authentication, meaning a login is required for rating professors.
