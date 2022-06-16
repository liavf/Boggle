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

# board = [['E', 'M', 'AB', 'O'],
#                 ['IN', 'ON', 'AN', 'M'],
#                 ['ST', 'R', 'U', 'TH'],
#                 ['Y', 'ST', 'R', 'W']]
#
# print(get_neighbors((0,0), len(board), len(board[0])))

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

def letter_in_index(curr_word, words) -> Set:
    """ checks if word starts with given start string
    returns only words that work """
    all = set()
    for word in words:
        if len(word) >= len(curr_word):
            if word[:len(curr_word)] == curr_word:
                all.add(word)
    return all

def _find_path_helper(start, board, n, curr_path, curr_word, paths,
                      words, find_by, up_to):
    """ recursive helper function for both n length words and n length paths by key """
    if find_by == "path":
        key = curr_path
    else:
        key = curr_word

    # print(curr_word, words)
    if curr_word in words:
        # print(curr_word,curr_path)
        if up_to:
            # if curr_word == "TESTEES":
            #     print("HI")
            paths.append(curr_path[:])
        elif len(key) == n:
            paths.append(curr_path[:])
    if len(key) <= n:
        # if curr_word == "E":
        #     print(start, len(board), len(board[0]))
        #     print(get_neighbors(start, len(board), len(board[0])))
        for location in get_neighbors(start, len(board), len(board[0])):
            # if curr_word == "E":
            #     print(location)
            # if curr_word == "ABC":
            # print(location)
            if location not in curr_path:
                curr_path.append(location)
                letter = get_from_location(board, location)

                # if curr_word == "E":
                #     print(curr_word, "letter", letter, location)
                curr_word += letter
                # if location == (0,0) or curr_word == "A":
                #     print(letter,curr_word, words)
                # print(curr_word, words)
                # if curr_word == "EON":
                #     print("EON", words)
                #     print("EON" in words)
                words_dialeted = letter_in_index(curr_word, words)
                # print(curr_word, words_dialeted)
                # if curr_word == "EON":
                #     print("EON", words_dialeted)


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
                curr_word = curr_word[:-len(letter)]
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
    # print(n)
    for location in get_all_indexes(len(board), len(board[0])):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                                    [location], start_letter,
                                                    [], words, "word", True)
        # print(paths_for_location)
        paths.extend(path for path in paths_for_location)
    return paths

def max_score_paths(board, words):
    words = filter_words_list(board, words)
    # print(words)
    # print("TESTEES" in words, "HI")
    paths_for_score = []
    words_for_score = set()
    n = max([len(word) for word in words]) + 1
    # print(n)
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
        # if word == "EON":

        to_add = False
        word_copy = "".join(list(word))
        word_counter = 0
        # print(board_counter)
        for let in board_counter:
            if let in word_copy:
                # if word == "TESTEES":
                #     print(let, word_copy)
                word_counter += len(let)
                if word_counter >= len(word):
                    to_add = True
                    break

                # word_copy = word_copy.replace(let, "")
                # # if word == "EON":
                # #     print(let, word_copy)
                # if not word_copy:
                #     to_add = True
                #     break
        # for letter in word:
        #     if letter in board_counter_copy:
        #         board_counter_copy.remove(letter)
        #     else:
        #         to_add = False
        #         break
        if to_add:
            res.add(word)
    # print(res)
    return res

def load_words_dict(file):
    milon = open(file)
    lines = set(line.strip() for line in milon.readlines())
    milon.close()
    return lines

if __name__ == '__main__':

    # board = [['E', 'M', 'AB', 'O'],
    #             ['IN', 'ON', 'AN', 'M'],
    #             ['ST', 'R', 'U', 'TH'],
    #             ['Y', 'ST', 'R', 'W']]
    board = [['A', 'I', 'P', 'H'],
            ['I', 'R', 'S', 'S'],
            ['A', 'E', 'E', 'T'],
            ['T', 'H', 'E', 'R']]
    all_word_from_dict = load_words_dict("boggle_dict.txt")
    # print(max_score_paths(board, all_word_from_dict))

    # [(''.join([board[test_num][i][j] for i, j in path]),
    #   len(path) ** 2) for path in result]
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