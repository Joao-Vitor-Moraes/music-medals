// Arquivo: frontend/src/app/page.js (VERSÃO COM ABAS DE SELEÇÃO)

"use client";

import { useState } from 'react';

// NOVO: Componente para as abas de seleção
const RankingTabs = ({ selected, onSelect }) => {
  const tabs = [
    { key: 'artists', label: 'Artistas' },
    { key: 'albums', label: 'Álbuns' },
    { key: 'tracks', label: 'Músicas' },
  ];

  return (
    <div className="flex justify-center border-b border-gray-700 mb-6">
      {tabs.map(tab => (
        <button
          key={tab.key}
          onClick={() => onSelect(tab.key)}
          className={`px-4 py-3 font-semibold transition-colors ${
            selected === tab.key
              ? 'text-white border-b-2 border-red-500' // Estilo da aba ativa
              : 'text-gray-400 hover:text-white' // Estilo da aba inativa
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
};


export default function HomePage() {
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [username, setUsername] = useState('');
  const [searchedUser, setSearchedUser] = useState('');
  
  // NOVO: Estado para controlar o tipo de ranking selecionado
  const [rankingType, setRankingType] = useState('artists');

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
      // Adicionamos o 'rankingType' à URL da API
      const response = await fetch(`http://127.0.0.1:8000/api/top-artists/?user=${username}&type=${rankingType}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'A resposta da rede não foi boa');
      }
      
      setRanking(data.ranking);
      setSearchedUser(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="bg-gray-900 text-gray-300 min-h-screen p-4 sm:p-8">
      <div className="container mx-auto max-w-2xl">
        
        <h1 className="text-3xl sm:text-4xl font-bold text-center mb-2 text-white">
          Music Medals
        </h1>
        <p className="text-center text-gray-400 mb-8">
          Quadro de medalhas dos top 5 artistas, álbuns e músicas de cada mês no último ano
        </p>

        {/* Adicionamos o componente de abas aqui */}
        <RankingTabs selected={rankingType} onSelect={setRankingType} />

        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-2 mb-8">
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            placeholder="Digite seu usuário do Last.fm"
            className="flex-grow bg-gray-800 border border-gray-700 rounded-md p-3 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
          />
          <button 
            type="submit"
            disabled={loading}
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 sm:px-6 rounded-md disabled:bg-gray-600 transition-colors"
          >
            {loading ? 'Analisando...' : 'Analisar'}
          </button>
        </form>

        {error && <p className="text-red-400 text-center bg-red-900/50 p-3 rounded-md border border-red-800">{error}</p>}
        
        {ranking.length > 0 && (
          <div>
            <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-white">
              Quadro de Medalhas de <span className="text-red-500">{searchedUser}</span>
            </h2>
            <ol className="space-y-2">
              {ranking.map((item, index) => (
                <li key={item.name + item.artist} className="bg-gray-800 p-4 rounded-lg flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 transition-all hover:bg-gray-700/50">
                  <span className="text-xl sm:text-2xl font-bold text-gray-500 w-10 text-left sm:text-center">{index + 1}</span>
                  <div className="flex-grow">
                    {/* NOVO: Lógica para exibir o nome e o artista (se houver) */}
                    <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-lg font-semibold text-white hover:text-red-500 hover:underline">{item.name}</a>
                    {item.artist && <p className="text-sm text-gray-400">{item.artist}</p>}
                  </div>
                  <div className="flex items-center gap-3 text-lg self-end sm:self-center shrink-0">
                    {item.pos_1 > 0 && <span title="1º lugar">🥇<span className="text-xs ml-1">{item.pos_1}</span></span>}
                    {item.pos_2 > 0 && <span title="2º lugar">🥈<span className="text-xs ml-1">{item.pos_2}</span></span>}
                    {item.pos_3 > 0 && <span title="3º lugar">🥉<span className="text-xs ml-1">{item.pos_3}</span></span>}
                    {item.pos_4 > 0 && <span title="4º lugar" className="text-gray-400">4º<span className="text-xs ml-1">x{item.pos_4}</span></span>}
                    {item.pos_5 > 0 && <span title="5º lugar" className="text-gray-500">5º<span className="text-xs ml-1">x{item.pos_5}</span></span>}
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