from worker.zero_crossings import count_zero_crossings


def test_count_zero_crossings():
    sequence = [1, -1, 1, -1, 1, -1, 0, -1, 0, 1]
    assert count_zero_crossings(sequence) == 6
