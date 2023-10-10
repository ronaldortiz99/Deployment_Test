from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_teams():
    response = client.get("/teams/")
    assert response.status_code == 200
    expected = [
        {
            "name": "CV Vall D'Hebron",
            "country": "Spain",
            "description": None,
            "id": 1
        },
        {
            "name": "CE Sabadell",
            "country": "Spain",
            "description": None,
            "id": 2
        },
        {
            "name": "Club Juventut Les Corts",
            "country": "Spain",
            "description": None,
            "id": 3
        },
        {
            "name": "Volei Rubi",
            "country": "Spain",
            "description": None,
            "id": 4
        }
    ]
    assert response.json() == expected

def test_get_team():
    response = client.get("/team/CE%20Sabadell")
    assert response.status_code == 200
    expected = {
        "name": "CE Sabadell",
        "country": "Spain",
        "description": None,
        "id": 2
    }
    assert response.json() == expected

def test_post_team():
    data = {
        "name": "CV Vall D'Hebron2",
        "country": "Spain",
        "description": None
    }
    expected = {
        "name": "CV Vall D'Hebron2",
        "country": "Spain",
        "description": None,
        "id": 5
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post("/teams/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected


def test_put_team():
    data = {
        "name": "CV Vall D'Hebron2",
        "country": "Spain",
        "description": None
    }
    expected = {
        "name": "CV Vall D'Hebron2",
        "country": "Spain",
        "description": None,
        "id": 5
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.put("/teams/5", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

def test_delete_team():
    response = client.delete("/teams/5")
    assert response.status_code == 200
    assert response.json() == "El equipo ha sido eliminado de la base de datos."

def test_get_competitions():
    expected = [
    {
        "name": "Women's European Championship",
        "category": "Senior",
        "sport": "Volleyball",
        "id": 1,
        "teams": [
            {
                "name": "CV Vall D'Hebron",
                "country": "Spain",
                "description": None,
                "id": 1
            },
            {
                "name": "CE Sabadell",
                "country": "Spain",
                "description": None,
                "id": 2
            }
        ]
        },
        {
            "name": "1st Division League",
            "category": "Junior",
            "sport": "Football",
            "id": 2,
            "teams": [
                {
                    "name": "CV Vall D'Hebron",
                    "country": "Spain",
                    "description": None,
                    "id": 1
                }
            ]
        },
        {
            "name": "Women's Copa Catalunya",
            "category": "Senior",
            "sport": "Basketball",
            "id": 3,
            "teams": []
        },
        {
            "name": "1st Division League",
            "category": "Junior",
            "sport": "Futsal",
            "id": 4,
            "teams": []
        }
    ]
    response = client.get("/competitions/")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_competition_by_id():
    response = client.get("/competition/1")
    expected = {
        "name": "Women's European Championship",
        "category": "Senior",
        "sport": "Volleyball",
        "id": 1,
        "teams": [
            {
                "name": "CV Vall D'Hebron",
                "country": "Spain",
                "description": None,
                "id": 1
            },
            {
                "name": "CE Sabadell",
                "country": "Spain",
                "description": None,
                "id": 2
            }
        ]
        }
    assert response.status_code == 200
    assert response.json() == expected

def test_post_competition():
    data = {
        "name": "Women's European Championship2",
        "category": "Senior",
        "sport": "Volleyball"
    }
    expected = {
        'category': 'Senior',
         'id': 5,
         'name': "Women's European Championship2",
         'sport': 'Volleyball',
         'teams': []}
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post("/competitions/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

def test_put_competition():
    data = {
        "name": "Women's European Championship2",
        "category": "Senior",
        "sport": "Volleyball"
    }
    expected = {
        'category': 'Senior',
         'id': 5,
         'name': "Women's European Championship2",
         'sport': 'Volleyball',
         'teams': []
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.put("/competitions/5", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

def test_delete_competition():
    response = client.delete("/competitions/5")
    assert response.status_code == 200
    assert response.json() == "La competición ha sido eliminado de la base de datos."

def test_get_competitions_by_team():
    expected=[{'category': 'Senior',
  'id': 1,
  'name': "Women's European Championship",
  'sport': 'Volleyball',
  'teams': [{'country': 'Spain',
             'description': None,
             'id': 1,
             'name': "CV Vall D'Hebron"},
            {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}]},
 {'category': 'Junior',
  'id': 2,
  'name': '1st Division League',
  'sport': 'Football',
  'teams': [{'country': 'Spain',
             'description': None,
             'id': 1,
             'name': "CV Vall D'Hebron"}]}]
    response = client.get("/teams/CV%20Vall%20D'Hebron/competitions")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_teams_from_competition():
    expected = [{'country': 'Spain', 'description': None, 'id': 1, 'name': "CV Vall D'Hebron"},
 {'country': 'Spain', 'description': None, 'id': 2, 'name': 'CE Sabadell'}]
    response = client.get("/competitions/1/teams")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_match():
    expected = [{'competition': {'category': 'Senior',
                  'id': 1,
                  'name': "Women's European Championship",
                  'sport': 'Volleyball',
                  'teams': [{'country': 'Spain',
                             'description': None,
                             'id': 1,
                             'name': "CV Vall D'Hebron"},
                            {'country': 'Spain',
                             'description': None,
                             'id': 2,
                             'name': 'CE Sabadell'}]},
  'date': '2023-05-01T10:30:00',
  'id': 1,
  'local': {'country': 'Spain',
            'description': None,
            'id': 1,
            'name': "CV Vall D'Hebron"},
  'price': 9.85,
  'visitor': {'country': 'Spain',
              'description': None,
              'id': 2,
              'name': 'CE Sabadell'}},
 {'competition': {'category': 'Senior',
                  'id': 1,
                  'name': "Women's European Championship",
                  'sport': 'Volleyball',
                  'teams': [{'country': 'Spain',
                             'description': None,
                             'id': 1,
                             'name': "CV Vall D'Hebron"},
                            {'country': 'Spain',
                             'description': None,
                             'id': 2,
                             'name': 'CE Sabadell'}]},
  'date': '2023-05-02T10:30:00',
  'id': 2,
  'local': {'country': 'Spain',
            'description': None,
            'id': 1,
            'name': "CV Vall D'Hebron"},
  'price': 9.85,
  'visitor': {'country': 'Spain',
              'description': None,
              'id': 2,
              'name': 'CE Sabadell'}}]
    response = client.get("/matches/")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_match_by_id():
    response = client.get("/match/1")
    expected = {'competition': {'category': 'Senior',
                 'id': 1,
                 'name': "Women's European Championship",
                 'sport': 'Volleyball',
                 'teams': [{'country': 'Spain',
                            'description': None,
                            'id': 1,
                            'name': "CV Vall D'Hebron"},
                           {'country': 'Spain',
                            'description': None,
                            'id': 2,
                            'name': 'CE Sabadell'}]},
 'date': '2023-05-01T10:30:00',
 'id': 1,
 'local': {'country': 'Spain',
           'description': None,
           'id': 1,
           'name': "CV Vall D'Hebron"},
 'price': 9.85,
 'visitor': {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}}
    assert response.status_code == 200
    assert response.json() == expected

def test_post_match():
    data = {'competition': {'category': 'Senior',
                 'id': 1,
                 'name': "Women's European Championship",
                 'sport': 'Volleyball',
                 'teams': [{'country': 'Spain',
                            'description': None,
                            'id': 1,
                            'name': "CV Vall D'Hebron"},
                           {'country': 'Spain',
                            'description': None,
                            'id': 2,
                            'name': 'CE Sabadell'}]},
 'date': '2023-04-01T10:30:00',
 'id': 1,
 'local': {'country': 'Spain',
           'description': None,
           'id': 1,
           'name': "CV Vall D'Hebron"},
 'price': 9.85,
 'visitor': {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}}
    expected = {'competition': {'category': 'Senior',
                 'id': 1,
                 'name': "Women's European Championship",
                 'sport': 'Volleyball',
                 'teams': [{'country': 'Spain',
                            'description': None,
                            'id': 1,
                            'name': "CV Vall D'Hebron"},
                           {'country': 'Spain',
                            'description': None,
                            'id': 2,
                            'name': 'CE Sabadell'}]},
 'date': '2023-04-01T10:30:00',
 'id': 3,
 'local': {'country': 'Spain',
           'description': None,
           'id': 1,
           'name': "CV Vall D'Hebron"},
 'price': 9.85,
 'visitor': {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}}
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post("/matches/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

def test_put_match():
    data = {'competition': {'category': 'Senior',
                 'id': 1,
                 'name': "Women's European Championship",
                 'sport': 'Volleyball',
                 'teams': [{'country': 'Spain',
                            'description': None,
                            'id': 1,
                            'name': "CV Vall D'Hebron"},
                           {'country': 'Spain',
                            'description': None,
                            'id': 2,
                            'name': 'CE Sabadell'}]},
 'date': '2023-04-01T10:30:00',
 'id': 1,
 'local': {'country': 'Spain',
           'description': None,
           'id': 1,
           'name': "CV Vall D'Hebron"},
 'price': 9.85,
 'visitor': {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}}
    expected = {'competition': {'category': 'Senior',
                 'id': 1,
                 'name': "Women's European Championship",
                 'sport': 'Volleyball',
                 'teams': [{'country': 'Spain',
                            'description': None,
                            'id': 1,
                            'name': "CV Vall D'Hebron"},
                           {'country': 'Spain',
                            'description': None,
                            'id': 2,
                            'name': 'CE Sabadell'}]},
 'date': '2023-04-01T10:30:00',
 'id': 3,
 'local': {'country': 'Spain',
           'description': None,
           'id': 1,
           'name': "CV Vall D'Hebron"},
 'price': 9.85,
 'visitor': {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}}
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.put("/matches/3", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

def test_delete_match():
    response = client.delete("/matches/3")
    assert response.status_code == 200
    assert response.json() == "El partido ha sido eliminado de la base de datos."

def test_get_matches_by_team():
    expected = [{'competition_id': 1,
  'date': '2023-05-01T10:30:00',
  'id': 1,
  'local_id': 1,
  'price': 9.85,
  'visitor_id': 2},
 {'competition_id': 1,
  'date': '2023-05-02T10:30:00',
  'id': 2,
  'local_id': 1,
  'price': 9.85,
  'visitor_id': 2}]
    response = client.get("/teams/CV%20Vall%20D'Hebron/matches")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_matches_by_competition():
    expected = [{'competition_id': 1,
  'date': '2023-05-01T10:30:00',
  'id': 1,
  'local_id': 1,
  'price': 9.85,
  'visitor_id': 2},
 {'competition_id': 1,
  'date': '2023-05-02T10:30:00',
  'id': 2,
  'local_id': 1,
  'price': 9.85,
  'visitor_id': 2}]
    response = client.get("/competitions/Women's%20European%20Championship/matches")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_teams_by_match_id():
    expected = {'local': {'country': 'Spain',
           'description': None,
           'id': 1,
           'name': "CV Vall D'Hebron"},
 'visitor': {'country': 'Spain',
             'description': None,
             'id': 2,
             'name': 'CE Sabadell'}}
    response = client.get("/matches/1/teams")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_competition_by_match_id():
    expected = {'category': 'Senior',
 'id': 1,
 'name': "Women's European Championship",
 'sport': 'Volleyball'}
    response = client.get("/matches/1/competition")
    assert response.status_code == 200
    assert response.json() == expected