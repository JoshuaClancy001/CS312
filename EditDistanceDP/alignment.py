import math


class Score:
    def __init__(self, value: int, back_pointer: 'Score', direction: str):
        self.value = value
        self.back_pointer = back_pointer
        self.direction = direction


def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """

    table: dict[tuple[int, int], Score] = {}
    if banded_width == -1: # Space: O(n*m) Time: O(n*m)
        init_regular_base_case(seq1, seq2, indel_penalty, table)  # Space: O(n+m) Time: O(n+m)
        for y in range(1, len(seq1) + 1):
            for x in range(1, len(seq2) + 1):
                fill_table(seq1, seq2, x, y, match_award, indel_penalty, sub_penalty, table)  # Space:O(1) Time:O(1)

    else: # Space: O(kn) Time: O(kn)
        init_banded_base_case(seq1, seq2, banded_width, indel_penalty, table)  # Space: O(k) Time:O(k)
        for y in range(1, len(seq1) + 1):
            for x in range(max(1, y - banded_width), min(len(seq2) + 1, y + banded_width + 1)):
                fill_table(seq1, seq2, x, y, match_award, indel_penalty, sub_penalty, table)  # Space: O(k) Time:O(k)
    aligned_sq1 = ""
    aligned_sq2 = ""
    x = len(seq2)
    y = len(seq1)
    while x > 0 or y > 0: # back trace Space: O(n+m) Time: O(n+m)
        current_box = table[(x, y)]
        if current_box is None:
            break
        if current_box.direction == "diagonal":
            aligned_sq1 = seq1[y - 1] + aligned_sq1
            aligned_sq2 = seq2[x - 1] + aligned_sq2
            x -= 1
            y -= 1
        elif current_box.direction == "left":
            aligned_sq1 = "-" + aligned_sq1
            aligned_sq2 = seq2[x - 1] + aligned_sq2
            x -= 1
        elif current_box.direction == "up":
            aligned_sq1 = seq1[y - 1] + aligned_sq1
            aligned_sq2 = "-" + aligned_sq2
            y -= 1
    return table[(len(seq2), len(seq1))].value, aligned_sq1, aligned_sq2


def init_banded_base_case(seq1: str, seq2: str, banded_width: int, indel_penalty: int,
                          table: dict[tuple[int, int], Score]):
    for y in range(min(len(seq1), banded_width + 1)):
        table[(0, y)] = Score(y * indel_penalty, None, "up")
    for x in range(min(len(seq2), banded_width + 1)):
        table[(x, 0)] = Score(x * indel_penalty, None, "left")


def init_regular_base_case(seq1: str, seq2: str, indel_penalty: int, table: dict[tuple[int, int], Score]):
    for y in range(len(seq1) + 1):
        table[(0, y)] = Score(y * indel_penalty, None, "up")
    for x in range(len(seq2) + 1):
        table[(x, 0)] = Score(x * indel_penalty, None, "left")


def fill_table(seq1: str, seq2: str, x: int, y: int, match_award: int, indel_penalty: int, sub_penalty: int,
               table: dict[tuple[int, int], Score]):
    delete: Score = table.get((x, y - 1), Score(math.inf, None, ""))
    insert: Score = table.get((x - 1, y), Score(math.inf, None, ""))
    replace: Score = table.get((x - 1, y - 1), Score(math.inf, None, ""))

    match_score_value: int = replace.value + match_award
    replace_score_value: int = replace.value + sub_penalty
    insert_score_value: int = insert.value + indel_penalty
    delete_score_value: int = delete.value + indel_penalty
    is_matching: bool = False

    if seq1[y - 1] == seq2[x - 1]:
        is_matching = True
        min_value = min(match_score_value, replace_score_value, insert_score_value, delete_score_value)
    else:
        min_value = min(replace_score_value, insert_score_value, delete_score_value)

    if min_value == match_score_value and is_matching:
        table[(x, y)] = Score(match_score_value, replace, "diagonal")
    elif min_value == replace_score_value:
        table[(x, y)] = Score(replace_score_value, replace, "diagonal")
    elif min_value == insert_score_value:
        table[(x, y)] = Score(insert_score_value, insert, "left")
    else:
        table[(x, y)] = Score(delete_score_value, delete, "up")
