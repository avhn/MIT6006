from collections import deque
import rubik


def track_path(move):
    ''' Track back path from current move '''
    path = list()
    while move[0]:
        path.append(move[1])
        move = move[0]
    return path[::-1]


def bfs(start, end):
    if start == end:
        return []

    # every position linked to previous
    # (parent, twist, pos)
    moves = deque()
    moves.append((None, None, start))

    # maximum 14 quarter twists
    for i in range(14):
        # use up oldest move, get parent
        parent = moves.popleft()

        # add up childs
        for twist in rubik.quarter_twists:
            position = rubik.perm_apply(twist, parent[2])
            move = (parent, twist, position)
            moves.append(move)

            if position == end:
                return track_path(moves[-1])


def path(position, parents):
    ''' Returns path as list, regarding forward bfs '''
    result = list()
    while True:
        move = parents[position]
        if move is None:
            return result[::-1]
        result.append(move[0])
        position = move[1]


def two_way_bfs(start, end):
    if start == end:
        return []

    # initialize moves for backward bfs'
    forward_moves = dict()
    backward_moves = dict()
    for move in rubik.quarter_twists:
        forward_moves[move] = move
        backward_moves[rubik.perm_inverse(move)] = move

    # item format
    # next_position: (twist, position)
    forward_parents = {start: None}
    backward_parents = {end: None}

    # set indicators for forward and backward
    # (moves, parents, other parents)
    forward = (forward_moves, forward_parents, backward_parents)
    backward = (backward_moves, backward_parents, forward_parents)
    
    # every depth level ends with None as indicator
    queue = deque([(start, forward), (end, backward), None])

    for i in range(7):
        while True:
            vertex = queue.popleft()
            if vertex is None:
                # next depth level
                queue.append(None)
                break

            position = vertex[0]
            moves, parents, other_parents = vertex[1]

            for move in moves:
                next_position = rubik.perm_apply(move, position)

                if next_position in parents:
                    # do not bother with cycles
                    continue

                parents[next_position] = (moves[move], position)
                queue.append((next_position, vertex[1]))

                if next_position in other_parents:
                    forward_path = path(next_position, forward_parents)
                    backward_path = path(next_position, backward_parents)
                    return forward_path + backward_path[::-1]


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    return two_way_bfs(start, end)
