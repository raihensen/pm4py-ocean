from itertools import product

import pm4py
from pm4py.objects.log.obj import EventLog
from pm4py.algo.discovery.inductive.variants.im_clean import utils


def detect(alphabet, transitive_predecessors, transitive_successors):
    '''
    This method finds a xor cut in the dfg.
    Implementation follows function XorCut on page 188 of
    "Robust Process Mining with Guarantees" by Sander J.J. Leemans (ISBN: 978-90-386-4257-4)

    Basic Steps:
    1. create a group per activity
    2. merge pairwise reachable nodes (based on transitive relations)
    3. merge pairwise unreachable nodes (based on transitive relations)
    4. sort the groups based on their reachability
    
    Parameters
    ----------
    alphabet
        characters occurring in the dfg
    transitive_predecessors
        dictionary mapping activities to their (transitive) predecessors, according to the DFG
    transitive_successors
        dictionary mapping activities to their (transitive) successors, according to the DFG

    Returns
    -------
        A list of sets of activities, i.e., forming a maximal sequence cut
        None if no cut is found.

    '''
    groups = [{a} for a in alphabet]
    if len(groups) == 0:
        return None
    for a, b in product(alphabet, alphabet):
        if (b in transitive_successors[a] and a in transitive_successors[b]) or (
                b not in transitive_successors[a] and a not in transitive_successors[b]):
            groups = utils.__merge_groups_for_acts(a, b, groups)

    groups = list(sorted(groups, key=lambda g: len(
        transitive_predecessors[next(iter(g))]) + (len(alphabet) - len(transitive_successors[next(iter(g))]))))
    return groups if len(groups) > 1 else None





def project(log, groups, activity_key):
    '''
    This method projects the log based on a presumed sequence cut and a list of activity groups
    Parameters
    ----------
    log
        original log
    groups
        list of activity sets to be used in projection (activities can only appear in one group)
    activity_key
        key to use in the event to derive the activity name

    Returns
    -------
        list of corresponding logs according to the sequence cut.
    '''
    # currently, not 'noise' proof
    logs = list()
    for group in groups:
        proj = EventLog()
        for t in log:
            proj.append(pm4py.filter_trace(lambda e: e[activity_key] in group, t))
        logs.append(proj)
    return logs


def _is_strict_subset(A, B):
    return A != B and A.issubset(B)


def _is_strict_superset(A, B):
    return A != B and A.issuperset(B)
