import time
import random
import matplotlib.pyplot as plt
from ford_fulkerson import ford_fulkerson
from push_and_rename import push_relabel
from min_cost_flow import min_cost_flow

def generate_random_graph(n):
    capacities = [[0]*n for _ in range(n)]
    costs = [[0]*n for _ in range(n)]
    
    num_edges = (n**2) // 2
    
    for _ in range(num_edges):
        i, j = random.sample(range(n), 2)
        capacities[i][j] = random.randint(1, 100)
        costs[i][j] = random.randint(1, 100)
    
    return capacities, costs

def analyze_complexity():
    sizes = [10, 20, 40, 100, 400, 1000]
    num_trials = 100
    
    results = {
        'FF': {size: [] for size in sizes},
        'PR': {size: [] for size in sizes},
        'MIN': {size: [] for size in sizes}
    }
    
    for size in sizes:
        print(f"Analyzing size {size}...")
        for _ in range(num_trials):
            capacities, costs = generate_random_graph(size)
            
            # Ford-Fulkerson
            start = time.time()
            ford_fulkerson(size, capacities)
            results['FF'][size].append(time.time() - start)
            
            # Push-Relabel
            start = time.time()
            push_relabel(size, capacities)
            results['PR'][size].append(time.time() - start)
            
            # Min Cost Flow (avec flot cible = flot max / 2)
            max_flow, _ = ford_fulkerson(size, capacities)
            target = max_flow // 2
            start = time.time()
            min_cost_flow(size, capacities, costs, target)
            results['MIN'][size].append(time.time() - start)
    
    # Affichage des résultats
    plot_results(results)

def plot_results(results):
    plt.figure(figsize=(12, 6))
    
    for algo in ['FF', 'PR', 'MIN']:
        sizes = sorted(results[algo].keys())
        avg_times = [sum(results[algo][size])/len(results[algo][size]) for size in sizes]
        max_times = [max(results[algo][size]) for size in sizes]
        
        plt.plot(sizes, avg_times, label=f"{algo} (moyenne)")
        plt.plot(sizes, max_times, '--', label=f"{algo} (pire cas)")
    
    plt.xlabel('Taille du graphe (n)')
    plt.ylabel('Temps d\'exécution (s)')
    plt.title('Analyse de complexité des algorithmes de flot')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('complexity_analysis.png')
    plt.show()