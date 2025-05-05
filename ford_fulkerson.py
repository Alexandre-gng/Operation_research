from tools import bfs, print_mat_flot

def ford_fulkerson(num_nodes, capacity_graph):
    residual_graph = [row[:] for row in capacity_graph]
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    max_flow_value = 0
    start_node, end_node = 0, num_nodes - 1
    iteration = 0

    print("=== Initialisation ===")

    while True:
        iteration += 1
        parent_nodes = [-1] * num_nodes
        if not find_augmenting_path(residual_graph, num_nodes, start_node, end_node, parent_nodes):
            break

        path_flow = float("inf")
        path_edges = []
        node = end_node
        while node != start_node:
            prev_node = parent_nodes[node]
            path_flow = min(path_flow, residual_graph[prev_node][node])
            path_edges.append((prev_node, node))
            node = prev_node
        path_edges.reverse()

        print(f"\n=== Itération {iteration} ===")
        print(f"Chemin augmentant: {' -> '.join(f'{u}->{v}' for u, v in path_edges)}")
        print(f"Flux ajouté: {path_flow}")

        node = end_node
        while node != start_node:
            prev_node = parent_nodes[node]
            residual_graph[prev_node][node] -= path_flow
            residual_graph[node][prev_node] += path_flow
            flow_matrix[prev_node][node] += path_flow
            node = prev_node

        max_flow_value += path_flow

        print("\nMatrice de flux actuelle:")
        show_flow_matrix(flow_matrix, capacity_graph)

    print(f"\n=== Résultat final ===")
    print(f"Flux maximal: {max_flow_value}")
    print("Matrice de flot finale:")
    show_flow_matrix(flow_matrix, capacity_graph)

    return max_flow_value, flow_matrix

def find_augmenting_path(residual_graph, num_nodes, start_node, end_node, parent_nodes):
    explored = [False] * num_nodes
    queue = [start_node]
    explored[start_node] = True

    while queue:
        current_node = queue.pop(0)
        for neighbor in range(num_nodes):
            if not explored[neighbor] and residual_graph[current_node][neighbor] > 0:
                parent_nodes[neighbor] = current_node
                explored[neighbor] = True
                queue.append(neighbor)
                if neighbor == end_node:
                    return True
    return False

def show_flow_matrix(flow_matrix, capacity_graph):
    num_rows = len(flow_matrix)
    num_cols = len(flow_matrix[0]) if num_rows > 0 else 0

    col_labels = [i for i in range(0, num_cols)]

    print("   " + " ".join(f"{label:>3}" for label in col_labels))
    print("  " + "-" * (4 * num_cols + 2))

    for idx, row in enumerate(flow_matrix):
        row_label = idx
        print(f"{row_label} |" + " ".join(f"{val:>3}" for val in row))