from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_goal_arc_and_idempotent_daily_chapter():
    character = client.post("/characters", json={"name": "Mira Vale", "bio": "A ceramic artist."}).json()
    goal = client.post(f"/characters/{character['id']}/goals", json={"title": "Launch a studio collection", "category": "creative"}).json()
    assert client.post(f"/goals/{goal['id']}/status/active").status_code == 200
    arc = client.post(f"/characters/{character['id']}/arcs", json={"title": "First collection", "premise": "Mira prepares her work.", "primary_goal_id": goal["id"]}).json()
    assert client.post(f"/arcs/{arc['id']}/status/active").status_code == 200
    first = client.post(f"/arcs/{arc['id']}/daily-chapter", json={"date": "2026-07-22"})
    second = client.post(f"/arcs/{arc['id']}/daily-chapter", json={"date": "2026-07-22"})
    assert first.status_code == 200 and first.json()[0]["id"] == second.json()[0]["id"]
    assert client.get(f"/characters/{character['id']}/narrative-state").json()["active_arcs"][0]["id"] == arc["id"]
