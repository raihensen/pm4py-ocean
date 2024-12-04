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

from pm4py.objects.ocel.obj import OCEL
from typing import Optional, Dict, Any


def apply(ocel: OCEL, parameters: Optional[Dict[Any, Any]] = None) -> OCEL:
    """
    Forces the consistency of the OCEL, ensuring that the event/object identifier,
    event/object type are of type string and non-empty.

    Parameters
    --------------
    ocel
        OCEL
    parameters
        Possible parameters of the method

    Returns
    --------------
    ocel
        Consistent OCEL
    """
    if parameters is None:
        parameters = {}

    fields = {
        "events": ["ocel:eid", "ocel:activity"],
        "objects": ["ocel:oid", "ocel:type"],
        "relations": ["ocel:eid", "ocel:oid", "ocel:activity", "ocel:type"],
        "o2o": ["ocel:oid", "ocel:oid_2"],
        "e2e": ["ocel:eid", "ocel:eid_2"],
        "object_changes": ["ocel:oid", "ocel:type"]
    }

    for tab, tfields in fields.items():
        df = getattr(ocel, tab)
        df[tfields] = df[tfields].astype("string")
        # df[tfields] = df[tfields].replace("", pd.NA)
        df = df.dropna(subset=tfields, how="any")
        filter = True
        for fie in tfields:
            filter = filter & (df[fie].str.len() > 0)
        if filter is not True:
            df = df[filter]
        setattr(ocel, tab, df)

    return ocel
