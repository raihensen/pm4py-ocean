from scipy.cluster.hierarchy import to_tree, linkage
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.clustering.hierarchical_attribute_based.merge_log import merge_log
from pm4py.algo.clustering.hierarchical_attribute_based.util import evaluation

VARIANT_DMM_LEVEN = "variant_DMM_leven"
VARIANT_AVG_LEVEN = "variant_avg_leven"
VARIANT_DMM_VEC = "variant_DMM_vec"
VARIANT_AVG_VEC = "variant_avg_vec"
DFG = 'dfg'


VERSION_METHODS = {VARIANT_DMM_LEVEN: evaluation.eval_DMM_leven, VARIANT_AVG_LEVEN: evaluation.eval_avg_leven,
                   VARIANT_DMM_VEC: evaluation.eval_DMM_variant, VARIANT_AVG_VEC: evaluation.eval_avg_variant,
                   DFG: evaluation.dfg_dis}


def bfs(tree):
    queue = []
    output = []
    queue.append(tree)
    while queue:
        # element in queue is waiting to become root and splited into child
        # root is the first ele of queue
        root = queue.pop(0)
        if len(root['children']) > 0:
            name = [root['name']]
            for child in root['children']:
                queue.append(child)
                name.append(child['name'])
            output.append(name)

    return output


def apply(log, variant=VARIANT_DMM_LEVEN, parameters=None):
    if parameters is None:
        parameters = {}

    percent = 1
    alpha = 0.5

    list_of_vals = []
    list_log = []
    list_of_vals_dict = attributes_filter.get_trace_attribute_values(log, 'responsible')

    list_of_vals_keys = list(list_of_vals_dict.keys())
    for i in range(len(list_of_vals_keys)):
        list_of_vals.append(list_of_vals_keys[i])

    for i in range(len(list_of_vals)):
        logsample = merge_log.log2sublog(log, list_of_vals[i],'responsible')
        list_log.append(logsample)

    if variant in VERSION_METHODS:
        y = VERSION_METHODS[variant](list_log, percent, alpha)

    Z = linkage(y, method='average')

    # Create dictionary for labeling nodes by their IDs

    id2name = dict(zip(range(len(list_of_vals)), list_of_vals))
    # print("id",id2name)

    T = to_tree(Z, rd=False)
    d3Dendro = dict(children=[], name="Root1")
    merge_log.add_node(T, d3Dendro)
    # print("d3", d3Dendro)

    leafname = merge_log.label_tree(d3Dendro["children"][0], id2name)
    d3Dendro = d3Dendro["children"][0]
    d3Dendro["name"] = 'root'
    ret = d3Dendro
    results = []

    trilist = bfs(ret)
    trilist[0][0] = trilist[0][1] + '-' + trilist[0][2]

    rootlist=[]
    for ele in trilist:
        rootlist.append(ele[0])


    return ret,leafname
