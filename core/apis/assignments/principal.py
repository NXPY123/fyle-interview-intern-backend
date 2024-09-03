from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from core.libs.exceptions import FyleError
from flask import request

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of graded and submitted assignments"""
    principal_assignments = Assignment.get_assignments_by_principal()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)



@principal_assignments_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def regrade_assignment(p):
    """Regrades an assignment"""
    data = AssignmentGradeSchema().load(request.json)
    print("data",data.id,data.grade)
    try:
        print("SUCESS")
        regraded_assignment=Assignment.re_grade(data.id, data.grade, p)
        db.session.commit()
        regraded_assignment_dump = AssignmentSchema().dump(regraded_assignment)
    
    except Exception as e:
        print("FAIL")
        print(e)
        db.session.rollback()
        message = {
            "data":{
                "state": AssignmentStateEnum.GRADED.value,
                "grade": data.grade
            }
        }
        print(message)
        raise FyleError(message=str(e), status_code=400)
    
    return APIResponse.respond(data=regraded_assignment_dump)
