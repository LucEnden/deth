import os
import random

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import poke_battle_sim as pb


# Data imports
package_dir = str(os.sep).join(str(pb.poke_sim.__file__).split(os.sep)[0:-1])
data_dir = os.path.join(package_dir, 'data')
abilities_df = pd.read_csv(os.path.join(data_dir, 'abilities.csv'))
items_df = pd.read_csv(os.path.join(data_dir, 'items_gen4.csv'))
moves_df = pd.read_csv(os.path.join(data_dir, 'move_list.csv'))
natures_df = pd.read_csv(os.path.join(data_dir, 'natures.csv'))
pokemon_stats_df = pd.read_csv(os.path.join(data_dir, 'pokemon_stats.csv'))
type_effectiveness_df = pd.read_csv(os.path.join(data_dir, 'type_effectiveness.csv'))


#region Data helper methods
def get_random_nature() -> str:
    return random.choice(natures_df.values)[0]

def get_stats_by_id(pokedex_id: int):
    if pokedex_id < min(pokemon_stats_df['ndex']) or pokedex_id > max(pokemon_stats_df['ndex']):
        raise ValueError(f'{pokedex_id} is not a valid pokedex id')
    
    return pb.PokeSim._pokemon_stats[pokedex_id - 1][4:10]

def get_stats_by_name(name: str):
    if name not in pokemon_stats_df['name'].values:
        raise ValueError(f'{name} is not a valid pokemon name')
    
    search_results = [ i for i in pb.PokeSim._pokemon_stats if i[1] == name ] # TODO make this search more time efficient
    if len(search_results) != 1:
        raise ValueError(f'Invalid search results: expected 1, got {len(search_results)} while searching for {name}')

    return search_results[0][4:10]

def get_ability_id_by_name(name: str):
    if name not in abilities_df['ability_name'].values:
        raise ValueError(f'{name} is not a valid starter ability')

    return abilities_df[abilities_df['ability_name'] == name]['ability_id'].values[0]
#endregion


#region Gender methods
gender_encoder = LabelEncoder()
gender_encoder.fit(pb.conf.global_settings.POSSIBLE_GENDERS)

def get_gender_encoding(gender: str):
    return gender_encoder.transform([gender])[0]

def get_gender_decoding(gender: int):
    return gender_encoder.inverse_transform([gender])[0]

def get_random_gender_mf():
    return random.choice(['male', 'female'])
#endregion


#region Type methods
type_encoder = LabelEncoder()
type_encoder.fit(pokemon_stats_df[[ 'type 1', 'type 2' ]].values.flatten())

def get_type_encoding(type_name: str | float):
    if isinstance(type_name, float) and np.isnan(type_name):
        return type_encoder.transform([np.nan])[0]
    
    if not type_name or type_name.lower() == 'none' or type_name.lower() == 'nan' or type_name == '':
        return type_encoder.transform([np.nan])[0]
    
    return type_encoder.transform([type_name])[0]

def get_type_decoding(type_id: int):
    return type_encoder.inverse_transform([type_id])[0]

def all_type_encodings():
    return np.array(type_encoder.transform(type_encoder.classes_))
#endregion


#region Stat methods
def get_random_ivs():
    return [ random.randint(0, 31) for _ in range(6) ]
#endregion