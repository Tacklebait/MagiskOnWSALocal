# Influence V2 operator guide status

Run `docker compose -f influence/docker-compose.yml up --build`, then open the
API docs at `http://localhost:8000/docs`. Create a character, create and
activate a goal, create and activate an arc, then generate a daily chapter.
The Next.js page at `http://localhost:3000` is a minimal character-first
spectator entry point. Runtime flags are listed in `influence/.env.example`.
