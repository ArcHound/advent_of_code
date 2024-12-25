from __future__ import annotations


class Interval:
    start: int
    end: int
    label: str

    def __init__(self, start: int, end: int, label: str = "bad"):
        self.start = start
        self.end = end
        self.label = label

    def __str__(self):
        return f"Interval(start={self.start}, end={self.end}, label={self.label})"

    def __repr__(self):
        return f"Interval(start={self.start}, end={self.end}, label={self.label})"

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
            and self.label == other.label
        )

    def length(self) -> int:
        return self.end - self.start

    def contains(self, other: Interval) -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlap_other(self, other: Interval) -> bool:
        return (
            self.contains(other)
            or other.contains(self)
            or (self.start > other.start and self.start > other.end)
            or (self.end > other.start and self.end < other.end)
        )

    @classmethod
    def overlap(cls, a: Interval, b: Interval) -> bool:
        return (
            a.contains(b)
            or b.contains(a)
            or (a.start > b.start and a.start < b.end)
            or (a.end > b.start and a.end < b.end)
        )

    @classmethod
    def least_common_intervals(
        cls, list_a: list[Interval], list_b: list[Interval]
    ) -> list[Interval]:
        """If you have two full sets of intervals over the same space (e.g. 0,inf), this partitions the space so that you are able to read the space and for each subinterval you can judge whether it belongs to a or b (or both)"""
        start_points = list(set([x.start for x in list_a] + [x.start for x in list_b]))
        end_points = list(set([x.end for x in list_a] + [x.end for x in list_b]))
        points = sorted(start_points + end_points)
        intervals = list()
        for i in range(0, len(points), 2):
            intervals.append(Interval(points[i], points[i + 1]))
        return intervals

    @classmethod
    def label_mask(cls, list_a: list[Interval], mask: list[Interval]) -> None:
        for x in list_a:
            for y in mask:
                if y.contains(x):
                    x.label = y.label
                    break

    @classmethod
    def fill_holes(cls, list_a: list[Interval], label: str = "bad") -> list[Interval]:
        s = sorted(list_a, key=lambda a: a.start)
        to_append = list()
        for i in range(len(list_a) - 1):
            if s[i].end + 1 != s[i + 1].start:
                to_append.append(Interval(s[i].end + 1, s[i + 1].start - 1, label))
        return sorted(list_a + to_append, key=lambda a: a.start)

    @classmethod
    def normalize(cls, list_a: list[Interval], label: str = "bad") -> list[Interval]:
        """adds interval from 0 to first point, adds interval from last point to infinity"""
        intervals = list()
        s = sorted(list_a, key=lambda a: a.start)
        for i in range(len(list_a)):
            a = s[i]
            if i == 0 and a.start != 0:
                intervals.append(Interval(0, a.start - 1, label))
            intervals.append(a)
            if i == len(list_a) - 1 and a.end != float("inf"):
                intervals.append(Interval(a.end + 1, float("inf"), label))
        return intervals

    @classmethod
    def find_intervals(cls, list_a: list[Interval], b: Interval) -> list[Interval]:
        return [i for i in list_a if b.contains(i)]
