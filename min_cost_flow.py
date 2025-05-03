def bellman_algo(n, costs, s):
    distance = [float('inf')] * n
    distance[s] = 0
    predecessor = [-1] * n

    # Relax edges up to n-1 times
    for _ in range(n-1):
        for u in range(n):
            for v in range(n):
                if costs[u][v] != 0 and distance[u] + costs[u][v] < distance[v]:
                    distance[v] = distance[u] + costs[u][v]
                    predecessor[v] = u

    # Check for negative weight cycles
    for u in range(n):
        for v in range(n):
            if costs[u][v] != 0 and distance[u] + costs[u][v] < distance[v]:
                raise ValueError("Cycle négatif détecté")

    return distance, predecessor

def min_cost_flow(n, capacities, costs, target_flow):
    # Initialisation
    flow = [[0] * n for _ in range(n)]
    total_flow = 0
    total_cost = 0

    while total_flow < target_flow:
        try:
            # Étape 1: Trouver le chemin de coût minimal avec Bellman-Ford
            distance, predecessor = bellman_algo(n, costs, 0)
        except ValueError as e:
            print(e)
            break  # Stop if a negative cycle is detected

        if distance[n-1] == float('inf'):
            print("Plus de chemin améliorant.")
            break  # No augmenting path exists, terminate the loop

        # Étape 2: Trouver le chemin améliorant
        path = []
        u = n-1
        while u != 0:
            path.append((predecessor[u], u))
            u = predecessor[u]
        path.reverse()

        # Étape 3: Calculer le flot maximal sur ce chemin
        path_flow = min(capacities[v][u] - flow[v][u] for v, u in path)
        path_flow = min(path_flow, target_flow - total_flow)

        if path_flow <= 0:
            print("Flot négatif ou infini, break.")
            break  # No valid flow can be pushed along this path

        # Étape 4: Mettre à jour les flots
        for v, u in path:
            flow[v][u] += path_flow
            flow[u][v] -= path_flow
            total_cost += path_flow * costs[v][u]

        total_flow += path_flow

    if total_flow < target_flow:
        print(f"Le flot voulu {target_flow} est innatteignable. Flot total: {total_flow}")

    return total_cost, flow