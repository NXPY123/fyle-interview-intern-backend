## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### To run the project locally, follow the steps below:

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```

> [!NOTE]  
> If you encounter errors in this step, ensure there is no conflict between your Global Python Interpreter and the Interpreter in the virtual environment created. Try running
`which flask` (On macOS/Linux) or
`where flask` (On Windows)
> to ensure the PATH is updated. Check the `PATH` variable by running `echo $PATH` (On macOS/Linux) or `echo %PATH%` (On Windows). Try
> updating the local shell configuration and reloading it before running `flask db upgrade -d core/migrations/` to see if it fixes the
> issue.

### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```

### Format Code

```
python -m black ./ 
```

### Lint Code

```
ruff check --fix
```

## To run the project in docker, follow the steps below:

### Using Docker Compose

```
docker-compose up --build   
```
The server will be running on http://localhost:6000

### Using Docker

##### Build Docker Image

```
docker build -t fyle-intern-backend .
```

##### Run Docker Container

```
docker run -d --name fyle-intern-backend-container -p 5000:5000 fyle-intern-backend
```

The server exposes port 5000. You can access the server at http://localhost:5000

##### Run Tests

```
docker exec fyle-intern-backend-container pytest --cov -vvv -s tests/
```

##### Format Code

```
docker exec fyle-intern-backend-container python -m black . --check
```

##### Lint Code

```
docker exec fyle-intern-backend-container ruff check . --fix
```

##### Stop and Remove Docker Container

```
docker stop fyle-intern-backend-container
docker rm fyle-intern-backend-container
```

# API Documentation

Postman Collection: [Public Workspace Collection](https://elements.getpostman.com/redirect?entityId=27754545-7a90f904-f8ae-4810-b406-9adfd7337b6f&entityType=collection)

## Auth

- header: "X-Principal"
- value: {"user_id":1, "student_id":1}

## Endpoints

### GET /student/assignments

List all assignments created by a student

```
headers:
X-Principal: {"user_id":1, "student_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T02:53:45.028101",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T02:53:45.034289"
        },
        {
            "content": "THESIS T1",
            "created_at": "2021-09-17T02:53:45.028876",
            "grade": null,
            "id": 2,
            "state": "DRAFT",
            "student_id": 1,
            "teacher_id": null,
            "updated_at": "2021-09-17T02:53:45.028882"
        }
    ]
}
```

### POST /student/assignments
Create a new assignment

```
headers:
X-Principal: {"user_id":2, "student_id":2}

payload:
{
    "content": "some text",
    "teacher_id": 1
}

response:
{
    "data": {
        "content": "some text",
        "created_at": "2021-09-17T03:14:08.572545",
        "grade": null,
        "id": 5,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2021-09-17T03:14:08.572560"
    }
}
```

### POST /student/assignments
Edit an assignment

```
headers:
X-Principal: {"user_id":2, "student_id":2}

payload:
{
    "id": 5,
    "content": "some updated text"
}

response:
{
    "data": {
        "content": "some updated text",
        "created_at": "2021-09-17T03:14:08.572545",
        "grade": null,
        "id": 5,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2021-09-17T03:15:06.349337"
    }
}
```

### POST /student/assignments/submit
Submit an assignment

```
headers:
X-Principal: {"user_id":1, "student_id":1}

payload:
{
    "id": 2,
    "teacher_id": 2
}

response:
{
    "data": {
        "content": "THESIS T1",
        "created_at": "2021-09-17T03:14:01.580467",
        "grade": null,
        "id": 2,
        "state": "SUBMITTED",
        "student_id": 1,
        "teacher_id": 2,
        "updated_at": "2021-09-17T03:17:20.147349"
    }
}
```

### GET /teacher/assignments
List all assignments submitted to this teacher

```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### POST /teacher/assignments/grade
Grade an assignment

```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```

### GET /principal/assignments
List all submitted and graded assignments

```
headers:
X-Principal: {"user_id":5, "principal_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### GET /principal/teachers
List all the teachers

```
headers:
X-Principal: {"user_id":5, "principal_id":1}


response:
{
    "data": [
        {
            "created_at": "2024-01-08T07:58:53.131970",
            "id": 1,
            "updated_at": "2024-01-08T07:58:53.131972",
            "user_id": 3
        }
    ]
}
```

### POST /principal/assignments/grade
Re-grade an assignment

```
headers:
X-Principal: {"user_id":5, "principal_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```



