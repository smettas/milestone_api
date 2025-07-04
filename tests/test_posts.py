import pytest
import allure
from api.posts_api import PostsAPI
from utils.data_loader import load_test_data
from utils.json_schema_validator import validate_json

# ✅ Load YAML data
data = load_test_data("post_data.yaml")
negative_data = load_test_data("negative_post_data.yaml")
multiple_data = load_test_data("multiple_post_data.yaml")

@pytest.fixture(scope="module")
def api():
    return PostsAPI()


# 🧪 Test 1: GET All Posts
def test_get_all_posts(api):
    res = api.get_all_posts()
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_post_by_id(api):
    res = api.get_post_by_id(1)
    assert res.status_code == 200
    assert res.json()["id"] == 1

def test_create_post(api):
    payload = data["create_post"]
    res = api.create_post(payload)
    assert res.status_code == 201
    assert res.json()["title"] == "API Automation"
    assert res.json()["body"] == "This post is created by Pytest!"

def test_update_post(api):
    payload = data["update_post"]
    res = api.update_post(1,payload)
    assert res.status_code == 200
    assert res.json()["title"] == "Updated Title will be soon"
    assert res.json()["body"] == "Body is updated"

def test_delete_post(api):
    res = api.delete_post(1)
    assert res.status_code == 200

def test_post_schema_validation(api):
    res = api.get_post_by_id(1)

    # ✅ Define expected schema
    schema = {
        "type": "object",
        "properties": {
            "userId": {"type": "integer"},
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["userId", "id", "title", "body"]
    }
    assert res.status_code == 200
    assert validate_json(res.json(), schema)

def test_authorization_in_header(api):
    res = api.get_all_posts()
    assert res.status_code == 200
    print(f"Authorization header sent successfuly")


#### # ⚠ This test fails on jsonplaceholder because it's a fake API.
# ✅ Will work on real backend API with validation
@pytest.mark.negative_test
@pytest.mark.xfail(reason="Validation not yet implemented")
def test_create_post_missing_title(api):
    payload = negative_data["missing_title"]
    res = api.create_post(payload)
    assert res.status_code in [400, 422], "Expected 400 or 422 for missing title"

@pytest.mark.negative_test
@pytest.mark.xfail(reason="Fake API accepts string ID")
def test_update_post_with_invalid_id(api):
    payload = negative_data["invalid_id_post"]
    res = api.update_post("abc", payload)
    assert res.status_code in [400, 404], "Expected 400 or 404 for invalid ID"

@pytest.mark.negative_test
@pytest.mark.xfail(reason="Fake API allows empty payload")
def test_create_post_with_empty_payload(api):
    payload = negative_data["empty_payload"]
    res = api.create_post(payload)
    assert res.status_code in [400, 422], "Expected 400 or 422 for empty payload"


@allure.feature("posts module")
@allure.story("create post using YAML data")
@allure.title("Test: Crete a Post from YAML")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_post_from_yaml(api):
    payload = data["create_post"]
    res = api.create_post(payload)

    with allure.step("Validate Status Code"):
        assert res.status_code == 201

    with allure.step("Validate Response Title"):
        assert res.json()["title"] == payload["title"]

    with allure.step("Validate Response Body"):
        assert res.json()["body"] == payload["body"]

    allure.attach(str(res.json()), name="Response Body", attachment_type=allure.attachment_type.JSON)

@pytest.mark.parametrize("payload", multiple_data["multiple_posts"])
@allure.feature("posts module")
@allure.story("Create post using Parameterized Data")
@allure.title("Create Parameterized Post")
@allure.severity(allure.severity_level.NORMAL)
def test_create_post_parameterized(api, payload):
    with allure.step(f"Creating post with the title: {payload['title']}"):
        res = api.create_post(payload)
    assert res.status_code == 201
    assert res.json()["title"] == payload["title"]
    allure.attach(str(res.json()), name="Response Body", attachment_type=allure.attachment_type.JSON)\
    

@allure.title("Test Get Post by ID = 10")
def test_get_post_id_10(api):
    res = api.get_post_by_id(10)
    assert res.status_code == 200
    assert res.json()["id"] == 10
