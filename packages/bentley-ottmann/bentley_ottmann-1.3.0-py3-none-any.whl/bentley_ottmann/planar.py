from itertools import (chain,
                       product)
from typing import (Callable,
                    Dict,
                    Sequence,
                    Set,
                    Tuple)

from ground.base import (Relation as _Relation,
                         get_context as _get_context)
from ground.hints import (Contour as _Contour,
                          Point as _Point,
                          Segment as _Segment)

from .core import (bentley_ottmann as _bentley_ottmann,
                   shamos_hoey as _shamos_hoey)
from .core.utils import (all_unique as _all_unique,
                         pairwise as _pairwise,
                         to_sorted_pair as _to_sorted_pair)


def edges_intersect(contour: _Contour) -> bool:
    """
    Checks if polygonal contour has self-intersection.

    Based on Bentley-Ottmann algorithm.

    Time complexity:
        ``O((len(segments) + len(intersections)) * log len(segments))``
    Memory complexity:
        ``O(len(contour))``
    Reference:
        https://en.wikipedia.org/wiki/Sweep_line_algorithm

    :param contour: contour to check.
    :returns: true if contour is self-intersecting, false otherwise.

    .. note::
        Consecutive equal vertices like ``Point(2, 0)`` in

        .. code-block:: python

            Contour([Point(0, 0), Point(2, 0), Point(2, 0), Point(2, 2)])

        will be considered as self-intersection,
        if you don't want them to be treated as such
        -- filter out before passing as argument.

    >>> from ground.base import get_context
    >>> context = get_context()
    >>> Contour, Point = context.contour_cls, context.point_cls
    >>> edges_intersect(Contour([Point(0, 0), Point(2, 0), Point(2, 2)]))
    False
    >>> edges_intersect(Contour([Point(0, 0), Point(2, 0), Point(1, 0)]))
    True
    """
    vertices = contour.vertices
    if len(vertices) < 3:
        raise ValueError('Contour {contour} is degenerate.'
                         .format(contour=contour))
    if not _all_unique(vertices):
        return True
    context = _get_context()
    segment_cls = context.segment_cls
    edges = [segment_cls(vertices[index - 1], vertices[index])
             for index in range(len(vertices))]

    def non_neighbours_intersect(edge_id: int,
                                 other_edge_id: int,
                                 last_edge_index: int = len(edges) - 1
                                 ) -> bool:
        return (other_edge_id - edge_id > 1
                and (edge_id != 0 or other_edge_id != last_edge_index))

    non_overlap_relations = (_Relation.CROSS, _Relation.DISJOINT,
                             _Relation.TOUCH)
    flatten = chain.from_iterable
    return any(
            len(event.segments_ids) > 1
            or any(relation not in non_overlap_relations
                   or any(non_neighbours_intersect(segment_id,
                                                   other_segment_id)
                          for segment_id in event.segments_ids
                          for other_segment_id in flatten(other_segments_ids))
                   for relation, other_segments_ids in event.relations.items())
            for event in _bentley_ottmann.sweep(edges,
                                                context=context))


def segments_intersect(segments: Sequence[_Segment]) -> bool:
    """
    Checks if segments have at least one intersection.

    Based on Shamos-Hoey algorithm.

    Time complexity:
        ``O(len(segments) * log len(segments))``
    Memory complexity:
        ``O(len(segments))``
    Reference:
        https://en.wikipedia.org/wiki/Sweep_line_algorithm

    :param segments: sequence of segments.
    :returns: true if segments intersection found, false otherwise.

    >>> from ground.base import get_context
    >>> context = get_context()
    >>> Point, Segment = context.point_cls, context.segment_cls
    >>> segments_intersect([])
    False
    >>> segments_intersect([Segment(Point(0, 0), Point(2, 2))])
    False
    >>> segments_intersect([Segment(Point(0, 0), Point(2, 0)),
    ...                     Segment(Point(0, 2), Point(2, 2))])
    False
    >>> segments_intersect([Segment(Point(0, 0), Point(2, 2)),
    ...                     Segment(Point(0, 0), Point(2, 2))])
    True
    >>> segments_intersect([Segment(Point(0, 0), Point(2, 2)),
    ...                     Segment(Point(2, 0), Point(0, 2))])
    True
    """
    return _shamos_hoey.sweep(segments,
                              context=_get_context())


def segments_cross_or_overlap(segments: Sequence[_Segment]) -> bool:
    """
    Checks if at least one pair of segments crosses or overlaps.

    Based on Bentley-Ottmann algorithm.

    Time complexity:
        ``O((len(segments) + len(intersections)) * log len(segments))``
    Memory complexity:
        ``O(len(segments))``
    Reference:
        https://en.wikipedia.org/wiki/Sweep_line_algorithm

    :param segments: sequence of segments.
    :returns: true if segments overlap or cross found, false otherwise.

    >>> from ground.base import get_context
    >>> context = get_context()
    >>> Point, Segment = context.point_cls, context.segment_cls
    >>> segments_cross_or_overlap([])
    False
    >>> segments_cross_or_overlap([Segment(Point(0, 0), Point(2, 2))])
    False
    >>> segments_cross_or_overlap([Segment(Point(0, 0), Point(2, 0)),
    ...                            Segment(Point(0, 2), Point(2, 2))])
    False
    >>> segments_cross_or_overlap([Segment(Point(0, 0), Point(2, 2)),
    ...                            Segment(Point(0, 0), Point(2, 2))])
    True
    >>> segments_cross_or_overlap([Segment(Point(0, 0), Point(2, 2)),
    ...                            Segment(Point(2, 0), Point(0, 2))])
    True
    """
    return any(len(event.segments_ids) > 1
               or any(relation is not _Relation.DISJOINT
                      and relation is not _Relation.TOUCH
                      for relation in event.relations)
               for event in _bentley_ottmann.sweep(segments,
                                                   context=_get_context()))


def segments_intersections(segments: Sequence[_Segment]
                           ) -> Dict[_Point, Set[Tuple[int, int]]]:
    """
    Returns mapping between intersection points
    and corresponding segments indices.

    Based on Bentley-Ottmann algorithm.

    Time complexity:
        ``O((len(segments) + len(intersections)) * log len(segments))``
    Memory complexity:
        ``O(len(segments) + len(intersections))``
    Reference:
        https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm

    >>> from ground.base import get_context
    >>> context = get_context()
    >>> Point, Segment = context.point_cls, context.segment_cls
    >>> segments_intersections([]) == {}
    True
    >>> segments_intersections([Segment(Point(0, 0), Point(2, 2))]) == {}
    True
    >>> segments_intersections([Segment(Point(0, 0), Point(2, 0)),
    ...                         Segment(Point(0, 2), Point(2, 2))]) == {}
    True
    >>> (segments_intersections([Segment(Point(0, 0), Point(2, 2)),
    ...                          Segment(Point(0, 0), Point(2, 2))])
    ...  == {Point(0, 0): {(0, 1)}, Point(2, 2): {(0, 1)}})
    True
    >>> (segments_intersections([Segment(Point(0, 0), Point(2, 2)),
    ...                          Segment(Point(2, 0), Point(0, 2))])
    ...  == {Point(1, 1): {(0, 1)}})
    True

    :param segments: sequence of segments.
    :returns:
        mapping between intersection points and corresponding segments indices.
    """
    result = {}
    context = _get_context()

    def to_intersections(first_start: _Point,
                         first_end: _Point,
                         second_start: _Point,
                         second_end: _Point,
                         relation: _Relation,
                         intersector
                         : Callable[[_Point, _Point, _Point, _Point], _Point]
                         = context.segments_intersection
                         ) -> Tuple[_Point, ...]:
        if relation is _Relation.TOUCH or relation is _Relation.CROSS:
            return intersector(first_start, first_end, second_start,
                               second_end),
        else:
            _, first_point, second_point, _ = sorted(
                    [first_start, first_end, second_start, second_end])
            return first_point, second_point

    for event in _bentley_ottmann.sweep(segments,
                                        context=context):
        segment_start, segment_end = event.original_start, event.original_end
        segments_ids = event.segments_ids
        if len(segments_ids) > 1:
            ids_pairs = set(_pairwise(segments_ids))
            result.setdefault(segment_start, set()).update(ids_pairs)
            result.setdefault(segment_end, set()).update(ids_pairs)
        for relation, other_segments_ids in event.relations.items():
            for other_segment_ids in other_segments_ids:
                ids_pairs = {_to_sorted_pair(segment_id, other_segment_id)
                             for segment_id, other_segment_id
                             in product(segments_ids, other_segment_ids)}
                other_segment = segments[other_segment_ids[0]]
                for point in to_intersections(segment_start, segment_end,
                                              other_segment.start,
                                              other_segment.end, relation):
                    result.setdefault(point, set()).update(ids_pairs)
    return result
