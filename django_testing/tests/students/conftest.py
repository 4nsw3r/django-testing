import pytest
from model_bakery import baker

from students.models import Course


@pytest.fixture()
def student_factory():
    def factory(**kwargs):
        student = baker.make("students.Student", **kwargs)
        return student

    return factory()


@pytest.fixture()
def course_factory():
    def factory(**kwargs):
        course = baker.make("students.Course", **kwargs)
        return course

    return factory


