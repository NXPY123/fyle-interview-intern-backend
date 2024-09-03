from core import db
from sqlalchemy import text

def test_get_assignments_student_1(client, h_student_1):
    print("h_student_1",h_student_1)
    response = client.get(
        '/student/assignments',
        headers=h_student_1,
        # Pass the student id as a query parameter
        query_string={'student_id': 1}
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_2):
    # If assignment already exists, remove it first
    db.engine.execute(
        text("UPDATE assignments SET state = :state WHERE id = :id"),
        {"state": "DRAFT", "id": 4}
    )
    db.session.commit()

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 4,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 2
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    print("error_response",error_response)
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
