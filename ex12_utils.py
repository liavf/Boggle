import itertools
from collections import Counter
NEIGHBORS_INDEXES = [0,1,-1]



def get_word_from_path(board, path):
    return "".join([board[cell[0]][cell[1]] for cell in path])

def get_all_indexes(board_length):
    for x in range(board_length):
        for y in range(board_length):
            yield (x,y)

def get_neighbors(location, board_length):
    neighbors = []
    x, y = location
    for dx, dy in itertools.product((0,1,-1),repeat=2):
        if not (dx == dy == 0) and 0 <= x+dx <= board_length - 1 and \
                                              0 <= y+dy <= board_length - 1:
                neighbors.append((x+dx, y+dy))
    return neighbors



def is_valid_path(board, path, words):
    valid_path = True
    if len(path) > 1:
        index, next_index = 0, 1
        while next_index < len(path) and valid_path:
            if path[next_index] in get_neighbors(path[index], len(board)):
                index += 1
                next_index += 1
            else:
                valid_path = False
    if valid_path:
        word = get_word_from_path(board, path)
        if word in words:
            return word
    return None


def find_length_n_paths(n, board, words):
    paths = []
    for location in get_all_indexes(len(board)):
        #print("getting path from", location)
        paths_for_location = _find_path_helper(location, board, n, [location], [], words,
                                       "path")
        paths.extend(path for path in paths_for_location)
    return paths

def _find_path_helper(start, board, n, path, all, words, find_by):
    word = get_word_from_path(board, path)
    if find_by == "path":
        key = path
    else:
        key = word

    if len(key) > n:
        return
    elif len(key) == n:
        if word in words: # count only real words
            all.append(path[:])
    else:
        for location in get_neighbors(start, len(board)):
            if location not in path:
                path.append(location)
                _find_path_helper(location, board, n, path, all, words, find_by)
                path.remove(location)
        return all

def find_length_n_words(n, board, words):
    paths = []
    for location in get_all_indexes(len(board)):
        paths_for_location = _find_path_helper(location, board, n, [location], [], words,
                                       "word")
        if paths_for_location:
            paths.extend(paths_for_location)
    return paths

def max_score_paths(board, words):
    paths_for_score = []
    words_for_score = set()
    max_len = max([len(word) for word in words])
    min_len = min([len(word) for word in words])
    for n in range(max_len, min_len - 1, -1):
        print(n)
        paths = find_length_n_paths(n, board, words)
        print("got paths")
        for path in paths:
            word = get_word_from_path(board, path)
            if word not in words_for_score:
                print(word, path)
                paths_for_score.append(path)
                words_for_score.add(word)
    return calculate_score(paths_for_score)

def calculate_score(paths_for_score):
    score = 0
    for path in paths_for_score:
        score += len(path) ** 2
    return score

# def get_words(path):
#     words = set()
#     with open(path, "r") as f:
#         for line in f.readlines():
#             words.add(line.strip())
#     return words

def get_relevant_words(path, board):
    board_counter = Counter(sum(board, []))
    words = set()
    with open(path, "r") as f:
        for line in f.readlines():
            word = line.strip()
            to_add = True
            word_counter = Counter(word)
            for key in word_counter:
                if word_counter[key] != board_counter[key]:
                    to_add = False
                    break
            if to_add:
                words.add(line.strip())
    return words

if __name__ == '__main__':
    #test
    from boggle_board_randomizer import *
    #board = randomize_board()
    board = [['C', 'Z', 'G', 'I'], ['Y', 'O', 'G', 'U'], ['K', 'Y', 'O', 'S'], ['E', 'E', 'R', 'N']]
    from pprint import pprint
    pprint(board)
    #words = get_words("boggle_dict.txt")
    #print(get_neighbors((2,2), len(board)))
    #words = get_relevant_words("boggle_dict.txt", board)
    #print(max_score_paths(board, words))

