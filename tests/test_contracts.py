"""G3: one explicit test per executable G2 case; all test data is synthetic.

API-034 and API-035 require an Update route absent from the pinned source,
so they are intentionally NOT implemented as passing or skipped tests.
"""

def payload(**changes):
    value = {"name": "Demo Widget", "category": "test", "quantity": 3}
    value.update(changes)
    return value


def create(api, **changes):
    response = api.post("/items", json=payload(**changes))
    assert response.status_code == 201, response.text
    return response.json()


def assert_validation(response):
    assert response.status_code == 422, response.text
    assert isinstance(response.json().get("detail"), list)


def test_api_001(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_002(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), dict)


def test_api_003(api_client):
    response = api_client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_api_004(api_client):
    ids = [create(api_client, name=f"Synthetic {n}")["id"] for n in range(22)]
    response = api_client.get("/items")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids[:20]


def test_api_005(api_client):
    for n in range(3):
        create(api_client, name=f"Synthetic {n}")
    response = api_client.get("/items?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_api_006(api_client):
    for n in range(3):
        create(api_client, name=f"Synthetic {n}")
    response = api_client.get("/items?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_api_007(api_client):
    assert_validation(api_client.get("/items?limit=0"))


def test_api_008(api_client):
    assert_validation(api_client.get("/items?limit=101"))


def test_api_009(api_client):
    assert_validation(api_client.get("/items?limit=abc"))


def test_api_010(api_client):
    response = api_client.post("/items", json=payload())
    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    for key, value in payload().items():
        assert body[key] == value


def test_api_011(api_client):
    response = api_client.post("/items", json=payload())
    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")
    assert set(response.json()) == {"id", "name", "category", "quantity"}


def test_api_012(api_client):
    item = create(api_client)
    response = api_client.get(f"/items/{item['id']}")
    assert response.status_code == 200
    assert response.json() == item


def test_api_013(api_client):
    item = create(api_client)
    response = api_client.get("/items")
    assert response.status_code == 200
    assert response.json() == [item]


def test_api_014(api_client):
    response = api_client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_api_015(api_client):
    assert_validation(api_client.get("/items/not-an-integer"))


def test_api_016(api_client):
    assert_validation(api_client.post("/items", json=payload(name="")))


def test_api_017(api_client):
    assert_validation(api_client.post("/items", json=payload(name="N" * 121)))


def test_api_018(api_client):
    assert_validation(api_client.post("/items", json=payload(category="")))


def test_api_019(api_client):
    assert_validation(api_client.post("/items", json=payload(category="C" * 61)))


def test_api_020(api_client):
    assert_validation(api_client.post("/items", json=payload(quantity=-1)))


def test_api_021(api_client):
    assert create(api_client, quantity=0)["quantity"] == 0


def test_api_022(api_client):
    assert create(api_client, quantity=1000000)["quantity"] == 1000000


def test_api_023(api_client):
    assert_validation(api_client.post("/items", json=payload(quantity=1000001)))


def test_api_024(api_client):
    data = payload()
    data.pop("category")
    assert_validation(api_client.post("/items", json=data))


def test_api_025(api_client):
    assert_validation(api_client.post("/items", json=payload(quantity="not-a-number")))


def test_api_026(api_client):
    response = api_client.post(
        "/items", content='{"name":', headers={"content-type": "application/json"}
    )
    assert_validation(response)


def test_api_027(api_client):
    item = create(api_client)
    response = api_client.delete(f"/items/{item['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_api_028(api_client):
    response = api_client.delete("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_api_029(api_client):
    item = create(api_client)
    url = f"/items/{item['id']}"
    assert api_client.delete(url).status_code == 204
    response = api_client.delete(url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_api_030(api_client):
    item = create(api_client)
    assert api_client.delete(f"/items/{item['id']}").status_code == 204
    response = api_client.get(f"/items/{item['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_api_031(api_client):
    ids = [create(api_client, name=f"Synthetic {n}")["id"] for n in range(3)]
    response = api_client.get("/items")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids
    assert ids == sorted(ids)


def test_api_032(isolated_client_factory):
    with isolated_client_factory() as first:
        assert first.get("/items").json() == []
        create(first)
        assert len(first.get("/items").json()) == 1
    with isolated_client_factory() as second:
        response = second.get("/items")
        assert response.status_code == 200
        assert response.json() == []


def test_api_033(api_client):
    response = api_client.post("/items", json=payload(name=""))
    assert_validation(response)
    first_issue = response.json()["detail"][0]
    assert isinstance(first_issue.get("loc"), list)
    assert "type" in first_issue
