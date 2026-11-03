"""Check consistency of asserted cohort relationships without inferring uncertain links."""


class CohortGraphError(ValueError):
    """Contradictory cohort relationships must not be presented as evidence."""


def _require(condition, message):
    if not condition:
        raise CohortGraphError(message)


def validate_cohort_graph(links, known_overlaps=()):
    """Validate (left, right, relationship) edges; subset points from child to superset."""
    links = tuple(links)
    known_overlaps = tuple(known_overlaps)
    parents = {}

    def find(population):
        parents.setdefault(population, population)
        if parents[population] != population:
            parents[population] = find(parents[population])
        return parents[population]

    def union(left, right):
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parents[max(left_root, right_root)] = min(left_root, right_root)

    for left, right, relationship in links:
        if relationship == "same":
            union(left, right)

    subset_graph = {}
    distinct_pairs = []
    for left, right, relationship in links:
        left_root, right_root = find(left), find(right)
        if relationship == "distinct_within_program":
            _require(left_root != right_root,
                     "contradictory cohort map: populations are both same and distinct")
            distinct_pairs.append((left_root, right_root))
        elif relationship == "subset":
            _require(left_root != right_root,
                     "contradictory subset cycle through same populations")
            subset_graph.setdefault(left_root, set()).add(right_root)
            subset_graph.setdefault(right_root, set())

    visiting = set()
    visited = set()

    def visit(population):
        _require(population not in visiting, "contradictory subset cycle")
        if population in visited:
            return
        visiting.add(population)
        for superset in subset_graph.get(population, ()):
            visit(superset)
        visiting.remove(population)
        visited.add(population)

    for population in subset_graph:
        visit(population)

    reachable = {
        population: {population, *subset_graph.get(population, ())}
        for population in set(subset_graph) |
        {root for pair in distinct_pairs for root in pair} |
        {find(population) for pair in known_overlaps for population in pair}
    }
    for middle in sorted(reachable):
        for population in sorted(reachable):
            if middle in reachable[population]:
                reachable[population].update(reachable[middle])

    for left, right in distinct_pairs:
        _require(not any(left in descendants and right in descendants
                         for descendants in reachable.values()),
                 "contradictory cohort map: distinct populations share a known subset")
        _require(not any(
            (left in reachable[overlap_left] and right in reachable[overlap_right]) or
            (right in reachable[overlap_left] and left in reachable[overlap_right])
            for overlap_left, overlap_right in (
                (find(a), find(b)) for a, b in known_overlaps
            )
        ), "contradictory cohort map: distinct populations contradict documented overlap")
