import itertools
from typing import List, Dict, Set, Any, Tuple

Board = List[List[str]]
Location = Tuple[int, int]
Path = List[Location]

PATH_KEYWORD = "path"
WORD_KEYWORD = "word"

def get_from_location(board: Board, location:Location) -> str:
    """
    gets the letter in given location
    """
    x, y = location
    return board[x][y]

def get_word_from_path(board: Board, path: Path) -> str:
    """
    gets word string from path location on board
    """
    if path:
        return "".join([get_from_location(board, cell) for cell in path])
    else:
        return ""

def get_dict_by_length(words: set[str]) -> Dict[int, Set[str]]:
    """
    sorts word dict by lengths, returning a dict with:
    key = length of word, value = list of all words in length
    """
    mydict = {}
    for word in words:
        if len(word) not in mydict:
            mydict[len(word)] = {word}
        else:
            mydict[len(word)].add(word)
    return mydict

def get_all_indexes(board_height: int, board_width: int) -> Location:
    """
    returns all indexes in board
    works as generator
    """
    for x in range(board_height):
        for y in range(board_width):
            yield (x,y)

def in_borders(cell, board: Board) -> bool:
    """
    checks if given cell is within board borders
    """
    x, y = cell
    if (x < 0 or x >= len(board)) or (y < 0 or y >= len(board[0])):
        return False
    else:
        return True

def check_valid(board: Board, path: Path) -> bool:
    """
    checks validity of path - in borders and in neighbors
    """
    valid_path = True
    # path is not empty and first cell is in borders
    if path and in_borders(path[0],board):
        index, next_index = 0, 1
        # continue until length of path
        while next_index < len(path) and valid_path:
            # checks if next cell is in borders and in previous cell neighbor list
            if path[next_index] in get_neighbors(path[index], len(board),
                                                 len(board[0])) \
                    and (in_borders(path[next_index], board)):
                index += 1
                next_index += 1
            else:
                valid_path = False
    else:
        valid_path = False
    return valid_path


def is_valid_path(board: Board, path: Path, words: Set[str]) -> str:
    """
    checks if path is valid and checks if word is in word list
    """
    if check_valid(board, path):
        word = get_word_from_path(board, path)
        if word in words:
            return word
    return None

def get_neighbors(location, board_height: int, board_width: int) -> List:
    """
    gets neighbors of given cell (all directions)
    """
    neighbors = []
    x, y = location
    for dx, dy in itertools.product((0,1,-1),repeat=2):
        if not (dx == dy == 0) and 0 <= x+dx <= board_height - 1 and \
                                              0 <= y+dy <= board_width - 1:
                neighbors.append((x+dx, y+dy))
    return neighbors

def find_length_n_paths(n: int, board: Board, words: Set[str]) -> List[Path]:
    """
    finds all paths that are n length
    """
    paths = []
    for location in get_all_indexes(len(board), len(board[0])):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                               [location], start_letter,
                                               [], words, PATH_KEYWORD, False)
        paths.extend(path for path in paths_for_location)
    return paths

def letter_in_index(curr_word: str, words: Set[str]) -> Set[str]:
    """
    checks if word starts with given start string
    returns only words that work
    """
    all = set()
    for word in words:
        if len(word) >= len(curr_word):
            if word[:len(curr_word)] == curr_word:
                all.add(word)
    return all

def _find_path_helper(start: Location, board: Board, n: int, curr_path: Path,
                      curr_word: str, paths: List[Path], words: Set[str],
                      find_by: str, up_to: bool) -> List[Path]:
    """
    recursive helper function for both n length words and n length paths by key
    find_by - key for checking length - word / path
    up_to - for getting all paths up to a certain number
    """
    if find_by == PATH_KEYWORD:
        key = curr_path
    else:
        key = curr_word

    if curr_word in words:
        if up_to:
            paths.append(curr_path[:])
        elif len(key) == n:
            paths.append(curr_path[:])

    if len(key) <= n:
        for location in get_neighbors(start, len(board), len(board[0])):
            if location not in curr_path:
                curr_path.append(location)
                letter = get_from_location(board, location)
                curr_word += letter
                words_dialeted = letter_in_index(curr_word, words)
                if words_dialeted:
                    _find_path_helper(location, board, n,
                                      curr_path, curr_word,
                                      paths, words_dialeted,
                                      find_by, up_to)
                curr_path.remove(location)
                curr_word = curr_word[:-len(letter)]
    return paths

def find_length_n_words(n: int, board: Board, words: Set[str]) -> List[Path]:
    """
    finds all legal paths whose words are n length
    """
    paths = []
    if n in get_dict_by_length(words):
        words = get_dict_by_length(words)[n]
        for location in get_all_indexes(len(board), len(board[0])):
            start_letter = get_from_location(board, location)
            paths_for_location = _find_path_helper(location, board, n,
                                                   [location], start_letter,
                                                   [], words, WORD_KEYWORD, False)
            paths.extend(path for path in paths_for_location)
        return paths
    else:
        return []

def find_up_to_n_paths(n: int, board, words: Set[str]) -> List[Path]:
    """
    finds all paths up to n length words - for getting all paths up to max length word
    """
    paths = []
    for location in get_all_indexes(len(board), len(board[0])):
        start_letter = get_from_location(board, location)
        paths_for_location = _find_path_helper(location, board, n,
                                                    [location], start_letter,
                                                    [], words, WORD_KEYWORD, True)
        paths.extend(path for path in paths_for_location)
    return paths

def max_score_paths(board: Board, words: Set[str]) -> List[Path]:
    """
    returns paths that lead to max score in game
    """
    words = filter_words_list(board, words)
    if not words:
        return []
    paths_for_score = []
    words_for_score = set()
    n = max([len(word) for word in words])
    paths = find_up_to_n_paths(n, board, words)
    paths = sorted(paths, key=len, reverse=True)
    for path in paths:
        word = get_word_from_path(board, path)
        if word not in words_for_score:
            paths_for_score.append(path)
            words_for_score.add(word)
    return paths_for_score

def get_words(path: str) -> Set[str]:
    """
    gets all words from path
    """
    words = set()
    with open(path, "r") as f:
        for line in f.readlines():
            words.add(line.strip())
    return words

def filter_words_list(board: Board, words: Set[str]) -> Set[str]:
    """
    filters word list only by letter count possibility (not order)
    """
    board_counter = sum(board, [])
    res = set()
    for word in words:
        to_add = False
        word_counter = 0
        for let in board_counter:
            if let in word:
                word_counter += len(let)
                if word_counter >= len(word):
                    to_add = True
                    break
        if to_add:
            res.add(word)
    return res