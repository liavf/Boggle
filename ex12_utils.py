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

def get_all_indexes(board_height: int, board_width: int) -> Location:
    """ returns all indexes in board
    generator """
    for x in range(board_height):
        for y in range(board_width):
            yield (x,y)

def in_borders(cell, board: Board) -> bool:
    """ checks if given cell is within board borders """
    x, y = cell
    if (x < 0 or x >= len(board)) or (y < 0 or y >= len(board[0])):
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
            if path[next_index] in get_neighbors(path[index], len(board), len(board[0])) and (in_borders(path[next_index], board)):
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

def get_neighbors(location, board_height: int, board_width: int) -> List:
    """ gets neighbors of given cell (all directions) """
    neighbors = []
    x, y = location
    for dx, dy in itertools.product((0,1,-1),repeat=2):
        if not (dx == dy == 0) and 0 <= x+dx <= board_height - 1 and \
                                              0 <= y+dy <= board_width - 1:
                neighbors.append((x+dx, y+dy))
    return neighbors

def find_length_n_paths(n: int, board: Board, words) -> List[Path]:
    """ finds all paths that are n length """
    paths = []
    for location in get_all_indexes(len(board), len(board[0])):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                               [location], start_letter,
                                               [], words, "path", False)
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
                      words, find_by, up_to):
    """ recursive helper function for both n length words and n length paths by key """
    if find_by == "path":
        key = curr_path
    else:
        key = curr_word

    if curr_word in words:
        # print(curr_word,curr_path)
        if up_to:
            paths.append(curr_path[:])
        elif len(key) == n:
            paths.append(curr_path[:])
    if len(key) <= n:
        for location in get_neighbors(start, len(board), len(board[0])):
            # if curr_word == "ABC":
                # print(location)
            if location not in curr_path:
                curr_path.append(location)
                letter = get_from_location(board, location)
                # if curr_word == "AB":
                    # print(curr_word, "letter", letter, location)
                curr_word += letter
                # if location == (0,0) or curr_word == "A":
                #     print(letter,curr_word, words)
                words_dialeted = letter_in_index(letter,
                                                 len(curr_word) - 1,
                                                 words)
                # if curr_word == "ABC":
                    # print(words_dialeted, n)
                # if location == (0,0):
                #     print(location, words_dialeted)
                if words_dialeted:
                    _find_path_helper(location, board, n,
                                        curr_path, curr_word,
                                        paths, words_dialeted,
                                      find_by, up_to)
                curr_path.remove(location)
                curr_word = curr_word[:-1]
    return paths

def find_length_n_words(n, board, words):
    """ finds all legal paths whose words are n length """
    paths = []
    if n in get_dict_by_length(words):
        words = get_dict_by_length(words)[n]
        for location in get_all_indexes(len(board), len(board[0])):
            start_letter = get_from_location(board, location)
            paths_for_location = _find_path_helper(location, board, n,
                                                   [location], start_letter,
                                                   [], words, "word", False)
            paths.extend(path for path in paths_for_location)
        return paths
    else:
        return []

def find_up_to_n_paths(n: int, board, words):
    """ finds all paths up to n length words - for getting all paths up to max length word"""
    paths = []
    for location in get_all_indexes(len(board), len(board[0])):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                                    [location], start_letter,
                                                    [], words, "word", True)
        paths.extend(path for path in paths_for_location)
    return paths

def max_score_paths(board, words):
    words = filter_words_list(board, words)
    # print(words)
    paths_for_score = []
    words_for_score = set()
    n = max([len(word) for word in words])
    # print(n)
    paths = find_up_to_n_paths(n, board, words)
    paths = sorted(paths, key=len, reverse=True)
    # print(paths)
    for path in paths:
        word = get_word_from_path(board, path)
        if word not in words_for_score:
            paths_for_score.append(path)
            words_for_score.add(word)
    return paths_for_score

def get_words(path):
     words = set()
     with open(path, "r") as f:
         for line in f.readlines():
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
    from boggle_board_randomizer import *
    # #board = randomize_board()
    # board = [['Y', 'A', 'X', 'I'],
    #  ['M', 'S', 'G', 'T'],
    #  ['R', 'T', 'P', 'G'],
    #  ['B', 'S', 'T', 'W']]
    from pprint import pprint
    # pprint(board)
    #
    # words = get_words("boggle_dict.txt")
    # start = time.time()
    # print(max_score_paths(board, words))
    # first = time.time()
    # # print(first-start, "seconds")
    #
    # a = max_score_paths([['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I',
    #                                                                 'G', 'K', 'L'],
    #      ['M', 'N', 'O', 'P']], ('ABC', 'CDE', 'ABCD'))
    # board = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I','G', 'K', 'L'], ['M', 'N', 'O', 'P']]
    # pprint(board)
    # print(a)
    # board = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I','G', 'K', 'L'], ['M', 'N', 'O', 'P']]
    # for location in get_all_indexes(len(board)):
    #     print(location)