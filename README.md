# react-flask-fileupload

This is a simple Flask and React application where a user can upload a file and then it gets changed to black and white and then returned to the user.

## Installing Python dependencies

1. ```python3 -m venv ~/Desktop/FileUpload```
2. ```source ~/Desktop/FileUpload/bin/activate``` - this line activates the virtual environment so your Python will use an packages that are installed in it
3. ```which pip``` to verify what is being used (Should point to the one from the virtual environment)
4. ```~/Desktop/FileUpload/bin/python3 -m pip install --upgrade pip```
5. ```pip install -r requirements.txt```

## Running the application

python3 main.py




```curl -X POST -F "image=@/Users/Logan/Downloads/profile.jpg" http://127.0.0.1:5000/upload```

```curl -O http://localhost:5000/image/<filename>```