import pytest
from rest_framework.test import APITestCase


pytestmark = [pytest.mark.django_db]


class ApiTest(APITestCase):
    fixtures = ["api/tests/fixtures/api.json", "api/tests/fixtures/user.json"]

    def test_successful(self):
        response = self.client.get(
            "/api/digest/?user_id=1&popularity=1500&spheres='cars, news'"
        )
        assert response.status_code == 200
        assert response.data == [{"content": "test"}, {"content": "test"}]

    def test_fail_user(self):
        response = self.client.get(
            "/api/digest/?user_id=2&popularity=1500&spheres='cars, news'"
        )
        assert response.status_code == 404
        assert response.data == "User not found"

    def test_fail_current_posts(self):
        response = self.client.get(
            "/api/digest/?user_id=1&popularity=3000&spheres='cars, news'"
        )
        assert response.status_code == 204
        assert response.data == "No current posts found"
        response = self.client.get(
            "/api/digest/?user_id=1&popularity=1500&spheres='fail'"
        )
        assert response.status_code == 204
        assert response.data == "No current posts found"
