import csv

def parse_map_data(file_path):
    """
    Lê um arquivo de mapa CSV e extrai o grid e os pontos de interesse.
    
    Args:
        file_path (str): Caminho para o arquivo CSV do mapa
        
    Returns:
        tuple: (grid, locations) onde grid é uma matriz 2D de tipos de terreno
               e locations é um dicionário com posições dos pontos especiais
               
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se o arquivo estiver malformado
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo de mapa não encontrado: {file_path}")
    
    grid = []
    locations = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                if not row:  # Pula linhas vazias
                    continue
                    
                grid_row = []
                for c, cell in enumerate(row):
                    cell_content = cell.strip()
                    terrain_type = LEGEND.get(cell_content, 6)
                    grid_row.append(terrain_type)
                    
                    if cell_content in ['L', 'MS', 'E', 'P', 'MA', 'LW']:
                        key = cell_content
                        if key not in locations:
                            locations[key] = []
                        locations[key].append((r, c))

                grid.append(grid_row)
                
        if not grid:
            raise ValueError(f"Arquivo de mapa vazio: {file_path}")
            
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Erro ao processar arquivo de mapa {file_path}: {str(e)}")
            
    return grid, locations

# --- Legenda de Terrenos e Custos ---
LEGEND = {
    'G': 0, 'S': 1, 'F': 2, 'M': 3, 'A': 4,
    '': 5, 'X': 6,
    'L': 0, 'MS': 0, 'MA': 0, 'LW': 2,
    'E': 5, 'P': 5
}

TERRAIN_COSTS = {
    0: 10, 1: 20, 2: 100, 3: 150, 4: 180,
    5: 10,
    6: float('inf')
}

# --- Carregando Mapas e Localizações ---
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(BASE_DIR, 'maps')

HYRULE_MAP_PATH = os.path.join(MAPS_DIR, 'hyrule_map.csv')
DUNGEON_1_MAP_PATH = os.path.join(MAPS_DIR, 'dungeon1_map.csv')
DUNGEON_2_MAP_PATH = os.path.join(MAPS_DIR, 'dungeon2_map.csv')
DUNGEON_3_MAP_PATH = os.path.join(MAPS_DIR, 'dungeon3_map.csv')

try:
    HYRULE_MAP, hyrule_locations = parse_map_data(HYRULE_MAP_PATH)
    DUNGEON_1_MAP, dungeon_1_locations = parse_map_data(DUNGEON_1_MAP_PATH)
    DUNGEON_2_MAP, dungeon_2_locations = parse_map_data(DUNGEON_2_MAP_PATH)
    DUNGEON_3_MAP, dungeon_3_locations = parse_map_data(DUNGEON_3_MAP_PATH)
except (FileNotFoundError, ValueError) as e:
    print(f"Erro ao carregar mapas: {e}")
    print("Verifique se os arquivos de mapa estão presentes no diretório 'maps/'")
    raise

DUNGEON_MAPS = {
    "dungeon1": DUNGEON_1_MAP,
    "dungeon2": DUNGEON_2_MAP,
    "dungeon3": DUNGEON_3_MAP,
}

# --- Pontos de Interesse (Coordenadas [linha, coluna]) ---
START_POS = hyrule_locations.get('L', [(-1, -1)])[0]
LOST_WOODS_POS = hyrule_locations.get('LW', [(-1,-1)])[0]

# DUNGEON_ENTRANCES: Localizações em Hyrule onde Link entra em uma masmorra (marcado como 'MA' em hyrule_map.csv).
# Estes são os pontos no mapa do mundo.
dungeon_entrances_coords = sorted(hyrule_locations.get('MA', []))
DUNGEON_ENTRANCES = {f"dungeon{i+1}": pos for i, pos in enumerate(dungeon_entrances_coords)}

# DUNGEON_PORTALS: Localizações *dentro* de cada masmorra onde Link aparece ao entrar
# e de onde ele sai de volta para Hyrule (marcado como 'E' nos mapas das masmorras).
DUNGEON_PORTALS = {
    "dungeon1": dungeon_1_locations.get('E', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('E', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('E', [(-1,-1)])[0],
}

PENDANT_LOCATIONS = {
    "dungeon1": dungeon_1_locations.get('P', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('P', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('P', [(-1,-1)])[0],
}
