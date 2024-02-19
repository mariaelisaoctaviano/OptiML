import random

errors = []

for super_ in range(1, 11):
    # Definindo a função de aptidão (fitness)
    def fitness_function(x):
        return -(x ** 2)  # Queremos maximizar, então usamos o negativo do quadrado

    # Função para inicializar a população
    def initialize_population(population_size, min_value, max_value):
        return [random.uniform(min_value, max_value) for _ in range(population_size)]

    # Função para avaliar a aptidão de cada indivíduo na população
    def evaluate_population(population):
        return [fitness_function(individual) for individual in population]

    # Função para selecionar indivíduos para reprodução (roleta)
    def selection(population, fitness_scores):
        # Adicionando um deslocamento positivo aos valores de aptidão
        shifted_fitness_scores = [score - min(fitness_scores) + 1 for score in fitness_scores]
        return random.choices(population, weights=shifted_fitness_scores, k=len(population))

    # Função para realizar cruzamento (recombinação)
    def crossover(parent1, parent2):
        # Verificar se os pais são listas
        if not isinstance(parent1, list) or not isinstance(parent2, list):
            return parent1, parent2
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    # Função para aplicar mutação
    def mutate(individual, mutation_rate, min_value, max_value):
        # Verificar se o indivíduo é uma lista
        if not isinstance(individual, list):
            return individual
        mutated_individual = []
        for gene in individual:
            if random.random() < mutation_rate:
                mutated_individual.append(random.uniform(min_value, max_value))
            else:
                mutated_individual.append(gene)
        return mutated_individual

    # Parâmetros do algoritmo
    population_size = 1000
    min_value = -10
    max_value = 10
    mutation_rate = 0.1
    num_generations = 100

    # Inicialização da população
    population = initialize_population(population_size, min_value, max_value)

    # Loop principal do algoritmo evolucionário
    for generation in range(num_generations):
        # Avaliação da população
        fitness_scores = evaluate_population(population)

        # Seleção
        selected_population = selection(population, fitness_scores)

        # Cruzamento
        next_generation = []
        for i in range(0, len(selected_population), 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1, mutation_rate, min_value, max_value))
            next_generation.append(mutate(child2, mutation_rate, min_value, max_value))

        # Atualização da população
        population = next_generation

    # Avaliação final da população
    fitness_scores = evaluate_population(population)

    # Encontrando o melhor indivíduo
    best_individual = population[fitness_scores.index(max(fitness_scores))]

    error = abs(fitness_function(best_individual))
    errors.append(error)

    print(f"Erro na execução {super_}: {error}")
    # De repente prrintar erro médio por iteração e depois o erro médio total

# Calculando o erro médio
mean_error = sum(errors) / len(errors)
print('Erro médio do algoritmo genético ao longo de 10 execuções: {:.5f} %'.format(mean_error))

# Plotando os erros
plt.bar(range(1, 11), errors)
plt.xlabel('Execução')
plt.ylabel('Erro')
plt.title('Erro por Execução - Algoritmo Genético')
plt.show()
