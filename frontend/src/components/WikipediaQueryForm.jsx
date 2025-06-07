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
    <div id="root">
      <h1 className="text-2xl font-bold">Consulta Wikipedia con IA</h1>
  
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
        <div className="flex flex-col gap-1">
          <label className="font-medium" htmlFor="url">Link del artículo de Wikipedia (en inglés):</label>
          <textarea
            id="url"
            className="border rounded p-2 min-h-[80px]"
            value={wikiUrl}
            onChange={(e) => setWikiUrl(e.target.value)}
            required
            placeholder="https://en.wikipedia.org/wiki/Example"
          />
        </div>
  
        <div className="flex flex-col gap-1">
          <label className="font-medium" htmlFor="query">¿Qué quieres saber del artículo?</label>
          <textarea
            id="query"
            className="border rounded p-2 min-h-[80px]"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
            placeholder="Ej: ¿Quién fue el fundador?"
          />
        </div>
  
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
          disabled={loading}
        >
          {loading ? 'Consultando...' : 'Enviar'}
        </button>
      </form>
  
      {error && <p className="error mt-4">{error}</p>}
  
      {response && (
        <>
          <h2 className="font-semibold mt-6">Respuesta del modelo:</h2>
          <div className="response-box">{response}</div>
        </>
      )}
    </div>
  );
  
}
