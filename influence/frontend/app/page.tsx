type Character = { id: number; name: string; bio: string };

async function getCharacters(): Promise<Character[]> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://api:8000"}/characters`, { cache: "no-store" });
  return response.ok ? response.json() : [];
}

export default async function Home() {
  const characters = await getCharacters();
  return <main><h1>Influence</h1><p>Character-first, persistent narrative lives.</p><h2>Characters</h2>{characters.length ? <ul>{characters.map((character) => <li key={character.id}><strong>{character.name}</strong> — {character.bio || "No public bio yet."}</li>)}</ul> : <p>No characters yet. Create one through the operator API at <code>/docs</code>.</p>}</main>;
}
