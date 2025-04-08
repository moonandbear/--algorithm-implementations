import heapq

def calculate_inversions(node):
    inversions = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if int(node[i]) > int(node[j]) and node[j] != '0':
                inversions += 1
    return inversions

def heuristic_zero(node, goal):
    return 0

def heuristic_misplaced(node, goal):
    return sum(node[i] != goal[i] for i in range(9))

def heuristic_manhattan(node, goal):
    manhattan_distance = 0
    for i in range(9):
        if node[i] != '0':
            row_goal = int(goal.index(node[i]) / 3)
            col_goal = int(goal.index(node[i]) % 3)
            row_current = int(i / 3)
            col_current = int(i % 3)
            manhattan_distance += abs(row_goal - row_current) + abs(col_goal - col_current)
    return manhattan_distance

def expand_node(node):
    expand = {
        0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
        3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
        6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
    }
    expanded_nodes = []
    zero_index = node.index("0")
    for move in expand[zero_index]:
        new_node = list(node)
        new_node[zero_index], new_node[move] = new_node[move], new_node[zero_index]
        expanded_nodes.append("".join(new_node))
    return expanded_nodes

def a_star(start, goal, heuristic):
    opened = []
    closed = set()
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    heapq.heappush(opened, (f_score[start], start))

    while opened:
        current = heapq.heappop(opened)[1]

        if current == goal:
            path = [current]
            while current in parent:
                current = parent[current]
                path.append(current)
            path.reverse()
            return path, closed

        closed.add(current)

        for neighbor in expand_node(current):
            tentative_g_score = g_score[current] + 1
            if neighbor in closed and tentative_g_score >= g_score.get(neighbor, 0):
                continue

            if tentative_g_score < g_score.get(neighbor, 0) or neighbor not in [i[1] for i in opened]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(opened, (f_score[neighbor], neighbor))

    return "No solution found."

def main():
    start = input("请输入初始状态(从左至右，从上到下，如：102345678)：")
    goal = input("请输入目标状态(从左至右，从上到下，如：123456780)：")
    heuristic_choice = int(input("请选择启发式函数：\n1. h(x)=0\n2. h(x) = 数码错误位置和\n3. h(x) = 数码错误位置曼哈顿距离和\n"))

    heuristic_functions = {
        1: heuristic_zero,
        2: heuristic_misplaced,
        3: heuristic_manhattan
    }

    if start == goal:
        print("初始状态和目标状态一致！")
        return

    if calculate_inversions(start) % 2 != calculate_inversions(goal) % 2:
        print("该目标状态不可达！")
        return

    heuristic_function = heuristic_functions.get(heuristic_choice)

    result, closed = a_star(start, goal, heuristic_function)
    if isinstance(result, list):
        print("搜索节点数:", len(result))
        print("最佳路径节点数:", len(result) - 1)
        print("遍历路径节点数:", len(closed))
        print("求解效率:", len(result) / len(closed))
        print("最佳路径:")
        for state in result:
            print(state[:3])
            print(state[3:6])
            print(state[6:])
            print()
    else:
        print(result)

if __name__ == "__main__":
    main()
