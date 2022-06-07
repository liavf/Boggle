import itertools
from collections import Counter
import time

def get_word_from_path(board, path):
    return "".join([board[cell[0]][cell[1]] for cell in path])

def get_from_location(board, location):
    return board[location[0]][location[1]]

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

def find_length_n_paths(n, board, words):
    paths = []
    for location in get_all_indexes(len(board)):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                               [location], start_letter,
                                               [], words, "path")
        paths.extend(path for path in paths_for_location)
    return paths

def _find_path_helper(start, board, n, curr_path, curr_word, paths,
                      words, find_by):
    if find_by == "path":
        key = curr_path
    else:
        key = curr_word

    if len(key) > n:
        return
    elif len(key) == n:
        if curr_word in words: # count only words from list
            paths.append(curr_path[:])
    else:
        for location in get_neighbors(start, len(board)):
            if location not in curr_path:
                curr_path.append(location)
                curr_word += get_from_location(board, location)
                _find_path_helper(location, board, n, curr_path, curr_word,
                                  paths, words, find_by)
                curr_path.remove(location)
                curr_word = curr_word[:len(curr_word) - 1]
        return paths

def find_length_n_words(n, board, words):
    paths = []
    for location in get_all_indexes(len(board)):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                               [location], start_letter,
                                               [], words, "word")
        paths.extend(path for path in paths_for_location)
    return paths

def max_score_paths(board, words):
    paths_for_score = []
    words_for_score = set()
    max_len = max([len(word) for word in words])
    min_len = min([len(word) for word in words])
    for n in range(max_len, min_len - 1, -1):
        paths = find_length_n_paths(n, board, words)
        for path in paths:
            #todo: return words from recursion to avoid this step
            word = get_word_from_path(board, path)
            if word not in words_for_score:
                paths_for_score.append(path)
                words_for_score.add(word)
    return calculate_score(paths_for_score)

def find_up_to_n_paths(n, board, words):
    paths = []
    for location in get_all_indexes(len(board)):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_up_to_n_paths_helper(location, board, n,
                                                        [location], start_letter,
                                                        [], words)
        paths.extend(path for path in paths_for_location)
    return paths

def _find_up_to_n_paths_helper(start, board, n, curr_path, curr_word, paths,
                        words):
    if len(curr_word) > n:
        return

    if curr_word in words: # count only words from list
        paths.append(curr_path[:])

    for location in get_neighbors(start, len(board)):
        if location not in curr_path:
            curr_path.append(location)
            curr_word += get_from_location(board, location)
            _find_up_to_n_paths_helper(location, board, n, curr_path, curr_word,
                                    paths, words)
            curr_path.remove(location)
            curr_word = curr_word[:len(curr_word) - 1]
    return paths
def max_score_paths_2(board, words):
    paths_for_score = []
    words_for_score = set()
    n = max([len(word) for word in words])
    paths = find_up_to_n_paths(n, board, words)
    paths.sort(key=len, reverse=True)
    for path in paths:
         #todo: return from recursion
        word = get_word_from_path(board, path)
        if word not in words_for_score:
            paths_for_score.append(path)
            words_for_score.add(word)
    return calculate_score(paths_for_score)

# def find_paths_by_word(board, word):
#     paths = []
#     for location in get_all_indexes(len(board)):
#         start_letter = get_from_location(board, location)
#         if start_letter == word[0:]: #start only from relevant locations
#             paths_for_location = _find_path_helper(location, board, n,
#                                                 [location], start_letter,
#                                                 [], [word], "path")
#             paths.extend(path for path in paths_for_location)
#     return paths

# def max_score_paths_faster(board, words):
#     paths_for_score = []
#     words_for_score = set()
#     max_len = max([len(word) for word in words])
#     min_len = min([len(word) for word in words])
#     for n in range(max_len, min_len - 1, -1):
#         #search normaly from every index
#         if n < THRESHOLD:
#             paths = find_length_n_paths(n, board, words)
#             for path in paths:
#                 #todo: return from recursion
#                 word = get_word_from_path(board, path)
#                 if word not in words_for_score:
#                     paths_for_score.append(path)
#                     words_for_score.add(word)
#         else:
#             for word in [word for word in words if len(word) == n]:
#                 paths = find_paths_by_word(board, word).sort(key=len)
#                 if paths:
#                     paths_for_score.append(paths[0]) #only longest path will be added
#     return calculate_score(paths_for_score)

def calculate_score(paths_for_score):
    score = 0
    for path in paths_for_score:
        score += len(path) ** 2
    return score

def get_words(path):
     words = set()
     with open(path, "r") as f:
         for line in f.readlines():
             words.add(line.strip())
     return words

def get_relevant_words(path, board):
    board_counter = sum(board, [])
    words = set()
    with open(path, "r") as f:
        for line in f.readlines():
            word = line.strip()
            to_add = True
            for letter in word:
                if letter in board_counter:
                    board_counter.remove(letter)
                else:
                    to_add = False
                    break
            if to_add:
                words.add(line.strip())
    return words


if __name__ == '__main__':
    #test
    from boggle_board_randomizer import *
    #board = randomize_board()
    board = [['Y', 'A', 'X', 'I'],
     ['M', 'S', 'G', 'T'],
     ['R', 'T', 'P', 'G'],
     ['B', 'S', 'T', 'W']]
    from pprint import pprint
    pprint(board)
    #print(get_neighbors((2,2), len(board)))

    words = get_relevant_words("boggle_dict.txt", board)
    start = time.time()
    print(max_score_paths(board, words))
    first = time.time()
    print(first-start, "seconds")

    print(max_score_paths_2(board, words))
    second = time.time()
    print(second-first, "seconds")
    # words = get_words("boggle_dict.txt")
    # print(max_score_paths(board, words))


