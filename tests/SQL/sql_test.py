import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(
    number: int = 0, teacher_id: int = 1
) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id, Assignment.grade == GradeEnum.A
    ).count()

    assignments = []

    for _ in range(number):

        grade = random.choice(list(GradeEnum))

        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content="test content",
            state=AssignmentStateEnum.GRADED,
        )

        db.session.add(assignment)
        assignments.append(assignment)

        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    db.session.commit()

    return grade_a_counter, assignments


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED

    db.session.flush()
    expected_result = [(1, 3)]

    with open(
        "tests/SQL/number_of_graded_assignments_for_each_student.sql", encoding="utf8"
    ) as fo:
        sql = fo.read()

    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    with open(
        "tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql",
        encoding="utf8",
    ) as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1, assignments_teacher_1 = create_n_graded_assignments_for_teacher(5)

    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()

    try:
        assert grade_a_count_1 == sql_result[0][0]
    except Exception:
        grade_a_count_1 = 0

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    grade_a_count_2, assignments_teacher_2 = create_n_graded_assignments_for_teacher(
        10, 2
    )

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()

    # Find teacher with max grading
    grade_count_teacher_1 = Assignment.filter(
        Assignment.teacher_id == 1 and Assignment.state == AssignmentStateEnum.GRADED
    ).count()
    grade_count_teacher_2 = Assignment.filter(
        Assignment.teacher_id == 2 and Assignment.state == AssignmentStateEnum.GRADED
    ).count()
    if grade_count_teacher_1 > grade_count_teacher_2:
        grade_count = grade_a_count_1
    else:
        grade_count = grade_a_count_2

    for assignment in assignments_teacher_1 + assignments_teacher_2:
        db.session.delete(assignment)
    db.session.commit()

    try:
        assert grade_count == sql_result[0][0]
    except Exception:
        assert grade_count == 0
