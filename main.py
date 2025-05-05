from parsing import lire_graphe_file
from ford_fulkerson import ford_fulkerson
from push_and_rename import push_relabel
from min_cost_flow import min_cost_flow
from tools import print_mat_flot

def main():
    print(" ____  ____  ____  ____  _     _      _____   ____  _____   _____ _     ____  _____ ")
    print("/  __\\/  __\\/  _ \\/  _ \\/ \\   / \\__/|/  __/  /  _ \\/  __/  /    // \\   /  _ \\/__ __\\")
    print("|  \\/||  \\/|| / \\|| | //| |   | |\\/|||  \\    | | \\||  \\    |  __\\| |   | / \\|  / \\  ")
    print("|  __/|    /| \\_/|| |_\\\\| |_/\\| |  |||  /_   | |_/||  /_   | |   | |_/\\| \\_/|  | |  ")
    print("\\_/   \\_/\\_\\\\____/\\____/\\____/\\_/  \\|\\____\\  \\____/\\____\\  \\_/   \\____/\\____/  \\_/  ")
    print("")
    while 1:
        print("a. Résoudre un problème de flot maximal")
        print("b. Résoudre un problème de flot à coût minimal")
        print("c. Quitter")
        
        choix = input("Choix: ")
        
        if choix == "c":
            break
            
        try:
            problem_num = int(input("Numéro du problème (1-10): "))
            if problem_num < 1 or problem_num > 10:
                raise ValueError
                
            filename = "txt_file/test" + str(problem_num) + ".txt"
            graph_type, n, capacities, costs = lire_graphe_file(filename)
            
            if choix == "a":
                print("\nAlgorithmes pour flot maximal:")
                print("a. Ford-Fulkerson")
                print("b. Pousser-Réétiqueter")
                algo_choix = input("Choix: ")
                
                if algo_choix == "a":
                    max_flow, flow_matrix = ford_fulkerson(n, capacities)
                    print(f"\nFlot maximal: {max_flow}")
                    print("Matrice de flot:")
                    print_mat_flot(flow_matrix, capacities)
                elif algo_choix == "b":
                    max_flow, flow_matrix = push_relabel(n, capacities)
                    print(f"\nFlot maximal: {max_flow}")
                    print("Matrice de flot:")
                    print_mat_flot(flow_matrix, capacities)
                    
            elif choix == "b":
                if graph_type != "min_cost":
                    print("Ce problème n'a pas de couts associes")
                    continue
                    
                max_flow, _ = ford_fulkerson(n, capacities)
                target_flow = max_flow + 1
                while target_flow < 1 or target_flow > max_flow:
                    print(f"Valeur max: {max_flow//2}") 
                    target_flow = input("Flot cible : ")
                    target_flow = int(target_flow)

                print(f"\nCalcul du flot à coût minimal pour une valeur de {target_flow}")
                
                total_cost, flow_matrix = min_cost_flow(n, capacities, costs, target_flow)
                print(f"Cout total: {total_cost}")
                print("Matrice de flot:")
                print_mat_flot(flow_matrix, capacities)
                
        except ValueError:
            print("Entrée invalide. Veuillez réessayer.")
        except FileNotFoundError:
            print("Fichier non trouvé. Veuillez vérifier le numéro du problème.")
        except Exception as e:
            print(f"Une erreur est survenue: {str(e)}")

if __name__ == "__main__":
    main()