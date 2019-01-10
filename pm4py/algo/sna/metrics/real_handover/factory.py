from pm4py.algo.sna.metrics.real_handover.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(mco, parameters=None, variant=CLASSIC):
    """
    Calculate the Real Handover of Work metric

    Parameters
    ------------
    mco
        Matrix container object
    parameters
        Parameters of the algorithm
    variant
        Variant of the algorithm: classic
    """
    return VERSIONS[CLASSIC].apply(mco, parameters=parameters)
