# Arquivo: core/views.py (VERSÃO FINAL OTIMIZADA COM CACHE E PARALELIZAÇÃO)

import os
from dotenv import load_dotenv
import pylast
from django.http import JsonResponse
from django.core.cache import cache

# Importações para lidar com datas, contagens e paralelização
import calendar
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
import concurrent.futures

load_dotenv()

def get_top_artists(request):
    lastfm_username = request.GET.get('user')
    if not lastfm_username:
        return JsonResponse({"error": "Nome de usuário não fornecido."}, status=400)

    # --- LÓGICA DE CACHE (INÍCIO) ---
    # 1. Cria uma "chave" única para este pedido no cache.
    cache_key = f"ranking_mensal_{lastfm_username.lower()}"
    
    # 2. Tenta pegar os dados a partir do cache.
    cached_data = cache.get(cache_key)
    
    # 3. Se os dados existirem no cache, retorna eles IMEDIATAMENTE!
    if cached_data:
        print(f"--- Cache HIT para o usuário: {lastfm_username} ---")
        return JsonResponse(cached_data)

    # 4. Se não houver cache (cache MISS), nós fazemos o trabalho pesado abaixo.
    print(f"--- Cache MISS para o usuário: {lastfm_username}. Calculando em paralelo... ---")
    
    try:
        # Configuração da API
        api_key = os.getenv("LASTFM_API_KEY")
        api_secret = os.getenv("LASTFM_SHARED_SECRET")
        network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
        user = network.get_user(lastfm_username)

        artists_medals = {}
        today = datetime.utcnow()

        # --- LÓGICA PARALELA ---

        # Função auxiliar que faz o trabalho para UM único mês.
        def fetch_and_process_month(month_index):
            try:
                target_month_date = today - relativedelta(months=month_index)
                
                first_day = target_month_date.replace(day=1, hour=0, minute=0, second=0)
                last_day_num = calendar.monthrange(target_month_date.year, target_month_date.month)[1]
                last_day = target_month_date.replace(day=last_day_num, hour=23, minute=59, second=59)

                time_from_ts = int(first_day.timestamp())
                time_to_ts = int(last_day.timestamp())
                
                # Chamada de API demorada usando o método correto
                scrobbles = user.get_recent_tracks(time_from=time_from_ts, time_to=time_to_ts, limit=None)
                
                if not scrobbles:
                    return []

                artist_names = [s.track.artist.name for s in scrobbles]
                top_5 = Counter(artist_names).most_common(5)
                return top_5
            except Exception as e:
                print(f"Erro ao processar o mês {month_index}: {e}")
                return []

        # Usamos o ThreadPoolExecutor para rodar a função 12 vezes em paralelo
        all_monthly_tops = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(fetch_and_process_month, range(12))
            all_monthly_tops = list(results)

        # Agora que temos TODOS os dados, processamos as medalhas
        for monthly_top_5 in all_monthly_tops:
            for position, (artist_name, playcount) in enumerate(monthly_top_5, 1):
                if artist_name not in artists_medals:
                    artist_url = "#" 
                    try:
                        artist_obj = pylast.Artist(artist_name, network)
                        artist_url = artist_obj.get_url()
                    except Exception:
                        pass # Ignora o erro se não conseguir pegar a URL
                    artists_medals[artist_name] = {
                        'artist_name': artist_name, 'url': artist_url, 
                        'pos_1': 0, 'pos_2': 0, 'pos_3': 0, 'pos_4': 0, 'pos_5': 0
                    }
                
                artists_medals[artist_name][f'pos_{position}'] += 1

        # Lógica de ordenação final
        final_ranking_list = list(artists_medals.values())
        sorted_ranking = sorted(
            final_ranking_list,
            key=lambda item: (
                -item['pos_1'], -item['pos_2'], -item['pos_3'], 
                -item['pos_4'], -item['pos_5'], item['artist_name'].lower()
            )
        )

        result_data = {"user": lastfm_username, "ranking": sorted_ranking}
        
        # --- LÓGICA DE CACHE (FIM) ---
        # 5. Salva o resultado no cache com validade de 24 horas.
        cache.set(cache_key, result_data, timeout=60*60*24)

        return JsonResponse(result_data)

    except pylast.WSError as e:
        if e.status == 6:
            return JsonResponse({"error": f"Usuário '{lastfm_username}' não encontrado."}, status=404)
        return JsonResponse({"error": str(e)}, status=500)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": "Um erro inesperado e complexo ocorreu no servidor."}, status=500)