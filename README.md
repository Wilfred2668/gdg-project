# Community Platform for Students and Enthusiasts

A Flask-based web application designed to create a collaborative community where students and enthusiasts can connect, learn, and grow. This platform enables users to explore events, join communities, and access learning resources, with separate user and admin roles for enhanced control.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Features
- **User Registration and Authentication**: Secure login system with session-based user roles (Admin & User).
- **Event Management**: Admins can create, view, update, and delete events. Regular users can view and search for events.
- **Dynamic Layouts**: Different layouts for authenticated and non-authenticated users.
- **File Uploads**: Image upload for events, stored securely on the server.

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/Wilfred2668/gdg-project.git
    cd gdg-project
    ```

2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application in terminal**:
    ```bash
    python app.py
    ```

6. **Access the app**:
    Open your browser and go to `http://127.0.0.1:5000`.

## Usage
- **User**: Sign up and log in to view events.
- **Admin**: Log in with admin credentials (`username: admin`, `password: admin123`) to manage events.


## Technologies Used
- **Flask**: Web framework for Python
- **SQLite**: Database for storing user and event data
- **HTML/CSS**: For structuring and styling pages
- **JavaScript**: Enhancing interactivity
- **Werkzeug**: Security for passwords and file management

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

