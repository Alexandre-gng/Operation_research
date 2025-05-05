from collections import deque

def print_mat_flot(matrice_flot, capacites):
    n = len(matrice_flot)

    max_widths = [5] * n

    for j in range(n):
        for i in range(n):
            if capacites[i][j] > 0:
                cell_content = f"{matrice_flot[i][j]}/{capacites[i][j]}" if matrice_flot[i][j] > 0 else "0"
                max_widths[j] = max(max_widths[j], len(cell_content))

    header = "   " + " ".join(f"{i:^{max_widths[j]}}" for j, i in enumerate(range(n)))
    print(header)

    for i in range(n):
        row_str = f"{i:2} "
        for j in range(n):
            if capacites[i][j] > 0:
                cell_content = f"{matrice_flot[i][j]}/{capacites[i][j]}" if matrice_flot[i][j] > 0 else "0"
                row_str += f"{cell_content:^{max_widths[j]}} "
            else:
                row_str += f"{'0':^{max_widths[j]}} "
        print(row_str)

        
        
def bfs(residual_graph, n, s, t, parent):
    visited = [False] * n
    queue = deque()
    queue.append(s)
    visited[s] = True
    
    while queue:
        u = queue.popleft()
        
        for v in range(n):
            if not visited[v] and residual_graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == t:
                    return True
    return False