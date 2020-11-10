import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED

from students.models import Course


@pytest.mark.django_db
def test_course_get(api_client, course_factory):
    course = course_factory()
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert resp_json['id'] == course.id


@pytest.mark.django_db
def test_course_list(api_client, course_factory):
    course = course_factory()
    url = reverse("courses-list")
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_course_filter_id(api_client, course_factory):
    course = course_factory(_quantity=3)
    url = reverse("courses-list")
    resp = api_client.get(url, {'id': 2})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 1


@pytest.mark.django_db
def test_course_filter_name(api_client, course_factory):
    url = reverse("courses-list")
    course = Course.objects.bulk_create([
        Course(name='two course'),
        Course(name='one course'),
    ])
    resp = api_client.get(url, {'name': 'one course'})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 1
    resp_course = resp_json[0]
    assert resp_course['name'] == course[1].name


@pytest.mark.django_db
def test_courses_create(api_client):
    url = reverse("courses-list")
    course = Course.objects.create(
        name='two course'
    )
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 1


@pytest.mark.django_db
def test_course_update(api_client, course_factory):
    course = course_factory(name='update_name')
    params = {"name": "mark"}
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.put(url, params)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert resp_json['id'] == course.id
    assert resp_json['name'] == params.get("name")


@pytest.mark.django_db
def test_course_delete(api_client, course_factory):
    course = course_factory()
    url = reverse("courses-detail", args=(course.id, ))
    resp = api_client.delete(url, {"id": 1})
    assert resp.status_code == HTTP_204_NO_CONTENT
