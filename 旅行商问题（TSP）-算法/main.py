import numpy as np
import random
import matplotlib.pyplot as plt

# 城市坐标数据
cities = {
    1: (116.46, 39.92), 2: (117.2, 39.13), 3: (121.48, 31.22), 4: (106.54, 29.59),
    5: (91.11, 29.97), 6: (87.68, 43.77), 7: (106.27, 38.47), 8: (111.65, 40.82),
    9: (108.33, 22.84), 10: (126.63, 45.75), 11: (125.35, 43.88), 12: (123.38, 41.8),
    13: (114.48, 38.03), 14: (112.53, 37.87), 15: (101.74, 36.56), 16: (117, 36.65),
    17: (113.6, 34.76), 18: (118.78, 32.04), 19: (117.27, 31.86), 20: (120.19, 30.26),
    21: (119.3, 26.08), 22: (115.89, 28.68), 23: (113, 28.21), 24: (114.31, 30.52),
    25: (113.23, 23.16), 26: (121.5, 25.05), 27: (110.35, 20.02), 28: (103.73, 36.03),
    29: (108.95, 34.27), 30: (104.06, 30.67), 31: (106.71, 26.57), 32: (102.73, 25.04),
    33: (114.1, 22.2), 34: (113.33, 22.13)
}

# 遗传算法参数设置
POP_SIZE = 500  # 种群规模
CROSS_RATE = 0.8  # 交叉概率
MUTATE_RATE = 0.8  # 变异概率
N_GENERATIONS = 20000  # 最大迭代步数

# 计算城市之间的距离
def calc_distance(city1, city2):
    return np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# 计算路径的总距离
def get_total_distance(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += calc_distance(cities[path[i]], cities[path[i+1]])
    total_distance += calc_distance(cities[path[-1]], cities[path[0]])  # 回到起点
    return total_distance

# 初始化种群
def init_population():
    population = []
    for _ in range(POP_SIZE):
        path = list(cities.keys())
        random.shuffle(path)
        population.append(path)
    return population

# 轮盘赌选择
def select(population, fitness):
    idx = np.random.choice(np.arange(len(population)), size=POP_SIZE, replace=True, p=fitness/fitness.sum())
    return [population[i] for i in idx]

# 交叉
def crossover(parent1, parent2):
    if np.random.rand() < CROSS_RATE:
        cross_point = np.random.randint(0, len(parent1))
        child1 = parent1[:cross_point]
        child2 = [city for city in parent2 if city not in child1]
        child = child1 + child2
        return child
    else:
        return parent1

# 变异
def mutate(child):
    for i in range(len(child)):
        if np.random.rand() < MUTATE_RATE:
            swap_idx = np.random.randint(0, len(child))
            child[i], child[swap_idx] = child[swap_idx], child[i]
    return child

# 遗传算法
def genetic_algorithm(num_iterations):
    population = init_population()
    best_path = []
    best_distance = float('inf')
    for generation in range(num_iterations):
        fitness = np.array([1 / get_total_distance(path) for path in population])
        if 1 / fitness.max() < best_distance:
            best_path = population[np.argmax(fitness)]
            best_distance = 1 / fitness.max()
        population = select(population, fitness)
        for i in range(len(population)):
            parent1 = population[i]
            parent2 = population[np.random.randint(0, POP_SIZE)]
            child = crossover(parent1, parent2)
            child = mutate(child)
            population[i] = child
    return best_path, best_distance

# 主程序
if __name__ == "__main__":
    num_iterations = int(input("请输入迭代次数（按回车键确认）："))
    if num_iterations > N_GENERATIONS:
        num_iterations = N_GENERATIONS

    best_path = None
    best_distance = float('inf')
    for iteration in range(num_iterations):
        path, distance = genetic_algorithm(1)
        if distance < best_distance:
            best_path = path
            best_distance = distance

        # 打印每次迭代的最佳适应度
        print(f"Iteration {iteration + 1}: Best fitness = {1 / best_distance}")

    print("最短路径值:", best_distance)
    print("最优个体:", best_path)

    # 绘制路径图
    x = [cities[city][0] for city in best_path]
    y = [cities[city][1] for city in best_path]
    x.append(x[0])  # 回到起点
    y.append(y[0])
    plt.figure()
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('TSP Problem Solution')
    plt.show()
