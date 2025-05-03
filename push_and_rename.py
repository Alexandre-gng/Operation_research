def push_relabel(n, capacities):
    # Initialisation
    flow = [[0] * n for _ in range(n)]
    height = [0] * n
    excess = [0] * n
    s, t = 0, n-1  # Source et puits
    
    height[s] = n
    # Pré-flot
    for v in range(n):
        if capacities[s][v] > 0:
            flow[s][v] = capacities[s][v]
            flow[v][s] = -flow[s][v]
            excess[v] = flow[s][v]
            excess[s] -= flow[s][v]
    
    # Liste des sommets actifs (sauf s et t)
    active_nodes = [i for i in range(n) if i != s and i != t and excess[i] > 0]
    
    while active_nodes:
        print("Active nodes:", active_nodes)  # Debug: afficher les noeuds actifs
        u = active_nodes[0]
        pushed = False
        
        # Essayer de pousser le flot
        for v in range(n):
            if capacities[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                delta = min(excess[u], capacities[u][v] - flow[u][v])
                flow[u][v] += delta
                flow[v][u] -= delta
                excess[u] -= delta
                excess[v] += delta
                pushed = True
                if v != s and v != t and v not in active_nodes and excess[v] > 0:
                    active_nodes.append(v)
                if excess[u] == 0:
                    active_nodes.remove(u)
                    break
        
        if not pushed and excess[u] > 0:
            # Réétiqueter
            min_height = float('inf')
            for v in range(n):
                if capacities[u][v] - flow[u][v] > 0:
                    min_height = min(min_height, height[v])
            height[u] = min_height + 1
    
    max_flow = sum(flow[s][v] for v in range(n) if flow[s][v] > 0)
    return max_flow, flow