## I Learn :


# What problem I can solve from this project ?

From this project, I learned how algorithms can solve practical warehouse problems. Before starting, I did not realise that selecting 
a shipping box required more than checking total volume and weight. I learned how product rotation, placement and overlap checks 
affect whether items fit together. I also learned to separate recommendation logic from Django views, validate inputs and understand 
that a heuristic can miss a valid packing arrangement.


# Why must dimensions and weights use consistent units?

I learned that dimensions and weights must use consistent units so the system makes correct comparisons.example: comparing a product
weighing 500 grams directly with a box capacity of 2 kilograms would incorrectly suggest that the product is too heavy. Converting 
500 grams to 0.5 kilograms gives the correct result. The same applies to dimensions when checking fit and calculating volume.


# How would padding space and empty-box weight affect the recommendation ?

I learned that padding reduces the space available for products, so an item that fits exactly without padding may require a larger
box.example: a 20 × 10 × 10 cm item needs 22 × 12 × 12 cm of internal space if we add 1 cm of padding on every side.
Empty-box weight matters if the weight limit applies to the entire shipment. In that case, we must add product weight, padding weight,
and box weight. If the limit applies only to the contents, we exclude the empty box’s weight.

# What information should the Product, Box Order and OrderItem models store ?

I learned how to organize the data into four related models:

Product: Stores the product’s ID, name, length, width, height and weight.
Box: Stores the box’s ID, name, internal dimensions, maximum weight capacity and cost.
Order: Stores the order’s ID and creation date.
OrderItem: Connects an order to a product and stores the quantity ordered.
This structure allows one order to contain multiple products and the same product to appear in different orders.

# Should an order preserve product measurements when the product is updated  ?

if we need consistent historical records. I learned that an OrderItem can store a snapshot of the product’s dimensions and weight when 
the order is confirmed. Later product updates would then affect new orders without changing the measurements used for existing orders.
For a basic implementation, using current product measurements is simpler, but recalculating an older order could produce a different 
box recommendation.

# Why are total weight, total volume and individual fit insufficient to prove that all items fit together ?

I learned that these checks do not consider how items are arranged together. Weight checks capacity, volume checks total space and 
individual fit checks each item separately. None of them guarantees a non-overlapping arrangement.
example: two 2 × 2 × 2 cm cubes have a combined volume of 16 cm³, less than a 3 × 3 × 3 cm box’s 27 cm³. Each cube fits 
individually, but placing both requires at least 4 cm along one axis, which the box does not provide.
That is why we need actual placement checks to confirm that all items fit together.

# How does simple stacking differ from a 3D packing heuristic  ?

I learned that simple stacking places items one above another and checks whether their footprints fit and their combined height stays within the box. It is easy to implement but can miss arrangements where items fit side by side.

A 3D packing heuristic tries different positions and rotations while checking boundaries and preventing overlaps. It can use the available space more effectively, but it is more complex and does not guarantee finding every possible valid arrangement.

# what I Understand through 12 Books Examle ?

The example with 12 books helped me understand that one book fitting inside a box and having enough total volume are not sufficient.
All 12 books must fit together without overlapping or extending beyond the box’s boundaries. Earlier, I thought checking weight and 
volume was enough. I understand the importance of rotation, quantity and actual placement.



# Why should packing logic be separate from Django views ?

I learned that Django views should handle requests, validate input and return responses, while a separate service handles the packing 
calculations. This makes the algorithm easier to understand, modify and test without sending HTTP requests. It also lets us reuse the 
same packing logic in an API, a management command or a background task without duplicating code.

# How does in_bulk() help avoid unnecessary database queries?

I learned that in_bulk() fetches multiple products together and returns a dictionary keyed by their IDs. For a small order, this 
usually takes one database query instead of a separate query for each product. We can then access each product from that dictionary 
without querying the database again.

# Which test cases verify rotation, exact fits, weight limits and multiple quantities?  

I learned to test these scenarios:

Rotation: A 4 × 3 × 2 cm item should fit in a 2 × 4 × 3 cm box after rotation.
Exact fit: An item matching the box’s internal dimensions should fit when no padding is required. An item exceeding a boundary should 
fail.
Weight limits: Test total weight below, exactly equal to and above capacity. The first two should pass the weight check; the third 
should fail.
Multiple quantities: Two 2 × 2 × 2 cm cubes should fit in a 4 × 2 × 2 cm box, but three should fail. The calculation must include 
every unit’s weight and volume.
For successful results, I would also verify that every unit is placed inside the box without overlaps.

# What did I learn and which part was hardest to understand?  

From this project, I learned that selecting a shipping box requires checking dimensions, weight, rotation and how items fit together.
I also learned how to structure Django models, separate packing logic from views and test edge cases.

The hardest part for me was understanding the 3D packing logic, especially choosing item positions and preventing overlaps. A key 
lesson was that enough total volume does not guarantee a fit and a heuristic failing to find an arrangement does not mean packing is 
impossible.
