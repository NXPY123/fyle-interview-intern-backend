from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs.exceptions import FyleError
from flask import request

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_teacher
def list_assignments(p):
    """Returns list of assignments"""
    query_params = request.args
    teacher_id = query_params.get('teacher_id')
    teachers_assignments = Assignment.get_assignments_by_teacher(teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_teacher
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    try:
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth=p # Is this the correct parameter?
        )
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    
    except Exception as e:
        db.session.rollback()
        if(str(e)[:-1]=="No assignment with this id was found"):
            raise FyleError(message=str(e), status_code=404)
        raise FyleError(message=str(e), status_code=400)
    
    return APIResponse.respond(data=graded_assignment_dump)

