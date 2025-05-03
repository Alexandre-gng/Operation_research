from tabulate import tabulate

def bellman_ford_residual(n, residual_cost, source):
    dist = [float('inf')] * n
    pred = [(-1, -1)] * n  # (u,v) arc utilisé pour atteindre v
    dist[source] = 0

    # Relaxation
    for _ in range(n - 1):
        updated = False
        for u in range(n):
            for v, cost_uv in residual_cost[u].items():
                if dist[u] + cost_uv < dist[v]:
                    dist[v] = dist[u] + cost_uv
                    pred[v] = (u, v)
                    updated = True
        if not updated:
            break

    # Détection de cycle négatif (optionnel)
    for u in range(n):
        for v, cost_uv in residual_cost[u].items():
            if dist[u] + cost_uv < dist[v]:
                raise ValueError("Cycle négatif détecté dans le résiduel")

    return dist, pred


def min_cost_flow(n, capacities, costs, target_flow, labels=None):
    """
    Résout le flot à coût minimal en poussant target_flow unités.
    Affiche un tableau des chemins d'augmentation avec push/capacité résiduelle.

    - n : nombre de nœuds (indices 0..n-1)
    - capacities[u][v] : capacité de l'arc u->v (0 si pas d'arc)
    - costs[u][v] : coût unitaire de u->v
    - target_flow : flot total souhaité depuis 0 vers n-1
    - labels : liste facultative de noms de nœuds, ex ['s','a','b','c','d','e','t']
    """
    if labels is None:
        labels = [str(i) for i in range(n)]
    assert len(labels) == n

    flow = [[0]*n for _ in range(n)]
    total_flow = 0
    total_cost = 0
    history = []

    while total_flow < target_flow:
        # 1) Construire le graphe résiduel
        residual_cap = [dict() for _ in range(n)]
        residual_cost = [dict() for _ in range(n)]
        for u in range(n):
            for v in range(n):
                cap_uv = capacities[u][v]
                if cap_uv > 0:
                    remain = cap_uv - flow[u][v]
                    if remain > 0:
                        residual_cap[u][v] = remain
                        residual_cost[u][v] = costs[u][v]
                    if flow[u][v] > 0:
                        # arc inverse
                        residual_cap[v][u] = flow[u][v]
                        residual_cost[v][u] = -costs[u][v]

        # 2) Plus court chemin dans le résiduel
        try:
            dist, pred = bellman_ford_residual(n, residual_cost, 0)
        except ValueError as e:
            print(e)
            break

        if dist[n-1] == float('inf'):
            print("Plus de chemin améliorant — flot max résiduel atteint.")
            break

        # 3) Remonter le chemin et calculer le push
        path = []
        v = n-1
        while v != 0:
            u, _ = pred[v]
            path.append((u, v))
            v = u
        path.reverse()

        # 4) Déterminer le flot qu'on peut y pousser
        push = target_flow - total_flow
        for u, v in path:
            push = min(push, residual_cap[u][v])

        # 5) Enregistrer la ligne du tableau d’itération
        row = { name: "" for name in labels }
        for u, v in path:
            cap_before = residual_cap[u][v]
            row[labels[v]] = f"{push}/{cap_before}"
        history.append(row)

        # 6) Appliquer le push
        for u, v in path:
            if capacities[u][v] > 0:
                # arc direct
                flow[u][v] += push
            else:
                # arc inverse
                flow[v][u] -= push
            total_cost += push * residual_cost[u][v]

        total_flow += push

    # Affichage du tableau final
    print(tabulate(history, headers="keys", tablefmt="plain"))
    print(f"\nValeur du coût minimal pour flot {target_flow} = {total_cost}")

    if total_flow < target_flow:
        print(f"(Flot atteint = {total_flow}, but {target_flow} demandé.)")

    return total_cost, flow