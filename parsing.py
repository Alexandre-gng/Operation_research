def lire_graphe_file(file_path):
    with open(file_path, 'r') as file:
        # Lire et nettoyer les lignes du fichier
        lines = [line.strip() for line in file if line.strip()]

    # Déterminer le type de problème en fonction du nombre de lignes
    node_count = int(lines[0])
    expected_lines_for_min_cost = 1 + 2 * node_count

    if len(lines) == expected_lines_for_min_cost:
        problem_type = "min_cost"
        print("Problème de coût minimal détecté.")
    else:
        problem_type = "max_flow"
        print("Problème de flot maximal détecté.")

    # Initialisation des structures de données
    capacity_matrix = []
    cost_matrix = []

    # Lire les capacités
    for i in range(1, node_count + 1):
        capacity_row = list(map(int, lines[i].split()))
        capacity_matrix.append(capacity_row)

    # Lire les coûts si c'est un problème de coût minimal
    if problem_type == "min_cost":
        for i in range(node_count + 1, expected_lines_for_min_cost):
            cost_row = list(map(int, lines[i].split()))
            cost_matrix.append(cost_row)
    else:
        # Initialiser une matrice de coûts nulle pour les problèmes de flot maximal
        cost_matrix = [[0] * node_count for _ in range(node_count)]

    return problem_type, node_count, capacity_matrix, cost_matrix
