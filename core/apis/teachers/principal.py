from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.apis.teachers.schema import TeacherSchema

principal_teacher_resources = Blueprint("principal_teacher_resources", __name__)


@principal_teacher_resources.route("/", methods=["GET"], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)
