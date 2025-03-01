import random

import numpy as np
import gymnasium as gym
from typing import Optional
import poke_battle_sim as pb

from services.helper_methods import get_random_nature, get_stats_by_name, get_random_gender_mf, pokemon_stats_df, moves_df


starter_lvl = 5
starter_names = ['turtwig', 'chimchar', 'piplup']
starter_moves = {
    'turtwig': ['tackle', 'withdraw'],
    'chimchar': ['scratch', 'leer'],
    'piplup': ['pound', 'growl']
}
starter_abilities = {
    'turtwig': 'overgrow',
    'chimchar': 'blaze',
    'piplup': 'torrent'
}
starter_stats_df = pokemon_stats_df.copy()[pokemon_stats_df['name'].isin(starter_names)]
all_starter_moves = np.array(list(starter_moves.values())).flatten()
starter_move_df = moves_df[moves_df['identifier'].isin(all_starter_moves)]


def get_random_starter_name():
    return random.choice(starter_names)

def get_starter(name: str, nature: Optional[str] = None) -> pb.Pokemon:
    if name not in starter_names:
        raise ValueError(f'{name} is not a valid starter name')

    # stats = get_stats_by_name(name)

    starter = pb.Pokemon(
        name_or_id=name,
        level=starter_lvl,
        moves=starter_moves[name],
        gender=get_random_gender_mf(),
        ability=starter_abilities[name],
        nature=get_random_nature() if nature is None else nature,
        # cur_hp=stats[0],
        # stats_actual=stats
        ivs = [0, 0, 0, 0, 0, 0],
        evs = [0, 0, 0, 0, 0, 0],
    )
    starter.reset_stats()
    return starter


def get_random_starter(nature: Optional[str] = None):
    name = random.choice(starter_names)
    return get_starter(name, nature)


def get_rival_starter(agent_starter_name: str, nature: Optional[str] = None):
    name = ''
    if agent_starter_name == 'turtwig':
        name = 'chimchar'
    elif agent_starter_name == 'chimchar':
        name = 'piplup'
    elif agent_starter_name == 'piplup':
        name = 'turtwig'

    return get_starter(name, nature)