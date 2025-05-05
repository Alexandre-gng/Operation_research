import time
import random
import matplotlib.pyplot as plt
import numpy as np
import math
from ford_fulkerson import ford_fulkerson

import time
import random
import matplotlib.pyplot as plt
import numpy as np
import math
from ford_fulkerson import ford_fulkerson
from push_and_rename import push_relabel
from min_cost_flow import min_cost_flow

def generate_random_flow_problem(n):
    """
    Génère un problème de flot aléatoire avec n sommets.
    - C : matrice de capacité, nulle sur la diagonale et comportant moins de la moitié de valeurs non nulles
    - D : matrice de coût associée aux arêtes de capacité non nulle
    """
    # Initialisation des matrices avec des zéros
    C = [[0 for _ in range(n)] for _ in range(n)]
    D = [[0 for _ in range(n)] for _ in range(n)]
    
    # Nombre d'arêtes à créer (environ la moitié du nombre maximum possible)
    num_edges = int(n * n / 2)
    
    # Génération des arêtes avec capacités aléatoires
    edges_created = 0
    while edges_created < num_edges:
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        
        # Éviter la diagonale et les arêtes déjà créées
        if i != j and C[i][j] == 0:
            C[i][j] = random.randint(1, 100)
            D[i][j] = random.randint(1, 100)
            edges_created += 1
    
    return C, D

def measure_execution_time(algorithm, *args):
    """
    Mesure le temps d'exécution d'un algorithme donné.
    """
    start_time = time.time()
    algorithm(*args)
    end_time = time.time()
    
    return end_time - start_time

def run_complexity_analysis(sizes=[10, 20, 40, 100, 400, 1000, 4000]):
    """
    Exécute l'analyse de complexité pour les tailles de problèmes spécifiées.
    Pour chaque taille, génère 100 problèmes aléatoires et mesure les temps d'exécution.
    """
    results = {
        "ff": {size: [] for size in sizes},
        "pr": {size: [] for size in sizes},
        "min": {size: [] for size in sizes}
    }
    
    for size in sizes:
        print(f"Analyse pour les problèmes de taille {size}...")
        
        for _ in range(100):  # Générer 100 instances pour chaque taille
            # Générer un problème aléatoire
            capacities, costs = generate_random_flow_problem(size)
            
            # Modifier les fonctions d'algorithme pour ne pas afficher les résultats
            # pendant l'analyse de complexité
            
            # Mesurer le temps d'exécution de Ford-Fulkerson
            time_ff = measure_execution_time(ford_fulkerson, size, capacities)
            results["ff"][size].append(time_ff)
            
            # Mesurer le temps d'exécution de Pousser-Réétiqueter
            time_pr = measure_execution_time(push_relabel, size, capacities)
            results["pr"][size].append(time_pr)
            
            # Calculer d'abord le flot max pour obtenir la valeur de flot cible
            max_flow, _ = ford_fulkerson(size, capacities)
            target_flow = max_flow // 2 if max_flow > 0 else 0
            
            # Mesurer le temps d'exécution de Flot à coût min
            time_min = measure_execution_time(min_cost_flow, size, capacities, costs, target_flow)
            results["min"][size].append(time_min)
    
    return results

def plot_results(results):
    """
    Trace les nuages de points des temps d'exécution.
    """
    sizes = sorted(list(results["ff"].keys()))
    
    # Tracer les nuages de points
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    
    # Ford-Fulkerson
    for size in sizes:
        axs[0].scatter([size] * len(results["ff"][size]), results["ff"][size], alpha=0.5)
    axs[0].set_title("Temps d'exécution de Ford-Fulkerson")
    axs[0].set_xlabel("Taille du problème (n)")
    axs[0].set_ylabel("Temps (secondes)")
    axs[0].set_xscale('log')
    axs[0].set_yscale('log')
    
    # Pousser-Réétiqueter
    for size in sizes:
        axs[1].scatter([size] * len(results["pr"][size]), results["pr"][size], alpha=0.5)
    axs[1].set_title("Temps d'exécution de Pousser-Réétiqueter")
    axs[1].set_xlabel("Taille du problème (n)")
    axs[1].set_ylabel("Temps (secondes)")
    axs[1].set_xscale('log')
    axs[1].set_yscale('log')
    
    # Flot à coût min
    for size in sizes:
        axs[2].scatter([size] * len(results["min"][size]), results["min"][size], alpha=0.5)
    axs[2].set_title("Temps d'exécution de Flot à coût minimal")
    axs[2].set_xlabel("Taille du problème (n)")
    axs[2].set_ylabel("Temps (secondes)")
    axs[2].set_xscale('log')
    axs[2].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('execution_times_scatter.png')
    plt.close()
    
    # Tracer les valeurs maximales (pire cas)
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    
    # Calculer les valeurs maximales pour chaque taille
    max_ff = [max(results["ff"][size]) for size in sizes]
    max_pr = [max(results["pr"][size]) for size in sizes]
    max_min = [max(results["min"][size]) for size in sizes]
    
    # Ford-Fulkerson - pire cas
    axs[0].plot(sizes, max_ff, 'ro-')
    axs[0].set_title("Temps d'exécution maximal de Ford-Fulkerson (pire cas)")
    axs[0].set_xlabel("Taille du problème (n)")
    axs[0].set_ylabel("Temps (secondes)")
    axs[0].set_xscale('log')
    axs[0].set_yscale('log')
    
    # Pousser-Réétiqueter - pire cas
    axs[1].plot(sizes, max_pr, 'go-')
    axs[1].set_title("Temps d'exécution maximal de Pousser-Réétiqueter (pire cas)")
    axs[1].set_xlabel("Taille du problème (n)")
    axs[1].set_ylabel("Temps (secondes)")
    axs[1].set_xscale('log')
    axs[1].set_yscale('log')
    
    # Flot à coût min - pire cas
    axs[2].plot(sizes, max_min, 'bo-')
    axs[2].set_title("Temps d'exécution maximal de Flot à coût minimal (pire cas)")
    axs[2].set_xlabel("Taille du problème (n)")
    axs[2].set_ylabel("Temps (secondes)")
    axs[2].set_xscale('log')
    axs[2].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('execution_times_worst_case.png')
    plt.close()
    
    # Comparer les algorithmes FF et PR
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ratio = [max_ff[i] / max_pr[i] if max_pr[i] > 0 else 0 for i in range(len(sizes))]
    ax.plot(sizes, ratio, 'mo-')
    ax.set_title("Rapport des temps d'exécution FF/PR")
    ax.set_xlabel("Taille du problème (n)")
    ax.set_ylabel("Rapport FF/PR")
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig('comparison_ff_pr.png')
    plt.close()
    
    return max_ff, max_pr, max_min

def identify_complexity(times, sizes):
    """
    Identifie le type de complexité en comparant la croissance des temps d'exécution
    avec différentes fonctions de complexité.
    """
    complexities = {
        "O(log(n))": [math.log(n) for n in sizes],
        "O(n)": [n for n in sizes],
        "O(n*log(n))": [n * math.log(n) for n in sizes],
        "O(n^2)": [n**2 for n in sizes],
        "O(n^3)": [n**3 for n in sizes],
        "O(2^n)": [2**min(n, 30) for n in sizes]  # Limité pour éviter les overflows
    }
    
    # Normalisation des valeurs pour une meilleure comparaison
    norm_times = times / max(times)
    
    best_fit = None
    best_correlation = 0
    
    for complexity_name, complexity_values in complexities.items():
        norm_complexity = np.array(complexity_values) / max(complexity_values)
        
        # Calculer la corrélation entre les temps normalisés et les valeurs de complexité
        correlation = np.abs(np.corrcoef(norm_times, norm_complexity)[0, 1])
        
        if correlation > best_correlation:
            best_correlation = correlation
            best_fit = complexity_name
    
    return best_fit

def analyze_complexity(results):
    """
    Analyse la complexité des algorithmes et affiche les résultats.
    """
    sizes = sorted(list(results["ff"].keys()))
    
    # Obtenir les temps maximaux pour chaque taille
    max_ff = np.array([max(results["ff"][size]) for size in sizes])
    max_pr = np.array([max(results["pr"][size]) for size in sizes])
    max_min = np.array([max(results["min"][size]) for size in sizes])
    
    # Identifier les complexités
    ff_complexity = identify_complexity(max_ff, sizes)
    pr_complexity = identify_complexity(max_pr, sizes)
    min_complexity = identify_complexity(max_min, sizes)
    
    print("\nAnalyse de la complexité dans le pire des cas :")
    print(f"Ford-Fulkerson: {ff_complexity}")
    print(f"Pousser-Réétiqueter: {pr_complexity}")
    print(f"Flot à coût minimal: {min_complexity}")
    
    return ff_complexity, pr_complexity, min_complexity


def main():
    """
    Fonction principale pour exécuter l'étude de complexité.
    """
    print("Démarrage de l'analyse de complexité...")
    
    # Tailles à tester (ajustées pour une exécution plus rapide)
    sizes = [10, 20, 40, 100, 200, 300, 400, 500]
    
    # Exécuter l'analyse
    results = run_complexity_analysis(sizes)
    
    # Tracer les résultats
    max_ff, max_pr, max_min = plot_results(results)
    
    # Analyser la complexité
    min_complexity = analyze_complexity(results)
    
    print("\nAnalyse terminée. Les graphiques ont été enregistrés.")
    
    return results

main()