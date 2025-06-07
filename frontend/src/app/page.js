// Arquivo: frontend/src/app/page.js (VERSÃO FINAL COMPLETA)

"use client";

import { useState } from 'react';

export default function HomePage() {
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [username, setUsername] = useState('');
  const [searchedUser, setSearchedUser] = useState('');

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!username) {
        setError("Por favor, digite um nome de usuário.");
        return;
    }

    setLoading(true);
    setError(null);
    setRanking([]);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/top-artists/?user=${username}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'A resposta da rede não foi boa');
      }
      
      // Lendo a chave 'ranking' que o nosso backend agora envia
      setRanking(data.ranking);
      setSearchedUser(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="bg-gray-900 text-white min-h-screen p-4 sm:p-8">
      <div className="container mx-auto max-w-2xl">
        
        <h1 className="text-3xl sm:text-4xl font-bold text-center mb-2 text-green-400">
          Music Medals
        </h1>

        <p className="text-center text-gray-400 mb-8">
          Quadro de medalhas dos top 5 artistas de cada mês no último ano
        </p>

        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-2 mb-8">
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            placeholder="Digite seu usuário do Last.fm"
            className="flex-grow bg-gray-800 border border-gray-700 rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <button 
            type="submit"
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 sm:px-6 rounded-md disabled:bg-gray-500 transition-colors"
          >
            {loading ? 'Analisando...' : 'Analisar'}
          </button>
        </form>

        {error && <p className="text-red-500 text-center bg-red-900/50 p-3 rounded-md">{error}</p>}
        
        {ranking.length > 0 && (
          <div>
            <h2 className="text-xl sm:text-2xl font-semibold mb-4">
              Quadro de Medalhas de <span className="text-green-400">{searchedUser}</span>
            </h2>
            <ol className="space-y-3">
              {ranking.map((artist, index) => (
                <li key={artist.artist_name} className="bg-gray-800 p-4 rounded-lg flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 transition-all hover:bg-gray-700/50">
                  <span className="text-xl sm:text-2xl font-bold text-gray-500 w-10 text-left sm:text-center">{index + 1}</span>
                  <div className="flex-grow">
                    <a href={artist.url} target="_blank" rel="noopener noreferrer" className="text-lg font-semibold hover:underline">{artist.artist_name}</a>
                  </div>
                  <div className="flex items-center gap-3 text-lg self-end sm:self-center shrink-0">
                    {artist.pos_1 > 0 && <span title="1º lugar">🥇<span className="text-xs ml-1">{artist.pos_1}</span></span>}
                    {artist.pos_2 > 0 && <span title="2º lugar">🥈<span className="text-xs ml-1">{artist.pos_2}</span></span>}
                    {artist.pos_3 > 0 && <span title="3º lugar">🥉<span className="text-xs ml-1">{artist.pos_3}</span></span>}
                    {artist.pos_4 > 0 && <span title="4º lugar" className="text-gray-400">4º<span className="text-xs ml-1">x{artist.pos_4}</span></span>}
                    {artist.pos_5 > 0 && <span title="5º lugar" className="text-gray-500">5º<span className="text-xs ml-1">x{artist.pos_5}</span></span>}
                  </div>
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </main>
  );
}