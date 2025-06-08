# Arquivo: core/views.py (VERSÃO DEFINITIVA COM ANÁLISE MENSAL PARA TUDO)

import os
from dotenv import load_dotenv
import pylast
from django.http import JsonResponse
from django.core.cache import cache

import calendar
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
import concurrent.futures

load_dotenv()

def get_top_artists(request):
    lastfm_username = request.GET.get('user')
    ranking_type = request.GET.get('type', 'artists') 

    if not lastfm_username:
        return JsonResponse({"error": "Nome de usuário não fornecido."}, status=400)

    cache_key = f"ranking_{ranking_type}_{lastfm_username.lower()}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print(f"--- Cache HIT para: {lastfm_username} (tipo: {ranking_type}) ---")
        return JsonResponse(cached_data)

    print(f"--- Cache MISS para: {lastfm_username} (tipo: {ranking_type}). Calculando... ---")
    
    try:
        api_key = os.getenv("LASTFM_API_KEY")
        api_secret = os.getenv("LASTFM_SHARED_SECRET")
        network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
        user = network.get_user(lastfm_username)

        artists_medals = {}
        today = datetime.utcnow()

        # --- LÓGICA UNIFICADA E PARALELA ---

        # Esta função agora sabe como contar artistas, álbuns ou músicas
        def fetch_and_process_month(month_index):
            try:
                target_month_date = today - relativedelta(months=month_index)
                first_day = target_month_date.replace(day=1, hour=0, minute=0, second=0)
                last_day_num = calendar.monthrange(target_month_date.year, target_month_date.month)[1]
                last_day = target_month_date.replace(day=last_day_num, hour=23, minute=59, second=59)
                time_from_ts, time_to_ts = int(first_day.timestamp()), int(last_day.timestamp())
                
                scrobbles = user.get_recent_tracks(time_from=time_from_ts, time_to=time_to_ts, limit=None)
                if not scrobbles: return []

                # Lógica condicional para decidir O QUE contar
                if ranking_type == 'artists':
                    items_to_count = [s.track.artist.name for s in scrobbles]
                elif ranking_type == 'albums':
                    # Usamos f-string para criar um identificador único "Artista - Álbum"
                    # O 'if s.album' protege contra scrobbles sem dados de álbum
                    items_to_count = [f"{s.track.artist.name} - {s.album}" for s in scrobbles if s.album]
                elif ranking_type == 'tracks':
                    items_to_count = [f"{s.track.artist.name} - {s.track.title}" for s in scrobbles]
                else:
                    return []
                
                return Counter(items_to_count).most_common(5)
            except Exception as e:
                print(f"Erro ao processar o mês {month_index} para {ranking_type}: {e}")
                return []

        # O executor continua o mesmo, rodando nossa nova função flexível
        with concurrent.futures.ThreadPoolExecutor() as executor:
            all_monthly_tops = list(executor.map(fetch_and_process_month, range(12)))

        # Processamento de medalhas agora também é flexível
        for monthly_top_5 in all_monthly_tops:
            for position, (item_identifier, playcount) in enumerate(monthly_top_5, 1):
                if item_identifier not in artists_medals:
                    # Lógica para obter nome, artista e URL dependendo do tipo
                    url = "#"
                    try:
                        if ranking_type == 'artists':
                            name = item_identifier
                            artist = None
                            url = pylast.Artist(name, network).get_url()
                        else: # Para Álbuns e Músicas
                            artist_str, name_str = item_identifier.split(' - ', 1)
                            name = name_str
                            artist = artist_str
                            if ranking_type == 'albums':
                                url = pylast.Album(artist, name, network).get_url()
                            elif ranking_type == 'tracks':
                                url = pylast.Track(artist, name, network).get_url()
                    except Exception as e:
                        print(f"AVISO: Não foi possível obter URL para '{item_identifier}'. Erro: {e}")

                    artists_medals[item_identifier] = {
                        'name': name, 'url': url, 'artist': artist,
                        'pos_1': 0, 'pos_2': 0, 'pos_3': 0, 'pos_4': 0, 'pos_5': 0
                    }
                
                artists_medals[item_identifier][f'pos_{position}'] += 1
        
        final_ranking_list = list(artists_medals.values())
        sorted_ranking = sorted(final_ranking_list, key=lambda item: (-item['pos_1'], -item['pos_2'], -item['pos_3'], -item['pos_4'], -item['pos_5'], item['name'].lower()))

        result_data = {"user": lastfm_username, "ranking": sorted_ranking, "type": ranking_type}
        cache.set(cache_key, result_data, timeout=60*60*24)
        return JsonResponse(result_data)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": "Um erro inesperado e complexo ocorreu no servidor."}, status=500)