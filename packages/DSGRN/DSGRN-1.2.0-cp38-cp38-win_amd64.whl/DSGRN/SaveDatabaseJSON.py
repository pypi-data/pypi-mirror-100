# SaveDatabaseJSON.py
# Marcio Gameiro
# MIT LICENSE
# 2021-03-26

import DSGRN
import pychomp2
import itertools
import json

def dsgrn_cell_to_cc_cell_map(network):
    """Return a mapping from the top dimensional cells
    in the DSGRN complex to the top dimensional
    cells in the pychomp2 cubical complex.
    """

    # Construct a cubical complex using pychomp2. A cubical complex in pychomp2
    # does not contain the rightmost boundary, so make one extra layer of
    # cubes and ignore the last layer (called rightfringe in pychomp2).
    cubical_complex = pychomp2.CubicalComplex([x + 1 for x in network.domains()])
    dimension = network.size()
    # Mapping from DSGRN top cells to cc top cells
    cell2cc_cell = {}
    # DSGRN only uses the top dimensional cells to
    # construct the state transiton graph and the
    # corresponding morse sets and these cells are
    # indexed from 0 to n-1, where n is the number
    # of top dimensional cells. Hence we can get a
    # mapping by counting the cells in the cc.
    dsgrn_index = 0
    for cell_index in cubical_complex(dimension):
        # Ignore fringe cells
        if cubical_complex.rightfringe(cell_index):
            continue
        cell2cc_cell[dsgrn_index] = cell_index
        dsgrn_index += 1
    return cell2cc_cell

def network_json(network):
    """Return json data for network."""
    nodes = [] # Get network nodes
    for d in range(network.size()):
        node = {"id" : network.name(d)}
        nodes.append(node)
    # Get network edges
    edges = [(u, v) for u in range(network.size()) for v in network.outputs(u)]
    links = []
    for (u, v) in edges:
        edge_type = 1 if network.interaction(u, v) else -1
        link = {"source" : network.name(u),
                "target" : network.name(v),
                "type": edge_type}
        links.append(link)
    network_json_data = {"network" : {"nodes" : nodes, "links" : links}}
    return network_json_data

def parameter_graph_json(parameter_graph, vertices=None, verts_colors=None):
    """Return json data for parameter graph."""
    # Get list of vertices if none
    if vertices == None:
        vertices = list(range(parameter_graph.size()))
    # Set empty dictionary for verts_colors if none
    if verts_colors == None:
        verts_colors = {}
    all_edges = [(u, v) for u in vertices for v in parameter_graph.adjacencies(u, 'codim1') if v in vertices]
    # Remove double edges (all edges are double)
    edges = [(u, v) for (u, v) in all_edges if u > v]
    nodes = []
    for v in vertices:
        v_color = verts_colors[v] if v in verts_colors else "";
        node = {"id" : v, "color" : v_color}
        # node = {"id" : str(v), "color" : v_color}
        nodes.append(node)
    links = []
    for (u, v) in edges:
        link = {"source" : u, "target" : v}
        # link = {"source" : str(u), "target" : str(v)}
        links.append(link)
    parameter_graph_json_data = {"parameter_graph" : {"nodes" : nodes, "links" : links}}
    return parameter_graph_json_data

def cubical_complex_json(network):
    """Return json data for cubical complex."""
    # Get complex dimension
    dimension = network.size()
    # Construct a cubical complex using pychomp2. A cubical complex in pychomp2
    # does not contain the rightmost boundary, so make one extra layer of
    # cubes and ignore the last layer (called rightfringe in pychomp2).
    cubical_complex = pychomp2.CubicalComplex([x + 1 for x in network.domains()])
    # Get vertices coordinates and set a
    # mapping from coords to its index in
    # the list of coordinates.
    verts_coords = []
    coords2idx = {}
    # Get the coords of all cells of dimension 0.
    # The 0-dim cells in a cubical complex in pychomp2
    # are indexed from 0 to n-1, where n is the number
    # of 0-dim cells. Hence the cell_index coincides
    # with the index of coords in the list verts_coords.
    for cell_index in cubical_complex(0):
        coords = cubical_complex.coordinates(cell_index)
        coords2idx[tuple(coords)] = cell_index
        verts_coords.append(coords)
    cells = [] # Get the cell complex data
    for cell_index in cubical_complex:
        # Ignore fringe cells
        if cubical_complex.rightfringe(cell_index):
            continue
        # Get this cell dimension
        cell_dim = cubical_complex.cell_dim(cell_index)
        # Get coords of the lower corner of the box
        coords_lower = cubical_complex.coordinates(cell_index)
        # Get index of vertex corresponding to these coords
        # Due to the way pychomp2 index the 0-dim cells we get
        # that idx_lower == cell_index (see coords2idx above).
        idx_lower = coords2idx[tuple(coords_lower)]
        # Get the shape of this cell (see pychomp2)
        shape = cubical_complex.cell_shape(cell_index)
        # Add 1 to the appropriate entries to get coords of the upper corner
        coords_upper = [coords_lower[d] + (1 if shape & (1 << d) != 0 else 0) for d in range(dimension)]
        # Get index of vertex corresponding to these coords
        idx_upper = coords2idx[tuple(coords_upper)]
        # Get indices of coords that have extent
        ind_extent = [d for d in range(dimension) if shape & (1 << d) != 0]
        if cell_dim == 0:
            cell_verts = [idx_lower]
        elif cell_dim == 1:
            cell_verts = [idx_lower, idx_upper]
        elif cell_dim == 2:
            # Index of vertex 1
            idx1 = idx_lower
            # Coords and index of vertex 2
            coords_v2 = [coord for coord in coords_lower]
            coords_v2[ind_extent[0]] += 1
            idx2 = coords2idx[tuple(coords_v2)]
            # Index of vertex 3
            idx3 = idx_upper
            # Coords and index of vertex 4
            coords_v4 = [coord for coord in coords_lower]
            coords_v4[ind_extent[1]] += 1
            idx4 = coords2idx[tuple(coords_v4)]
            cell_verts = [idx1, idx2, idx3, idx4]
        elif cell_dim == 3: # cell_dim == dimension == 3
            # First get vertices of unit cube as cartesian product of {0, 1}
            u_verts = list(itertools.product((0, 1), repeat=cell_dim))
            # Add verts of unit cube to coords_lower to get verts of this cell
            cell_verts = []
            for u in u_verts:
                coords_vert = [sum(x) for x in zip(u, coords_lower)]
                idx_vert = coords2idx[tuple(coords_vert)]
                cell_verts.append(idx_vert)
        else: # Ignore cell if dim > 3
            continue
        cell = {"cell_dim" : cell_dim, "cell_index" : cell_index, "cell_verts" : cell_verts}
        cells.append(cell)
    complex_json_data = {"complex" : {"dimension" : dimension,
                                      "verts_coords" : verts_coords,
                                      "cells" : cells} }
    return complex_json_data

def morse_graph_json(morse_graph):
    """Return json data for Morse graph."""

    def vertex_rank(u):
        """Return how many levels down of children u have."""
        children = [v for v in morse_graph.poset().children(u)]
        if len(children) == 0:
            return 0
        return 1 + max([vertex_rank(v) for v in children])

    # Get list of Morse nodes
    morse_nodes = range(morse_graph.poset().size())
    morse_graph_data = [] # Morse graph data
    for morse_node in morse_nodes:
        label = morse_graph.annotation(morse_node)[0]
        adjacencies = morse_graph.poset().children(morse_node)
        morse_node_data = {"node" : morse_node,
                           "rank" : vertex_rank(morse_node),
                           "label" : label,
                           "adjacencies" : adjacencies}
        morse_graph_data.append(morse_node_data)
    morse_graph_json_data = {"morse_graph" : morse_graph_data}
    return morse_graph_json_data

def morse_sets_json(network, morse_graph, morse_decomposition):
    """Return json data for Morse sets."""
    # Get a mapping from DSGRN top cells to cc top cells
    cell2cc_cell = dsgrn_cell_to_cc_cell_map(network)
    # Get list of Morse nodes
    morse_nodes = range(morse_decomposition.poset().size())
    # Permutation that gives node index from Morse set index
    permutation = morse_graph.permutation()
    morse_sets_data = [] # Morse sets data
    for morse_node in morse_nodes:
        morse_cells = [cell2cc_cell[c] for c in morse_decomposition.morseset(morse_node)]
        # Get Morse graph node index
        morse_graph_node = permutation[morse_node]
        morse_set = {"index" : morse_graph_node, "cells" : morse_cells}
        morse_sets_data.append(morse_set)
    morse_sets_json_data = {"morse_sets" : morse_sets_data}
    return morse_sets_json_data

def state_transition_graph_json(network, domain_graph):
    """Return json data for state transiton graph."""
    # Get a mapping from DSGRN top cells to cc top cells
    cell2cc_cell = dsgrn_cell_to_cc_cell_map(network)
    # Get state transition graph vertices
    stg_vertices = range(domain_graph.digraph().size())
    stg = [] # State transition graph
    for v in stg_vertices:
        adjacencies = [cell2cc_cell[u] for u in domain_graph.digraph().adjacencies(v)]
        node_adjacency_data = {"node" : cell2cc_cell[v], "adjacencies" : adjacencies}
        stg.append(node_adjacency_data)
    stg_json_data = {"stg" : stg}
    return stg_json_data

def save_morse_graph_database_json(parameter_graph, database_fname, param_indices=None):
    if parameter_graph.dimension() not in [2, 3]:
        print('Only networks of dimension 2 or 3 are allowed!')
        return
    network = parameter_graph.network()
    if param_indices == None:
        param_indices = range(parameter_graph.size())
    network_json_data = network_json(network)
    cell_complex_json_data = cubical_complex_json(network)
    param_graph_json_data = parameter_graph_json(parameter_graph, param_indices)
    dynamics_database = [] # Dynamics database
    for par_index in param_indices:
        # Compute DSGRN dynamics
        parameter = parameter_graph.parameter(par_index)
        domain_graph = DSGRN.DomainGraph(parameter)
        morse_decomposition = DSGRN.MorseDecomposition(domain_graph.digraph())
        morse_graph = DSGRN.MorseGraph(domain_graph, morse_decomposition)
        morse_graph_json_data = morse_graph_json(morse_graph)
        morse_sets_json_data = morse_sets_json(network, morse_graph, morse_decomposition)
        stg_json_data = state_transition_graph_json(network, domain_graph)
        # Dynamics data for this parameter
        dynamics_json_data = {"parameter" : par_index,
                              "morse_graph" : morse_graph_json_data["morse_graph"],
                              "morse_sets" : morse_sets_json_data["morse_sets"],
                              "stg" : stg_json_data["stg"]}
        dynamics_database.append(dynamics_json_data)
    morse_graph_database = {"network" : network_json_data["network"],
                            "complex" : cell_complex_json_data["complex"],
                            "parameter_graph" : param_graph_json_data["parameter_graph"],
                            "dynamics_database" : dynamics_database}
    # Save database to a file
    with open(database_fname, 'w') as outfile:
        json.dump(morse_graph_database, outfile)
