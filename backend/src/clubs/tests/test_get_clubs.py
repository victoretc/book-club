def test_get_clubs_as_anon(anon_clubs_api):
    anon_clubs_api.get_api_v1_clubs(page=1, page_size=10, search=None, membership=None)


def test_get_clubs(authenticated_clubs_api):
    authenticated_clubs_api.get_api_v1_clubs(page=1, page_size=1, search=None, membership=None)


def test_get_club_by_id(authenticated_clubs_api, club):
    authenticated_clubs_api.get_api_v1_clubs_id(id_=club.json()["id"])
