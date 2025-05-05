from tabulate import tabulate

def bellman_ford_residual(n, residual_cost, source):
    dist = [float('inf')] * n
    # (u,v) arc utilisé pour atteindre v
    pred = [(-1, -1)] * n 
    dist[source] = 0

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

    for u in range(n):
        for v, cost_uv in residual_cost[u].items():
            if dist[u] + cost_uv < dist[v]:
                raise ValueError("Cycle négatif détecté dans le résiduel")

    return dist, pred


def min_cost_flow(n, capacities, costs, target_flow, labels=None):
    if labels is None:
        labels = [str(i) for i in range(n)]
    assert len(labels) == n
    
    flow = [[0]*n for _ in range(n)]
    total_flow = 0
    total_cost = 0
    history = []

    while total_flow < target_flow:
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
                        residual_cap[v][u] = flow[u][v]
                        residual_cost[v][u] = -costs[u][v]

        try:
            dist, pred = bellman_ford_residual(n, residual_cost, 0)
        except ValueError as e:
            print(e)
            break

        if dist[n-1] == float('inf'):
            print("Plus de chemin améliorant — flot max résiduel atteint.")
            break

        path = []
        v = n-1
        while v != 0:
            u, _ = pred[v]
            path.append((u, v))
            v = u
        path.reverse()

        push = target_flow - total_flow
        for u, v in path:
            push = min(push, residual_cap[u][v])

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