from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs.exceptions import FyleError
from flask import request
from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_student
def list_assignments(p):
    """Returns list of assignments"""
    # Get student id from query params
    print("request",request)
    query_params = request.args
    print("query",query_params)
    student_id = query_params.get('student_id')


    students_assignments = Assignment.get_assignments_by_student(student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_student
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    try:
        # Check if content is not empty
        if not request.json.get('content'):
            raise FyleError(message='Content cannot be empty', status_code=400)

        upserted_assignment = Assignment.upsert(assignment)
        db.session.commit()
        upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)

    except Exception as e:
        db.session.rollback()
        raise FyleError(message=str(e), status_code=400)
    
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_student
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)
    print("ID",submit_assignment_payload.id)
    try:
        submitted_assignment = Assignment.submit(
            _id=submit_assignment_payload.id,
            teacher_id=submit_assignment_payload.teacher_id,
            auth=p
        )
        db.session.commit()
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)

    except Exception as e:
        db.session.rollback()
        print("E",str(e)[:-1])
        raise FyleError(message=str(e)[:-1], status_code=400)
    
    return APIResponse.respond(data=submitted_assignment_dump)
