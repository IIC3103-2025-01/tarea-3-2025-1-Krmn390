import { useState } from 'react';

export default function WikipediaQueryForm() {
  const [wikiUrl, setWikiUrl] = useState('');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: wikiUrl, question: query }),
      });

      if (!res.ok) {
        throw new Error('Error al consultar el backend.');
      }

      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResponse(data.result);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Consulta Wikipedia con IA</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium">Link del artículo de Wikipedia (en inglés):</label>
          <input
            type="url"
            className="w-full border rounded p-2"
            value={wikiUrl}
            onChange={(e) => setWikiUrl(e.target.value)}
            required
            placeholder="https://en.wikipedia.org/wiki/Example"
          />
        </div>
        <div>
          <label className="block font-medium">¿Qué quieres saber del artículo?</label>
          <input
            type="text"
            className="w-full border rounded p-2"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
            placeholder="Ej: ¿Quién fue el fundador?"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? 'Consultando...' : 'Enviar'}
        </button>
      </form>

      {error && <p className="text-red-600 mt-4">{error}</p>}
      {response && (
        <div className="mt-6 p-4 border rounded bg-gray-100">
          <h2 className="font-semibold mb-2">Respuesta del modelo:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}