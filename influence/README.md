# Influence V2

Influence V2 is a character-first AI influencer platform. It lives in this
directory intentionally: the existing WSA build utility remains untouched.

## Run locally

```bash
docker compose -f influence/docker-compose.yml up --build
```

The API is available at `http://localhost:8000/docs` and the operator UI at
`http://localhost:3000`.

For a backend-only development environment, install `backend` dependencies and
run `uvicorn app.main:app --reload` from `influence/backend`.
