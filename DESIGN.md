# Design Decisions and Trade-offs

## Meaning of Suitable

The system chooses the lowest-cost box among boxes for which the algorithm finds a valid geometric packing. Ties are resolved by smaller internal volume, then box ID.

This is an explicit assumption because the supplied brief does not specify whether box cost or unused space should take priority. The system considers box purchase cost, not carrier charges or shipping tariffs.

Dimensions use integer millimetres, and weights use integer grams. Cost uses a decimal field to avoid binary floating-point money comparisons.

Product dimensions, product weights, and box weight capacities must be positive. Box cost may be zero. Field validators provide feedback in the admin interface, while database constraints also protect writes that bypass form validation.

## Physical Assumptions

* Each product unit is represented as a rigid rectangular cuboid.
* Axis-aligned rotations in 90-degree increments are permitted.
* Box dimensions represent internal usable space.
* Products may touch box walls or other products. No additional packing clearance is included.
* Maximum weight capacity means allowable product payload weight, excluding the box’s own weight.
* Each order must fit into one box; splitting an order across multiple boxes is not implemented.
* An order may contain at most 50 individual units.
* Only active boxes are considered.
* Fragility, stacking pressure, physical support, stability, upright-only restrictions, nesting, compression, hazardous-goods rules, and packing materials are not modeled.

A geometrically valid arrangement may still require warehouse judgment about safe handling.

## Why Volume Alone Is Not Enough

Two cubes measuring 6 × 6 × 6 units have a combined volume of 432 cubic units. A box measuring 10 × 10 × 10 units has a volume of 1,000 cubic units.

Although the combined product volume is smaller, the cubes cannot fit together in that box under axis-aligned placement. To avoid overlapping, they must be separated along at least one axis, requiring 12 units along that axis.

Weight, total volume, and individual dimensions are useful preliminary checks. Explicit placement coordinates provide stronger evidence that all products fit together.

## Selection Steps

1. Validate the request and aggregate repeated product quantities.
2. Fetch all requested products together and reject unknown product IDs.
3. Expand quantities into individual units and calculate total product weight and volume.
4. Sort active boxes by cost, internal volume, and ID.
5. Reject boxes that fail weight, total-volume, or individual rotated-dimension checks.
6. Attempt to pack the products into each remaining box.
7. Return the first box with a successful packing, including placement coordinates and reasons for earlier skipped boxes.
8. If no packing is found, return no_recommendation with reasons.

A failed heuristic search is not presented as proof that every possible arrangement is impossible.

## Packing Heuristic

The algorithm begins with one free rectangular region equal to the box interior.

It tries three largest-first item-ordering strategies:

* Product volume.
* Longest product side.
* Sum of the product’s three dimensions.

For each strategy, it tries all six axis orders for splitting free space. This produces at most 18 packing attempts per box. Some attempts may be identical when the ordering strategies produce the same sequence. The search stops as soon as a complete packing is found.

For each product unit, the algorithm:

1. Enumerates its unique dimension permutations.
2. Finds free regions that can contain each orientation.
3. Selects the fitting region with the smallest volume.
4. Resolves ties deterministically using region origin, product orientation, and region index.
5. Places the product at the selected region’s origin.
6. Removes that region and divides its remaining space into up to three non-overlapping rectangular regions.

For an X/Y/Z split, the remaining regions are:

* A right-hand region occupying the remaining X length.
* A back region restricted to the product’s X length.
* A top region restricted to the product’s X and Y lengths.

Other splitting orders apply the same construction in a different axis sequence.

Each product is placed entirely inside a free region, and the replacement regions are disjoint. This construction keeps placements within the box and prevents product overlap.

A seeded randomized test separately checks successful placements for box-boundary containment, non-overlap, and preservation of item dimensions. These checks do not establish that the search finds every feasible packing.

## Limitations of the Heuristic

This is a heuristic rather than an exact 3D bin-packing solver.

The algorithm does not backtrack within an attempt or merge free regions. It can therefore miss valid arrangements.

The result packing_not_found means the algorithm did not find a packing. It differs from a definite weight or volume violation.

If the algorithm misses a feasible arrangement in a cheaper box, it may recommend a more expensive box. The recommendation is therefore the cheapest box with a packing found by this algorithm, not a guaranteed globally optimal choice.

## Weight Capacity and Space Utilization

Weight capacity and space utilization are separate constraints.

For example, the demo Book weighs 400 g, while the Large box has a maximum payload capacity of 5,000 g:

* 12 Books weigh 4,800 g and remain within the weight limit.
* 13 Books weigh 5,200 g and exceed the weight limit.

Consequently, the box cannot accept 13 Books even if unused space remains.

Space utilization is calculated as:

Total product volume / Internal box volume × 100

The system must satisfy both the weight limit and geometric packing requirements.

## Complexity and Operational Limits

Let:

* B be the number of active boxes.
* N be the total number of individual product units.

There are at most 18 packing attempts per box, up to six orientations per product, and O(N) free regions during an attempt.

Treating the fixed attempt and rotation counts as constants, the coarse time-complexity bound is:

O(B × N² + B log B)

The B log B term accounts for sorting the box catalog. Item sorting is covered by the coarser packing bound.

The implementation temporarily stores possible placements in a candidate list. That list uses O(N) space because each free region contributes at most six orientations.

Including product units, placements, free regions, temporary candidates, loaded boxes, and rejection reasons, working space is:

O(N + B)

The 50-unit limit bounds order size, but the box catalog is not capped. Larger catalogs and public traffic would require benchmarking, request limits, and additional resource controls.

## Why There Is No Runtime LLM

The supplied brief permits AI assistance during development but does not explicitly require an LLM in the recommendation process.

Deterministic geometric checks are reproducible, auditable, and work without an external AI service.

A language model could explain a verified recommendation, but it should not override weight limits, dimensions, or calculated placements.

If the complete assignment rubric requires a runtime AI component, that requirement should be confirmed and implemented separately, with deterministic validation and a fallback.

## Future Improvements

Possible improvements include:

* Packing clearance and padding allowances.
* Upright-only and fragile-product rules.
* Physical support and stacking constraints.
* Comparison against an exact solver on small orders to measure missed feasible packings.
* Multi-box order splitting.
* Saved orders and snapshots of dimensions, capacities, and costs for reproducible historical results.
* Box stock availability and reservation.
* Authentication, rate limiting, and a bounded search budget for deployment.

Stock reservation would require transactions and concurrency control. The current recommendation is advisory: it does not reserve inventory or guarantee box availability.
