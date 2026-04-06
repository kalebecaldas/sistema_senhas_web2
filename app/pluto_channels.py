# app/pluto_channels.py
"""
Canais Pluto TV disponíveis no Brasil
URLs obtidas da API pública da Pluto TV
"""

PLUTO_CHANNELS = {
    # Notícias
    '5f5a7b6d14a1af00074576a0': {
        'name': 'Pluto TV Notícias',
        'category': 'Notícias',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f5a7b6d14a1af00074576a0/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    '5f5132e3b66c76000790ef27': {
        'name': 'CNN Brasil',
        'category': 'Notícias',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f5132e3b66c76000790ef27/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    
    # Filmes
    '5f120f41b7d403000783a6d6': {
        'name': 'Pluto TV Cine Ação',
        'category': 'Filmes',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f120f41b7d403000783a6d6/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    '5f120f5a546d770007a39f1f': {
        'name': 'Pluto TV Cine Suspense',
        'category': 'Filmes',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f120f5a546d770007a39f1f/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    '5f120f6b140bcf00077a2e4f': {
        'name': 'Pluto TV Cine Drama',
        'category': 'Filmes',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f120f6b140bcf00077a2e4f/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    
    # Séries
    '5f121460b73ac6000719fbaf': {
        'name': 'Pluto TV Séries',
        'category': 'Séries',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f121460b73ac6000719fbaf/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    
    # Música
    '5f5a545d0dbf7f0007c09408': {
        'name': 'MTV Pluto TV',
        'category': 'Música',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f5a545d0dbf7f0007c09408/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    
    # Entretenimento
    '5f120f0b140bcf00077a2e63': {
        'name': 'Pluto TV Comédia',
        'category': 'Entretenimento',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f120f0b140bcf00077a2e63/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    
    # Documentários
    '5f1214a637c6fd00079c652f': {
        'name': 'Pluto TV Documentários',
        'category': 'Documentários',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f1214a637c6fd00079c652f/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
    
    # Infantil
    '5f121262a189a800076b9386': {
        'name': 'Pluto TV Kids',
        'category': 'Infantil',
        'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f121262a189a800076b9386/master.m3u8?deviceType=web&deviceMake=web&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceLat=0&deviceLon=0&deviceDNT=0&deviceId=channel&sid=1'
    },
}

def get_channel_by_id(channel_id):
    """Retorna informações do canal pelo ID"""
    return PLUTO_CHANNELS.get(channel_id)

def get_channels_by_category(category):
    """Retorna todos os canais de uma categoria"""
    return {
        cid: info for cid, info in PLUTO_CHANNELS.items()
        if info['category'] == category
    }

def get_all_categories():
    """Retorna lista de todas as categorias"""
    return list(set(info['category'] for info in PLUTO_CHANNELS.values()))
