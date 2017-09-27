import json
from maximal_match import max_flow, alternating_path, label_match

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

    while True:
        converted = convert_0weight(matrix)
        matched, num_matched = max_flow(converted)

        if num_matched == len(matrix):
            break
        else:
            iterative_step(matrix, converted, matched)
    print(matched)

def adjust_by(i, j, matched_rows, matched_cols, min_val):
    if i in matched_rows and j in matched_cols:
        return min_val
    elif i not in matched_rows and j not in matched_cols:
        return -1 * min_val
    else:
        return 0
    


def convert_0weight(matrix_old):
    # convert 0 weight edges to 1 and non zero weight edges to 0
    matrix = [[1 if cost == 0 else 0 for cost in row] for row in matrix_old]
    return matrix

def min_vertex_cover(matrix, matched):
    # find min vertex cover from maximal matching
    min_vertex = [[], []]
    for i in range(len(matrix)):
        if matched[i] == -1:
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    min_vertex[1].append(j)

    
    for j in range(len(matrix[0])):
        this_matched = False
        coming_from = None
        for i in range(len(matrix)):
            if matched[i] == j:
                this_matched = True
                break
            if matrix[i][j] == 1:
                coming_from = i
        if not this_matched:
            min_vertex[0].append(coming_from)

    return min_vertex


def iterative_step(matrix, converted, matched):
    matched_rows, matched_cols = min_vertex_cover(converted, matched)
    
    # calc min val
    min_val = None
    for i in range(len(matrix)):
        if i not in matched_rows:
            for j in range(len(matrix[0])):
                if j not in matched_cols:
                    if min_val is None:
                        min_val = matrix[i][j]
                    elif matrix[i][j] < min_val:
                        min_val = matrix[i][j]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] += adjust_by(i, j, matched_rows, matched_cols, min_val)


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