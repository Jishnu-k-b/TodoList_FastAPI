# Todo List API

The repo contains a Todo List API which is created using FastAPI as framework and uses MongoDB as database.

## Run Locally

Clone the project

```bash
  git clone
```

Go to the project directory

```bash
  cd my-project
```

Create a virtual environment

```bash
python -m venv venv
```

Install the requirements

```bash
pip install -r requirements.txt
```
Make sure you have installed MongoDB in your system.

```bash
Create a database in MongoDB:
todo_db
Create collections:
1. todos
2. users
```

Start the server (setup the config file and database connection before running the project)

```bash
uvicorn core.main:app --reload
```

Or use

```bash
python run.py
```

## Screenshots

![API docs](screenshots/api-docs.png?raw=true "API Docs")
![API docs](screenshots/user-reg.png?raw=true "User reg")
![API docs](screenshots/create-todo.png?raw=true "Create todo")
![API docs](screenshots/view-all-todos.png?raw=true "View all todo")
![API docs](screenshots/update-a-todo.png?raw=true "Update")
![API docs](screenshots/delete-a-todo.png?raw=true "Delete")
