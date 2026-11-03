from collections import deque
from collections.abc import Callable
import typing

T = typing.TypeVar("T")


def bfs(
    start: T,
    is_done: Callable[[T], bool],
    legal_moves: Callable[[T], [tuple[T, int]]],
    sort: bool = False,
    final_position: T = list(),
    break_first=True,
):
    """Breadth-First Search to find a shortest path
    start is a position,
    is_done evaluates a position to determine if it's the goal,
    legal_moves returns legal moves from that position and their costs
    sort if queue should be sorted by steps (e.g. when some steps are cheaper)
    final_position to store the last position for retrieval
    """
    queue = deque([(start, 0)])
    seen = {start}
    result = -1
    while len(queue) > 0:
        p, s = queue.popleft()
        if is_done(p):
            if break_first:
                result = s
                final_position.append(p)  # ugly trick
                break
            else:
                if result == -1 or s < result:
                    result = s
                    final_position.append(p)  # even uglier
                    continue
        moves = legal_moves(p)
        for m, c in moves:
            if m not in seen:
                seen.add(m)
                queue.append((m, s + c))
        if sort:
            queue = deque(sorted(list(queue), key=lambda x: x[1]))
    return result
