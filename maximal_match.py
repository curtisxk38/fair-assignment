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

def max_flow(matrix):
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

def label_match(matrix, match_list):
    # only bother labeling a match_list that isn't the maximum
    first = None
    for i in range(len(match_list)):
        if match_list[i] == -1:
            first = i
            break
    if first is None:
        return None
    print(first)
    labels = [[-1] * len(matrix), [-1] * len(matrix[0])]
    labels[0][first] = "*"
    # while some node doesn't have a label
    while any(i == -1 for i in labels[0] + labels[1]):
        odd_edge(matrix, labels, match_list)
        even_edge(matrix, labels, match_list)
        print(labels)
        breakthrough(matrix, labels, match_list)

    return labels


def alternating_path(matrix):
    # keep track of whether each agent is matched
    match_list = [-1] * len(matrix)
    # make initial match
    for j in range(matrix[0]):
        if matrix[0][j] == 1:
            match_list[0] = j

    label_match(matrix, match_list)

def odd_edge(matrix, labels, match_list):
    for j in range(len(matrix[0])):
        if labels[1][j] == -1:
            for i in range(len(matrix)):
                if matrix[i][j] == 1 and labels[0][i] != -1 and match_list[i] == -1:
                    labels[1][j] = i
                    break

def even_edge(matrix, labels, match_list):
    for i in range(len(matrix)):
        if labels[0][i] == -1:
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1 and labels[1][j] != -1 and match_list[i] == j:
                    labels[0][i] = j
                    break

def breakthrough(matrix, labels, match_list):
    for j in range(len(matrix[0])):
        if labels[1][j] != -1:
            matched = any(match_list[i] == j for i in range(len(matrix)))
            if not matched:
                next_node = labels[1][j]
                current_is_agent = False
                while next_node != "*":
                    current_is_agent = not current_is_agent
                    label_select = 0 if current_is_agent else 1
                    next_node = labels[label_select][next_node]



def main():
    test = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [0, 1, 0, 0]
    ]
    print(alternating_path(test))