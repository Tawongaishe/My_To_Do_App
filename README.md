
# Barbie To-Do App

Barbie To-Do is a web application that helps you manage your tasks and to-do lists effortlessly. With this app, you can create, organize, and track tasks, subtasks, and more. This README will guide you through setting up and using the application.

This project is made with Python and Flask as the main server and html-page renderer. It makes use of Javascript for custom functionalities in which case it interacts with the API called routes.py. Other than 2 functions this API is not used in this application but built for the sake of building extensions on this application in the future. 


https://github.com/Tawongaishe/My_To_Do_App/assets/92609012/313a97c9-1e86-49cc-ae9c-89e2e1d69847


## Table of Contents

- [Features](#features)
- [Project Struture](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)



## Features

- **User Authentication:** Securely log in and log out of your account.
- **Create Lists:** Organize your tasks by creating lists.
- **Add and Manage Tasks:** Easily add, edit, and delete tasks within your lists.
- **Hierarchical Tasks:** Create subtasks and subsubtasks to organize tasks hierarchically.
- **Task Hierarchy:** View tasks, subtasks, and subsubtasks organized in a hierarchy.
- **Move Tasks:** Move tasks between lists with ease.
- **Delete Lists:** Delete lists and their associated tasks.
- **Flash Messages:** Receive informative messages and notifications.

## Project Structure
- `/app`: This is the root directory of the Flask application.

### Static Files
- `/app/static/css`: This directory contains the CSS files used for styling the web pages.
- `/app/static/fonts`: Fonts used in the application are stored here.
- `/app/static/js`: JavaScript files for adding interactivity to the web pages.

### Templates
- `/app/templates`: HTML templates used for rendering different web pages.
  - `base.html`: The base template that provides the overall structure for all pages.
  - `home.html`: The main page for displaying lists and tasks.
  - `list_tasks.html`: A template for displaying tasks within a specific list.
  - `login.html`: The login page for user authentication.
  - `signup.html`: The signup page for user registration.

### Python Files
- `/app/__init__.py`: Initialization file for the Flask application.
- `/app/auth.py`: Contains routes and logic related to user authentication and authorization.
- `/app/models.py`: Defines the database models using SQLAlchemy, including Users, Lists, and Tasks.
- `/app/routes.py`: Originally intended for API routes (not in use except for deleting and editing tasks)
- `/app/web_routes.py`: Contains web routes and logic for rendering the web pages.


## Prerequisites

- Python (version 3 or higher)
- Node (version 3 or higher )
- All other dependencies are included in the requirements.txt file which we will install

An understanding of HTML, CSS, Flask, Python and SQLAlchemy are recommended.

## Installation

To install and run Your Web App Name, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-web-app-name.git
   ```

2. Change to the project directory:

   ```bash
   cd your-web-app-name
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Make sure nothing is running on your port 500:
    If something is already running on port 5000 and you want to stop it, you can follow these steps:

    6.1. **Identify the Process:** First, you need to identify the process that is running on port 5000. You can use the following command to find the process using port 5000:

    On Windows:
    ```bash
    netstat -ano | findstr :5000
    ```

    On macOS and Linux:
    ```bash
    lsof -i :5000
    ```

    These commands will display a list of processes using port 5000, along with their process IDs (PIDs). If there are no processes listed, it means port 5000 is now available.

    If there are listed processes then:
    6.2. **Terminate the Process:** Once you've identified the PID of the process, you can terminate it. Use the following command to kill the process on macOS and Linux:

    ```bash
    kill -9 PID
    ```

    Replace `PID` with the actual process ID you want to terminate.

    On Windows, you can use the `taskkill` command:

    ```bash
    taskkill /F /PID PID
    ```

    Again, replace `PID` with the actual process ID.

    6.3. **Check Port Status:** After terminating the process, you can check the port status again to ensure that nothing is using port 5000:

    On Windows:
    ```bash
    netstat -ano | findstr :5000
    ```

    On macOS and Linux:
    ```bash
    lsof -i :5000
    ```

    If there are no processes listed, it means port 5000 is now available.

    Please exercise caution when terminating processes, especially if you're not sure what the process is. Be sure to terminate only processes that you are certain you no longer need.

7. Run the application:

   ```bash
   python app.py
   ```
This application assumes that you will be using SQLite as your database.

8. Access the app in your web browser at `http://localhost:5000`.

    


## Usage

Here are some basic usage instructions for Your Web App Name:

1. **User Authentication:**
   - Register for an account or log in if you already have one.
   - Log out when you're done.

2. **Create Lists:**
   - Click on "Home" to view your lists.
   - Create a new list by clicking the "Create List" button.

3. **Add and Manage Tasks:**
   - Click on a list to view its tasks.
   - Add a new task to the list.
   - Edit or delete tasks as needed.

4. **Hierarchical Tasks:**
   - Create subtasks or subsubtasks for a task by clicking the "Add Subtask" button.
   - Edit or delete subtasks.

5. **Task Hierarchy:**
   - Tasks are organized hierarchically, making it easy to manage complex projects.

6. **Move Tasks:**
   - Move tasks between lists using the "Move" button.

7. **Delete Lists:**
   - Delete lists and their tasks when you're finished with them.

8. **Flash Messages:**
   - Receive informative messages about your actions and tasks.

## Contributing

To contribute to Your Web App Name, follow these steps:

1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the original branch: `git push origin feature/your-feature-name`.
5. Create a pull request.

