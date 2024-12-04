'''
    PM4Py – A Process Mining Library for Python
Copyright (C) 2024 Process Intelligence Solutions UG (haftungsbeschränkt)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see this software project's root or
visit <https://www.gnu.org/licenses/>.

Website: https://processintelligence.solutions
Contact: info@processintelligence.solutions
'''
from typing import Dict, Tuple


def apply(dfg: Dict[Tuple[str, str], int]) -> Dict[Tuple[str, str], float]:
    """
    Computes a causal graph based on a directly follows graph according to the heuristics miner

    Parameters
    ----------
    dfg: :class:`dict` directly follows relation, should be a dict of the form (activity,activity) -> num of occ.

    Returns
    -------
    :return: dictionary containing all causal relations as keys (with value inbetween -1 and 1 indicating that
    how strong it holds)
    """
    causal_heur = {}
    for (f, t) in dfg:
        if (f, t) not in causal_heur:
            rev = dfg[(t, f)] if (t, f) in dfg else 0
            causal_heur[(f, t)] = float((dfg[(f, t)] - rev) / (dfg[(f, t)] + rev + 1))
            causal_heur[(t, f)] = -1 * causal_heur[(f, t)]
    return causal_heur
