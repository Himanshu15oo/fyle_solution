from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentGradeSchema, AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint(
    'teacher_assignments_resources', __name__)

# Returns list of assignments for a teacher


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_students(p.teacher_id)
    students_assignments_dump = AssignmentSchema().dump(
        students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)

# Grading assignments


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """grading an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    gradded_assignment = Assignment.grade_assignment(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    gradded_assignment_dump = AssignmentSchema().dump(gradded_assignment)
    return APIResponse.respond(data=gradded_assignment_dump)
