import json

def load(name):
    with open(name, "r") as f:
        return json.load(f)

def initial(matrix):
    # Matrix is square
    rows = len(matrix)
    cols = len(matrix[0])
    # For each agent vertix, find the minimal cost edge
    #  and subtract its weight from all weights connected to that agent vertex
    for i in range(rows):
        min_edge_cost = min(matrix[i])
        matrix[i] = [cost - min_edge_cost for cost in matrix[i]]

    # For each task vertex, find the minimal cost edge
    #  and subtrct its weight from all weights connected to that task vertex
    for j in range(cols):
        col_list = [matrix[i][j] for i in range(rows)]
        min_edge_cost = min(col_list)
        for i in range(rows):
            matrix[i][j] = matrix[i][j] - min_edge_cost

def assignment(matrix):
    initial(matrix)

    print_matrix(matrix)

    while True:
        converted = convert_0weight(matrix)
        matched, num_matched = maximum_matching(converted)
        print("{}, {}".format(matched, num_matched))

        if num_matched == len(matrix):
            break
        else:
            iterative_step(matrix)
            break

def convert_0weight(matrix_old):
    # convert 0 weight edges to 1 and non zero weight edges to 0
    matrix = [[1 if cost == 0 else 0 for cost in row] for row in matrix_old]
    return matrix

def maximum_matching(matrix):
    # keep track of applicants assigned to jobs
    # match[i] = agent index assigned to task i
    # -1 means not assigned
    match_list = [-1] * len(matrix[0])
    # count of jobs assigned to agent
    result = 0
    for i in range(len(matrix)):
        # mark all jobs as not seen for the next agent
        seen = [False] * len(matrix)
        # Find if this agent can get a job
        if bpm(i, match_list, seen, matrix):
            result += 1
    return match_list, result

def iterative_step(matrix):
    pass

def bpm(agent, match_list, seen, matrix):
    # try every job
    for j in range(len(matrix[0])):
        if matrix[agent][j] == 1 and not seen[j]:
            seen[j] = True
            # if task j is not assigned to an agent
            # OR if the previously assigned agent for task j (match_list[j])
            #  has an alternate job available

            # since seen[j] is marked as already visited, the recursive call won't assign task j to the current match_list[j] again
            if match_list[j] == -1 or bpm(match_list[j], match_list, seen, matrix):
                match_list[j] = agent
                return True
    return False

def main():
    test = [[1, 4, 5], [5, 7, 6], [5, 8, 8]]
    assignment(test)

def print_matrix(matrix):
    # matrix is square
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=' ')
        print()

if __name__ == "__main__":
    main()