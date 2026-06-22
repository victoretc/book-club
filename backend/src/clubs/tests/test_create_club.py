import pytest

from clients.http.book_club import ClubsApi
from clients.http.book_club.models.api_models import PatchedClub


def test_create_club(authenticated_clubs_api, club, user):
    got = authenticated_clubs_api.get_api_v1_clubs_id(id_=club.json()["id"])
    assert got.book_title == club.json()["bookTitle"]
    assert got.id == club.json()["id"]
    assert len(got.members) == 1
    assert got.owner == user["id"]


def test_create_club_with_existing_name(authenticated_clubs_api: ClubsApi, club_request_data):
    authenticated_clubs_api.post_api_v1_clubs_with_http_info(PatchedClub(**club_request_data))  # type: ignore[arg-type]
    got = authenticated_clubs_api.post_api_v1_clubs_with_http_info(PatchedClub(**club_request_data))  # type: ignore[arg-type]
    assert got.status_code == 400
    assert got.json() == {"bookTitle": ["Book Club with this Book Title already exists."]}


def test_try_to_join_to_your_own_club(club, authenticated_clubs_api):
    got = authenticated_clubs_api.post_api_v1_clubs_id__members_me_with_http_info(id_=club.json()["id"])
    assert got.status_code == 400
    assert got.json() == {"detail": "User is already a member of this club."}


def test_try_to_leave_from_your_own_club(club, authenticated_clubs_api):
    got = authenticated_clubs_api.delete_api_v1_clubs_id__members_me_with_http_info(id_=club.json()["id"])
    assert got.status_code == 400
    assert got.json() == {"detail": "Club owner cannot leave the club."}


@pytest.mark.skip("Create second user for this test")
def test_try_to_leave_from_foreign_club(club, authenticated_clubs_api):
    got = authenticated_clubs_api.delete_api_v1_clubs_id__members_me_with_http_info(id_=club.json()["id"])
    assert got.status_code == 400
    assert got.json() == {"detail": "User is not a member of this club."}


@pytest.mark.skip("Create second user for this test")
def test_join_to_club():
    pass
