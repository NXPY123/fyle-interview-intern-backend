import json
from flask import request
from core.libs import assertions
from functools import wraps


class Auth:
    def __init__(self, p_dict):
        self.user_id = p_dict['user_id']
        self.student_id = p_dict.get('student_id')
        self.teacher_id = p_dict.get('teacher_id')
        self.principal_id = p_dict.get('principal_id')

def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)

        p = Auth(
            p_dict=p_dict
        )

        if request.path.startswith('/principal'):
            assertions.assert_found(p.principal_id, 'No such principal')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper

def authenticate_teacher(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'teacher not found')
        p_dict = json.loads(p_str)
        p = Auth(
            p_dict=p_dict
        )

        if request.path.startswith('/teacher'):
            assertions.assert_found(p.teacher_id, 'No such teacher')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper

def authenticate_student(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        print("p_str",p_str)
        assertions.assert_auth(p_str is not None, 'student not found')
        p_dict = json.loads(p_str)
        p = Auth(
            p_dict=p_dict
        )

        if request.path.startswith('/student'):
            print("STUDENT")
            assertions.assert_found(p.student_id, 'No such student')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper


