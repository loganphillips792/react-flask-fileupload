# react-flask-fileupload

This is a simple Flask and React application where a user can upload a file and then it gets changed to black and white and then returned to the user.

## Installing Python dependencies

1. ```python3 -m venv ~/Desktop/FileUpload```
2. ```source ~/Desktop/FileUpload/bin/activate``` - this line activates the virtual environment so your Python will use an packages that are installed in it
3. ```which pip``` to verify what is being used (Should point to the one from the virtual environment)
4. ```~/Desktop/FileUpload/bin/python3 -m pip install --upgrade pip```
5. ```pip install -r requirements.txt```

## Running the application

cd react-flask-fileupload

python backend/db/__init__db.py

python3 backend/app/app.py



```curl -X POST -F "image=@/Users/Logan/Downloads/profile.jpg" http://127.0.0.1:5000/upload```

```curl -O http://localhost:5000/image/<filename>```

## Running through Docker

```cd react-flask-fileupload```

```docker build -t your-flask-app -f backend/build/Dockerfile .```

```docker run -p 5001:5000 your-flask-app```

# Environment Variables

# Generating AWS Credentials

1. Select your account name in the top right corner
2. Select Security Credentials from the drop-down list
3. 'Create access key'