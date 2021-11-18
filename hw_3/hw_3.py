import random
import matplotlib.pyplot as plt

def generate_random_coordinates(number_cities):
    coordinates = []
    for _ in range(number_cities):
        coordinates.append([random.uniform(-number_cities, number_cities), random.uniform(-number_cities, number_cities)])
    return coordinates

def get_distance_between_two_cities(city_1, city_2):
    return ((city_1[0] - city_2[0]) ** 2 + (city_1[1] - city_2[1]) ** 2) ** 0.5

def create_route(cities):
    route = random.sample(cities, len(cities))
    return route


def create_initial_population(size, cities):
    population = []
    for _ in range(size):
        population.append(create_route(cities))
    return population



def get_route_distance(route):
    path_distance = 0
    for i, city in enumerate(route):
        from_city = city
        to_city = route[(i + 1) % (len(route))]
        path_distance += get_distance_between_two_cities(from_city, to_city)
    return path_distance    

def get_ranked_routes(population):
    rank_routes = []
    for _, route in enumerate(population):
        route_distance = get_route_distance(route)
        rank_routes.append([route, route_distance])
    rank_routes = sorted(rank_routes, key=lambda x: x[1])
    return rank_routes

def selection(ranked_population, elite_size):
    selected_routes = []
    for i in range(elite_size):
        selected_routes.append(ranked_population[i][0])
    return selected_routes

def get_mating_pool(selected_routes):
    matingpool = []
    for i in range(len(selected_routes)):
        matingpool.append(selected_routes[i])
    return matingpool

def breed(parent1, parent2):
    gene_a = random.randint(0, len(parent1))
    gene_b = random.randint(0, len(parent1))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    genes_from_parent1 = parent1[start_gene:end_gene + 1]
    child = genes_from_parent1 + [gene for gene in parent2 if gene not in genes_from_parent1]
    return child

 
def breed_population(matingpool, size):
    children = []
    pool = random.sample(matingpool, len(matingpool))
    for i in range(size):
        children.append(matingpool[i])
    for i in range(len(matingpool)):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutation_rate):
    for i, _ in enumerate(individual):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(individual) - 1)
            while i == swap_with:
                swap_with = random.randint(0, len(individual) - 1)
            gene_a = individual[i]
            gene_b = individual[swap_with]
            individual[i] = gene_a
            individual[swap_with] = gene_b
    return individual


def mutate_population(population, mutation_rate):
    mutated_population = []
    for index, _ in enumerate(population):
        mutated_individual = mutate(population[index], mutation_rate)
        mutated_population.append(mutated_individual)
    return mutated_population


def next_generation(population, elite_size, mutation_rate):
    ranked_routes = get_ranked_routes(population)
    selected_routes = selection(ranked_routes, elite_size)
    mating_pool = get_mating_pool(selected_routes)
    children = breed_population(mating_pool, elite_size)
    next_generation = mutate_population(children, mutation_rate)
    return next_generation

def genetic_algorithm(coordinates, size, elite_size, mutation_rate, generations):
    population = create_initial_population(size, coordinates)
    print(f"Initial distance: {get_ranked_routes(population)[0][1]}")
    for _ in range(generations):
        population = next_generation(population, elite_size, mutation_rate)
    print(f"Final distance: {get_ranked_routes(population)[0][1]}")
    best_route = get_ranked_routes(population)[0][0]
    return best_route

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = create_initial_population(popSize, population)
    progress = []
    progress.append(1 / get_ranked_routes(pop)[0][1])
    
    for i in range(0, generations):
        pop = next_generation(pop, eliteSize, mutationRate)
        progress.append(1 / get_ranked_routes(pop)[0][1])
    
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
def solve():
    # number_cities = int(input("Enter number fo cities: "))
    # coordinates = generate_random_coordinates(number_cities)
    number_cities = 12
    coordinates = [[0.190032E-03,-0.285946E-03],    
                    [383.458,-0.608756E-03],[-27.0206,-282.758],
                    [335.751,-269.577], [69.4331,-246.780], 
                    [168.521,31.4012],[320.350,-160.900],
                    [179.933,-318.031],[492.671,-131.563],
                    [112.198,-110.561],[306.320,-108.090],
                    [217.343,-447.089]]

    coordinates_to_cities = {'Aberystwyth': [0.190032E-03,-0.285946E-03],
                                'Brighton': [383.458,-0.608756E-03],
                                'Edinburgh': [-27.0206,-282.758],
                                'Exeter': [335.751,-269.577],
                                'Glasgow': [69.4331,-246.780],
                                'Inverness': [168.521,31.4012],
                                'Liverpool': [320.350,-160.900],
                                'London': [179.933,-318.031],
                                'Newcastle': [492.671,-131.563],
                                'Nottingham': [112.198,-110.561],
                                'Oxford': [306.320,-108.090],
                                'Stratford': [217.343,-447.089]}

    coordinates_to_cities = {(0.190032E-03,-0.285946E-03): 'Aberystwyth',
                                (383.458,-0.608756E-03): 'Brighton',
                                (-27.0206,-282.758): 'Edinburgh',
                                (335.751,-269.577): 'Exeter',
                                (69.4331,-246.780): 'Glasgow',
                                (168.521,31.4012): 'Inverness',
                                (320.350,-160.900): 'Liverpool',
                                (179.933,-318.031): 'London',
                                (492.671,-131.563): 'Newcastle',
                                (112.198,-110.561): 'Nottingham',
                                (306.320,-108.090): 'Oxford',
                                (217.343,-447.089): 'Stratford'}

    POPULATION_SIZE = int(1.2 * 12)
    ELITE_SIZE = int(0.15 * number_cities)
    MUTATION_RATE = 0.4
    EPOCH_NUMBER = 10
    RANDOM_SELECT_RATE = 0.3
    best_route = genetic_algorithm(coordinates, POPULATION_SIZE, ELITE_SIZE, MUTATION_RATE, 50)
    best_route_tuple = [tuple(city) for city in best_route]
    for city in best_route_tuple:
        print(coordinates_to_cities[city], end="->")

def main():
    solve()

main()