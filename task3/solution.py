from typing import List


# Объединяет пересекающиеся или соприкасающиеся интервалы
def merge_time_ranges(timestamps: List[int]) -> List[tuple[int, int]]:
    merged_ranges: List[tuple[int, int]] = []

    raw_intervals = sorted(
        (timestamps[i], timestamps[i + 1]) for i in range(0, len(timestamps), 2)
    )
    for current_start, current_end in raw_intervals:
        if not merged_ranges or current_start > merged_ranges[-1][1]:
            merged_ranges.append((current_start, current_end))
        else:
            previous_start, previous_end = merged_ranges[-1]
            merged_ranges[-1] = (previous_start, max(previous_end, current_end))

    return merged_ranges


# Находит пересечения между каждым интервалом из первого и второго списка
def get_intersection_ranges(
    intervals_a: List[tuple[int, int]], intervals_b: List[tuple[int, int]]
) -> List[tuple[int, int]]:
    intersections = []

    i = j = 0
    while i < len(intervals_a) and j < len(intervals_b):
        start_a, end_a = intervals_a[i]
        start_b, end_b = intervals_b[j]

        overlap_start = max(start_a, start_b)
        overlap_end = min(end_a, end_b)

        if overlap_start < overlap_end:
            intersections.append((overlap_start, overlap_end))

        if end_a < end_b:
            i += 1
        else:
            j += 1

    return intersections


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals["lesson"]
    lesson_interval = [(lesson_start, lesson_end)]

    pupil_intervals = merge_time_ranges(intervals["pupil"])
    tutor_intervals = merge_time_ranges(intervals["tutor"])

    pupil_in_lesson = get_intersection_ranges(pupil_intervals, lesson_interval)
    tutor_in_lesson = get_intersection_ranges(tutor_intervals, lesson_interval)

    total_intervals = get_intersection_ranges(pupil_in_lesson, tutor_in_lesson)
    total_time = sum(end - start for start, end in total_intervals)
    return total_time


tests = [
    {
        "intervals": {
            "lesson": [1594663200, 1594666800],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3117,
    },
    {
        "intervals": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        "answer": 3577,
    },
    {
        "intervals": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3565,
    },
]


if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["intervals"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
