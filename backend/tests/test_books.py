def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_book(client):
    res = client.post("/api/books", json={"title": "Dune", "author": "Frank Herbert"})
    assert res.status_code == 201
    body = res.json()
    assert body["id"] == 1
    assert body["status"] == "to-read"

def test_list_books(client):
    client.post("/api/books", json={"title": "A", "author": "X"})
    client.post("/api/books", json={"title": "B", "author": "Y"})
    res = client.get("/api/books")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_missing_book_returns_404(client):
    assert client.get("/api/books/999").status_code == 404


def test_update_book(client):
    book_id = client.post("/api/books", json={"title": "A", "author": "X"}).json()["id"]
    res = client.put(f"/api/books/{book_id}",
                     json={"title": "A", "author": "X", "status": "done", "rating": 5})
    assert res.status_code == 200
    assert res.json()["status"] == "done"
    assert res.json()["rating"] == 5


def test_delete_book(client):
    book_id = client.post("/api/books", json={"title": "A", "author": "X"}).json()["id"]
    assert client.delete(f"/api/books/{book_id}").status_code == 204
    assert client.get(f"/api/books/{book_id}").status_code == 404


def test_invalid_rating_returns_422(client):
    res = client.post("/api/books", json={"title": "A", "author": "X", "rating": 9})
    assert res.status_code == 422


def test_metrics_endpoint(client):
    client.get("/health")
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "http_requests_total" in res.text
