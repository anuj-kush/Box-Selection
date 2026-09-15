"""Deterministic, conservative guillotine packing; no external AI service."""
from itertools import permutations
from math import prod

AXIS_ORDERS = tuple(permutations(range(3)))

def pack(units, bounds):
    """Return a geometric placement witness or None (not proof of infeasibility).

    Try three item orders and six free-space splitting orders. Every residual
    region is disjoint, so placing inside one cannot overlap prior placements.
    Coordinates and dimensions are integer millimetres.
    """
    keys = (lambda u: prod(u["size"]), lambda u: max(u["size"]), lambda u: sum(u["size"]))
    for key in keys:
        ordered = sorted(units, key=lambda u: (-key(u), u["product_id"], u["unit"]))
        for axes in AXIS_ORDERS:
            free = [((0, 0, 0), bounds)]
            placed = []
            for unit in ordered:
                candidates = []
                for i, (origin, space) in enumerate(free):
                    for size in sorted(set(permutations(unit["size"]))):
                        if all(size[a] <= space[a] for a in range(3)):
                            candidates.append((prod(space)-prod(size), origin, size, i))
                if not candidates:
                    break
                _, origin, size, i = min(candidates)
                _, space = free.pop(i)
                placed.append({"product_id": unit["product_id"], "unit": unit["unit"], "position_mm": origin, "size_mm": size})
                # Each cut peels off a slab; subsequent slabs are restricted
                # along already-cut axes, which prevents overlapping regions.
                remaining = list(space)
                for axis in axes:
                    residual = remaining.copy()
                    residual[axis] -= size[axis]
                    start = list(origin)
                    start[axis] += size[axis]
                    if all(d > 0 for d in residual):
                        free.append((tuple(start), tuple(residual)))
                    remaining[axis] = size[axis]
            else:
                return placed
    return None

def select_box(units, total_weight, boxes):
    volume = sum(prod(u["size"]) for u in units)
    checked = []
    for box in sorted(boxes, key=lambda b: (b.cost, prod(b.dimensions), b.pk)):
        reason = None
        if total_weight > box.max_weight_g:
            reason = "weight_exceeded"
        elif volume > prod(box.dimensions):
            reason = "volume_exceeded"
        elif any(not any(all(s[a] <= box.dimensions[a] for a in range(3)) for s in permutations(u["size"])) for u in units):
            reason = "item_dimensions_exceeded"
        if reason:
            checked.append({"box_id": box.pk, "reason": reason})
            continue
        placements = pack(units, box.dimensions)
        if placements is None:
            checked.append({"box_id": box.pk, "reason": "packing_not_found"})
            continue
        return {"status": "recommended", "box": {"id": box.pk, "name": box.name, "internal_dimensions_mm": box.dimensions, "max_weight_g": box.max_weight_g, "cost": str(box.cost)}, "total_weight_g": total_weight, "utilization_percent": round(100 * volume / prod(box.dimensions), 2), "placements": placements, "checked_boxes": checked, "explanation": "Lowest-cost box with a packing found; ties use smaller volume then ID. Heuristic search may miss feasible cheaper boxes."}
    return {"status": "no_recommendation", "checked_boxes": checked, "explanation": "No packing found in active boxes. This is not proof that every arrangement is impossible."}
