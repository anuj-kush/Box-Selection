# Box Recommendation System — Test Cases

## 1. Purpose and execution status

Verify order validation, geometric packing, box selection, database constraints, and result explanations for the Django hiring assignment.

**Total: 44 test cases.** All cases are **Not run** in this document. Expected results are specifications, not evidence of successful execution. No project test results have been supplied for this test suite.

## 2. Assumptions and preconditions

- Dimensions are length × width × height in centimetres; box dimensions are internal.
- Weights are kilograms and costs are rupees. Convert consistently if the implementation stores grams.
- Each order must fit in one box. Products are rigid rectangular items, with six axis-aligned orientations allowed.
- These cases use zero padding and compare product weight alone with box capacity. These provisional policies require confirmation against the submitted implementation.
- Rank successful boxes by cost, internal volume, then ascending stable box ID.
- Unless stated otherwise, product weight is 1 kg, box capacity is 10 kg, and box cost is ₹20. Only the boxes specified for a case are available; mark them active if active filtering is retained.
- Each case starts with isolated data. Replace example product ID 1 with the ID of its saved fixture.
- For API cases, use the configured recommendation URL; its path has not been provided. Send POST and Content-Type: application/json unless testing a different method or content type.
- Supply valid CSRF handling when enforcement is enabled, so requests reach the view.
- Strict JSON fields, duplicate-row merging, and the 50-unit limit reflect the shared view. They are implementation policies, not universal packing requirements.
- Database cases describe the proposed integrity rules; confirm they exist in the final models.

## 3. Packing and recommendation

For each row, create the specified products and boxes, submit the order, and inspect the recommendation and placement details.

| ID | Scenario | Test data / steps | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- | --- |
| TC01 | Single item fits | Product 2×2×2, 1 kg, quantity 1; box 3×3×3, capacity 2 kg. | Recommend the box with one valid placement. | — | Not run |
| TC02 | Rotation required | Product 4×3×2, quantity 1; box 2×4×3. | Find a valid rotated placement and recommend the box. | — | Not run |
| TC03 | Exact dimensional fit | Product and box both 4×3×2. | Accept the exact fit under the zero-padding policy. | — | Not run |
| TC04 | Item exceeds dimensions | Product 5×3×2; box 4×3×2. | Reject because no allowed rotation fits. | — | Not run |
| TC05 | Weight below capacity | Product 1×1×1 weighing 1.9 kg; box 2×2×2, capacity 2 kg. | Pass the weight check and recommend the box. | — | Not run |
| TC06 | Weight equals capacity | Product 1×1×1 weighing 2 kg; box 2×2×2, capacity 2 kg. | Accept the weight boundary and recommend the box. | — | Not run |
| TC07 | Weight above capacity | Product 1×1×1 weighing 2.001 kg; box 2×2×2, capacity 2 kg. | Reject because total weight exceeds capacity. | — | Not run |
| TC08 | Multiple units fit | Two 2×2×2 cubes; box 4×2×2. | Return two distinct non-overlapping placements. | — | Not run |
| TC09 | Quantity exceeds volume | Three 2×2×2 cubes; box 4×2×2. | Reject: total volume 24 cm³ exceeds box volume 16 cm³. | — | Not run |
| TC10 | Volume and individual fit insufficient | Two 2×2×2 cubes; box 3×3×3. | No recommendation. Each cube fits alone and total volume passes, but no joint arrangement fits. A heuristic may report packing_not_found rather than claiming an exhaustive proof. | — | Not run |
| TC11 | Different products | One 3×2×2 item and one 1×2×2 item; box 4×2×2. | Find a valid arrangement containing both products. | — | Not run |
| TC12 | Cheapest valid box | Product 1×1×1; fitting boxes 2×2×2 at ₹20 and 3×3×3 at ₹30. | Select the ₹20 box. | — | Not run |
| TC13 | Cheapest box unsuitable | Product 2×2×2; box 1×1×1 at ₹10 and box 3×3×3 at ₹20. | Reject the ₹10 box and select the ₹20 box. | — | Not run |
| TC14 | Equal costs, different volumes | Product 1×1×1; boxes 4×4×4 and 3×3×3, both ₹20. | Select the 3×3×3 box. | — | Not run |
| TC15 | Equal costs and volumes | Product 1×1×1; identical 2×2×2 boxes, both ₹20, with IDs 7 and 3. | Select ID 3. If fixtures use different IDs, select the smaller saved ID. | — | Not run |
| TC16 | Deterministic output | Repeat TC15, reversing the box iterable supplied to the service. | Same selected box and placement arrangement. | — | Not run |
| TC17 | No available boxes | Valid product and quantity; no eligible boxes. | Clear no_suitable_box result, not an unhandled exception. | — | Not run |
| TC18 | Every box fails | Product 3×3×3 weighing 2 kg; box 2×2×2 with capacity 10 kg and box 4×4×4 with capacity 1 kg. | No recommendation; explain geometric/volume and weight rejection reasons. | — | Not run |
| TC19 | Quantity totals | Three units, each 2×3×4 and 0.5 kg; box 10×10×10. | Total volume 72 cm³ and total weight 1.5 kg; every unit included. | — | Not run |

## 4. Request validation

Where a case lists multiple invalid inputs, execute each separately and record each outcome. Valid requests may return either a recommendation or a normal no-suitable-box result unless a fitting box is explicitly provided.

| ID | Scenario | Test data / steps | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- | --- |
| TC20 | Valid JSON request | Save product ID 1, size 1×1×1, weight 1 kg, and box 2×1×1 with capacity 2 kg. POST `{"items":[{"product_id":1,"quantity":2}]}`. | HTTP 200 with a successful recommendation and two placements. | — | Not run |
| TC21 | Empty order | POST `{"items":[]}`. | HTTP 400 with an input-validation message. | — | Not run |
| TC22 | Unknown product | Submit a positive product ID absent from the database, quantity 1. | HTTP 400 identifying the unknown ID. | — | Not run |
| TC23 | Zero quantity | Submit existing product ID with quantity 0. | HTTP 400. | — | Not run |
| TC24 | Negative quantity | Submit existing product ID with quantity -1. | HTTP 400. | — | Not run |
| TC25 | Invalid quantity types | Submit quantities `1.5`, `"2"`, `true`, and `null` separately. | HTTP 400 for every input. | — | Not run |
| TC26 | Invalid product IDs | Submit IDs `0`, `-1`, `"1"`, and `true` separately, quantity 1. | HTTP 400 for every input. | — | Not run |
| TC27 | Required field missing | Submit `{"items":[{"product_id":1}]}`. | HTTP 400 because quantity is missing. | — | Not run |
| TC28 | Unexpected fields | Add `"extra":1` to a valid top-level object, then to an item in a separate request. | HTTP 400 for both requests under the strict schema. | — | Not run |
| TC29 | Wrong JSON structure | Submit `[]`, `null`, and `{"items":"invalid"}` separately. | HTTP 400 for each request. | — | Not run |
| TC30 | Malformed JSON | Send incomplete body `{"items":`. | HTTP 400 with an invalid-JSON message. | — | Not run |
| TC31 | Unsupported content type | POST an otherwise valid body using Content-Type: text/plain. | HTTP 415 when the request reaches the view. | — | Not run |
| TC32 | Unsupported method | Send GET to the recommendation endpoint. | HTTP 405. | — | Not run |
| TC33 | Duplicate product rows | Product 1×1×1, 1 kg; box 5×1×1, capacity 5 kg. Submit the same product in rows with quantities 2 and 3. | Merge to five units; total weight 5 kg and volume 5 cm³; return five valid placements. | — | Not run |
| TC34 | Exactly 50 units | Submit an existing product with quantity 50. | Pass quantity validation; packing outcome depends on available boxes. | — | Not run |
| TC35 | More than 50 units | Submit an existing product with quantity 51. | HTTP 400 under the current unit limit. | — | Not run |
| TC36 | Duplicates exceed unit limit | Submit the same product in rows with quantities 30 and 21. | HTTP 400 after aggregation to 51 units. | — | Not run |
| TC37 | Product ID out of range | Submit product ID 9223372036854775808, quantity 1. | HTTP 400 under the shared signed-64-bit ID check. | — | Not run |

## 5. Database integrity and packing-result validation

For database constraints, attempt each invalid write inside an isolated transaction and roll it back. A form-validation failure alone does not demonstrate database enforcement. Use otherwise valid fields. For result checks, reuse successful fixtures such as TC08 and TC11.

| ID | Scenario | Test data / steps | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- | --- |
| TC38 | Nonpositive dimensions | Attempt to save 0 and -1 separately for each product dimension and each internal box dimension. | Database constraints reject each invalid write. | — | Not run |
| TC39 | Nonpositive weights/capacity | Attempt product weights 0 and -1 and box capacities 0 and -1 separately. | Database constraints reject each invalid write. | — | Not run |
| TC40 | Negative cost | Attempt to save a box with cost -1. | Reject negative cost. Zero-cost policy is a separate documented decision. | — | Not run |
| TC41 | Complete placements and rotations | Inspect successful TC08 and TC11 results; compare placements with expanded order units and original dimensions. | Every unit appears exactly once; each placed size is a permitted permutation of its original dimensions. | — | Not run |
| TC42 | Box boundaries | Inspect every position and rotated size in successful TC08 and TC11 results. | On every axis, position ≥ 0 and position + size ≤ internal box dimension. | — | Not run |
| TC43 | No overlaps | Check every pair of placements in successful TC08 and TC11 results. | Each pair is separated on at least one axis. Face/edge contact is allowed; positive-volume intersection is not. | — | Not run |
| TC44 | Accurate heuristic explanation | Inspect the packing failure response from TC10 and success explanations from recommendation cases. | Heuristic failure says packing was not found, without claiming exhaustive search. Success describes the cheapest box with a valid packing found, not guaranteed global optimality. | — | Not run |

## 6. Recording execution results

- Replace the Actual result dash with the observed status, response, calculation, or database exception. Include a screenshot/log reference if useful.
- Set Status to Pass only when every expected check succeeds; otherwise use Fail and record the discrepancy.
- Use Blocked when setup or missing functionality prevents execution. For cases with multiple inputs, record all outcomes before assigning an overall status.
- Record the tested commit/version, Python and Django versions, database, execution date, and tester below. These facts have not been provided.

| Execution detail | Value |
| --- | --- |
| Commit / application version | To be recorded |
| Python version | To be recorded |
| Django version | To be recorded |
| Database | To be recorded |
| Test date | To be recorded |
| Tester | To be recorded |

## 7. Current execution summary

| Total | Pass | Fail | Blocked | Not run |
| --- | --- | --- | --- | --- |
| 44 | 0 | 0 | 0 | 44 |

This document contains test specifications only. It does not assert that the final Django project implements all proposed constraints or passes these cases.
