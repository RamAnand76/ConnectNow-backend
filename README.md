---

# User Connections Web Application

---

This is a web application that allows users to browse, connect, and interact with other users. Users can create an account, log in, browse other users, and send interest messages. The project is built using React for the frontend and a Django REST API for the backend.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Additional Information](#additional-information)

## Prerequisites

Before you start, ensure that you have the following installed on your local machine:

- **Node.js** (v14.x or higher)
- **npm** (v6.x or higher)
- **Python** (v3.7 or higher)
- **Django** (v3.x or higher)
- **Django REST Framework** (v3.x or higher)

## Dependencies

### Frontend (React)

The React frontend requires the following npm packages:

- `axios`: For making HTTP requests to the backend.
- `react-router-dom`: For handling routing in the React app.
- `react-icons`: For using icons in the UI.

### Backend (Django)

The Django backend requires the following Python packages:

- `djangorestframework`: For creating RESTful APIs.
- `djoser`: For user authentication and registration.
- `corsheaders`: For handling CORS (Cross-Origin Resource Sharing) issues.

## Installation

### 1. Clone the Repository(Backend)

```bash
git clone https://github.com/RamAnand76/ConnectNow-backend.git
cd ConnectNow-backend
```

### 2. Create and activate a virtual environment::

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Set Up the Frontend:

```bash
git clone https://github.com/RamAnand76/ConnectNow-frontend.git
cd Connect-frontend
```

### 6. Install the npm packages:

```bash
npm install
```

### 7. Start the React development server:

```bash
npm start
```

## Running the Application

1. **Backend**: The Django backend will run at `http://localhost:8000/` by default.
2. **Frontend**: The React frontend will run at `http://localhost:3000/` by default.

### Accessing the Application

- Open your browser and go to `http://localhost:3000/` to access the frontend.
- Use the login page to authenticate with your credentials.
- After logging in, you can browse users, send interest messages, and more.

## Project Structure

### Backend

- `backend/`
  - `api/`: Contains the Django REST Framework views, serializers, and URLs for the API.
  - `auth/`: Handles user authentication and registration using `djoser`.
  - `settings.py`: Configuration file for the Django project.

### Frontend

- `frontend/`
  - `src/`
    - `components/`: Contains reusable components like `CustomPopup`, `Loading`, `BrowseUsers`, `ChatScreen`, `ConnectionList`, `Dashboard`, `Navbar`, `Login`, `Signup`.
    - `constants/`: Contains default-profile image file.

## Additional Information

### API Endpoints

- **User Authentication**:
  - `/api/auth/login/`: Login endpoint.
  - `/api/auth/signup/`: Signup endpoint.
  - `/api/auth/users/`: Retrieve a list of users.
  - `/api/auth/interests/send/`: Send an interest message to another user.

### UI/UX Design

The application follows a modern, clean, and responsive design pattern. The design is consistent across all pages, with a dark theme and glowing accent colors to enhance user experience.

### Error Handling

The application includes error handling and popup notifications to inform users about successful or failed actions.

### Security

- User passwords are securely hashed and stored using Django's built-in authentication system.
- JWT tokens are used for secure API communication between the frontend and backend.

---
