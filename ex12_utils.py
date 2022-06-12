import itertools
from typing import List, Dict, Set, Any, Tuple
from collections import Counter
import time

Board = List[List[str]]
Location = Tuple[int, int]
Path = List[Location]

def get_from_location(board: Board, location:Location) -> str:
    """ gets the letter in given location """
    return board[location[0]][location[1]]

def get_word_from_path(board: Board, path: Path) -> str:
    """ gets word string from path location on board """
    if path:
        return "".join([get_from_location(board, cell) for cell in path])
    else:
        return ""



def get_dict_by_length(words: Dict) -> Dict[int, List[str]]:
    """ sorts word dict by lengths, returning a dict with:
    key = length of word, value = list of all words in length """
    mydict = {}
    for word in words:
        if len(word) not in mydict:
            mydict[len(word)] = [word]
        else:
            mydict[len(word)].append(word)
    return mydict

def get_all_indexes(board_length: int) -> Location:
    """ returns all indexes in board
    generator """
    for x in range(board_length):
        for y in range(board_length):
            yield (x,y)

def in_borders(cell, board: Board) -> bool:
    """ checks if given cell is within board borders """
    x, y = cell
    if (x < 0 or x >= len(board)) or (y < 0 or y >= len(board)):
        return False
    else:
        return True

def is_valid_path(board: Board, path: Path, words) -> str:
    """ checks if path is valid in borders and if word is in list """
    valid_path = True
    if path and in_borders(path[0], board): # path is not empty and first cell is in borders
        index, next_index = 0, 1
        while next_index < len(path) and valid_path: # continue until length of path
            # checks if next cell is in borders and in previous cell neighbor list
            if path[next_index] in get_neighbors(path[index], len(board)) and (in_borders(path[next_index], board)):
                index += 1
                next_index += 1
            else:
                valid_path = False
    else:
        valid_path = False
    if valid_path:
        word = get_word_from_path(board, path)
        if word in words:
            return word
    return None

def get_neighbors(location, board_length: int) -> List:
    """ gets neighbors of given cell (all directions) """
    neighbors = []
    x, y = location
    for dx, dy in itertools.product((0,1,-1),repeat=2):
        if not (dx == dy == 0) and 0 <= x+dx <= board_length - 1 and \
                                              0 <= y+dy <= board_length - 1:
                neighbors.append((x+dx, y+dy))
    return neighbors

def find_length_n_paths(n: int, board: Board, words) -> List[Path]:
    """ finds all paths that are n length """
    paths = []
    for location in get_all_indexes(len(board)):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                               [location], start_letter,
                                               [], words, "path")
        paths.extend(path for path in paths_for_location)
    return paths

def letter_in_index(char, index, words) -> Set:
    """ checks if word starts with given start string
    returns only words that work """
    all = set()
    for word in words:
        if len(word) > index:
            if word[index] == char:
                all.add(word)
    return all

def _find_path_helper(start, board, n, curr_path, curr_word, paths,
                      words, find_by):
    """ recursive helper function for both n length words and n length paths by key """
    if find_by == "path":
        key = curr_path
    else:
        key = curr_word

    if len(key) == n:
        if curr_word in words: # count only words from list
            paths.append(curr_path[:])

    elif len(key) < n:
        for location in get_neighbors(start, len(board)):
            if location not in curr_path:
                curr_path.append(location)
                curr_word += get_from_location(board, location)
                # words = start_word(curr_word, words)
                # if words:
                _find_path_helper(location, board, n, curr_path, curr_word,
                                      paths, words, find_by)
                curr_path.remove(location)
                curr_word = curr_word[:-1]
    return paths

def find_length_n_words(n, board, words):
    """ finds all legal paths whose words are n length """
    paths = []
    if n in get_dict_by_length(words):
        words = get_dict_by_length(words)[n]
        for location in get_all_indexes(len(board)):
            start_letter = get_from_location(board, location)
            paths_for_location = _find_path_helper(location, board, n,
                                                   [location], start_letter,
                                                   [], words, "word")
            paths.extend(path for path in paths_for_location)
        return paths
    else:
        return []

# def max_score_paths_2(board, words):
#     """"""
#     paths_for_score = []
#     words_for_score = set()
#     max_len = max([len(word) for word in words])
#     min_len = min([len(word) for word in words])
#     for n in range(max_len, min_len - 1, -1):
#         paths = find_length_n_paths(n, board, words)
#         for path in paths:
#             word = get_word_from_path(board, path)
#             if word not in words_for_score:
#                 paths_for_score.append(path)
#                 words_for_score.add(word)
#     return calculate_score(paths_for_score)

def calculate_score(paths_for_score):
    score = 0
    for path in paths_for_score:
        score += len(path) ** 2
    return score

def find_up_to_n_paths(n: int, board, words):
    """ finds all paths up to n length words - for getting all paths up to max length word"""
    paths = []
    for location in get_all_indexes(len(board)):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_up_to_n_paths_helper(location, board, n,
                                                        [location], start_letter,
                                                        [], words)
        paths.extend(path for path in paths_for_location)
    return paths

# def filter_words(words, curr_path):
#     for word in words.copy():
#         if word[:len(curr_word)] == curr_word:
#             words.remove(word)
#     return words

def _find_up_to_n_paths_helper(start, board, n, curr_path, curr_word, paths,
                        words):
    """ same as before but gets all length paths and not specific one """
    if curr_word in words: # count only words from list
        # if len(curr_word) in paths:
        #     paths[len(curr_word)].append(curr_word)
        # else:
         paths.append(curr_path[:])

    elif len(curr_word) <= n:
        for location in get_neighbors(start, len(board)):
            if location not in curr_path:
                curr_path.append(location)
                letter = get_from_location(board, location)
                curr_word += letter
                words_dialeted = letter_in_index(letter, len(curr_word) - 1,
                                              words)
                if words:
                    _find_up_to_n_paths_helper(location, board, n, curr_path, curr_word,
                                            paths, words_dialeted)
                curr_path.remove(location)
                curr_word = curr_word[:-1]
    return paths

def max_score_paths(board, words):
    words = filter_words_list(board, words)
    print("done1")
    paths_for_score = []
    words_for_score = set()
    n = max([len(word) for word in words])
    paths = find_up_to_n_paths(n, board, words)
    print("done2")
    paths = sorted(paths, key=len, reverse=True)
        # .sort(key=len, reverse=True)
    # for path_len in paths:
    #     for path in paths[path_len]:
    for path in paths:
        word = get_word_from_path(board, path)
        if word not in words_for_score:
            paths_for_score.append(path)
            words_for_score.add(word)
    return paths_for_score

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
            board_counter_copy = board_counter.copy()
            for letter in word:
                if letter in board_counter_copy:
                    board_counter_copy.remove(letter)
                else:
                    to_add = False
                    break
            if to_add:
                words.add(line.strip())
    return words

def filter_words_list(board: Board, words: set):
    board_counter = sum(board, [])
    res = set()
    for word in words:
        to_add = True
        board_counter_copy = board_counter.copy()
        for letter in word:
            if letter in board_counter_copy:
                board_counter_copy.remove(letter)
            else:
                to_add = False
                break
        if to_add:
            res.add(word)
    return res

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

    # print(max_score_paths_2(board, words))
    # second = time.time()
    # print(second-first, "seconds")
    # words = get_words("boggle_dict.txt")
    # print(max_score_paths(board, words))


