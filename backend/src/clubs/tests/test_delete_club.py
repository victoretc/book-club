import pytest


def test_delete_club(authenticated_clubs_api, club):
    got = authenticated_clubs_api.delete_api_v1_clubs_id_with_http_info(id_=club.json()["id"])
    assert got.status_code == 204


@pytest.mark.skip("Create second user for this test")
def test_try_to_delete_foreign_club():
    pass
