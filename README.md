# AI-Assisted Box Selection System

A Django application that recommends a shipping box for an order based on product dimensions, total weight, box capacity, and box cost.

The system selects the **lowest-cost box for which its packing algorithm finds a valid arrangement**. It provides placement coordinates and explains why earlier candidate boxes were skipped.

AI tools assisted development. The application itself does not call an AI model or require paid services or API keys.

## Features

* Manage products and boxes through Django admin.
* Enter product quantities using a browser form.
* Get recommendations through a JSON API.
* Check weight limits, volume, and individual product dimensions.
* Try product rotations and multiple packing arrangements.
* Display space utilization and placement details.
* Validate order input and explain unsuccessful recommendations.

## Technology Stack

| Component | Technology                                  |
| --------- | ------------------------------------------- |
| Backend   | Python and Django                           |
| Database  | SQLite                                      |
| Frontend  | Django templates, HTML, CSS, and JavaScript |
| Testing   | Django test framework                       |
| Packing   | Deterministic 3D packing heuristic          |

## Requirements

* Python 3.10 or newer.
* pip.
* A terminal and code editor, such as VS Code.

The project was tested in the assistant execution environment with Django 5.2.17. The supported dependency range is specified in requirements.txt.

## Local Setup

### 1. Open the project

Extract the project and open the box-selection folder in VS Code.

Open a terminal in the folder containing manage.py.

### 2. Create a virtual environment

powershell
python -m venv .venv


Check that the environment uses Python 3.10 or newer:

powershell
.venv\Scripts\python.exe --version


### 3. Install dependencies

powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt


### 4. Apply database migrations

powershell
.venv\Scripts\python.exe manage.py migrate


The project includes its initial migration. Running this command creates the required database tables.

### 5. Load the sample catalog

powershell
.venv\Scripts\python.exe manage.py seed_demo


This creates sample products and boxes. Running it again preserves existing records with the same names.

### 6. Create an admin account

powershell
.venv\Scripts\python.exe manage.py createsuperuser


Follow the prompts to enter your account details. This step is optional if you only want to try the sample catalog.

### 7. Start the development server

powershell
.venv\Scripts\python.exe manage.py runserver


Open:

* Application: http://127.0.0.1:8000/
* Admin: http://127.0.0.1:8000/admin/

Keep the terminal running while using the application. Press Ctrl+C to stop the server.

These Windows commands use the virtual environment’s Python directly, so activation is unnecessary.

On macOS or Linux, use .venv/bin/python instead of .venv\Scripts\python.exe.

## Try a Sample Order

With the original sample catalog:

1. Open the application.
2. Set the Book quantity to 2.
3. Leave the other quantities at 0.
4. Click **Recommend box**.

Expected result:

| Field                | Value  |
| -------------------- | ------ |
| Selected box         | Small  |
| Box cost             | 15.00  |
| Total product weight | 800 g  |
| Space utilization    | 59.66% |

Expand **Placement coordinates and decision details** to inspect the complete response.

Results may change if you edit the sample products or boxes.

## How Recommendations Work

1. Validate product IDs and quantities.
2. Merge repeated product rows.
3. Calculate total product weight and volume.
4. Sort active boxes by cost, then internal volume, then ID.
5. Reject boxes that fail weight, volume, or individual-dimension checks.
6. Try to place every product unit inside each remaining box.
7. Return the first box with a successful packing.

The algorithm permits axis-aligned product rotations and tries several item orders and free-space splitting orders.

This is a heuristic: it may miss some valid arrangements. A no_recommendation result means no packing was found, not necessarily that every possible arrangement is impossible.

See DESIGN.md for the complete algorithm, assumptions, and trade-offs.

## Units and Capacity

| Measurement                             | Unit                                                   |
| --------------------------------------- | ------------------------------------------------------ |
| Product and box dimensions              | Millimetres                                            |
| Product weight and box payload capacity | Grams                                                  |
| Cost                                    | Decimal amount in one consistent business currency     |
| Space utilization                       | Percentage of internal box volume occupied by products |

Box dimensions represent internal usable space. Weight capacity represents the allowable product payload.

A box can reach its weight limit before its space is full. For example, 12 sample Books weigh 4,800 g, while 13 weigh 5,200 g. The sample Large box has a 5,000 g limit, so it cannot accept 13 Books even if space remains.

## API Usage

### Endpoint

http
POST /api/recommend/
Content-Type: application/json


### Request Body

json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}


Product IDs must match records in the database. On a fresh database populated only by seed_demo, product ID 1 refers to Book.

### Successful Response

A successful recommendation includes:

* status: recommended.
* box: selected box details and cost.
* total_weight_g: combined product weight.
* utilization_percent: occupied volume percentage.
* placements: position and rotated dimensions of each unit.
* checked_boxes: reasons for earlier skipped boxes.
* explanation: selection policy and heuristic limitation.

If no packing is found, the response contains status: no_recommendation, checked-box reasons, and an explanation.

### CSRF Protection

Django CSRF protection is enabled. The browser form handles the token automatically.

For Postman:

1. Send a GET request to http://127.0.0.1:8000/.
2. Retain the returned csrftoken cookie.
3. Send the POST request with that cookie and an X-CSRFToken header containing the token value.
4. Set Content-Type to application/json.

### Response Codes

| Status code | Meaning                                                                                                           |
| ----------- | ----------------------------------------------------------------------------------------------------------------- |
| 200         | Recommendation returned, or no packing found                                                                      |
| 400         | Invalid JSON, unknown products, unsupported fields, invalid quantities, empty order, or order-size limit exceeded |
| 403         | Missing or invalid CSRF token                                                                                     |
| 405         | HTTP method not allowed                                                                                           |
| 415         | Content type is not application/json                                                                              |

CSRF checks run before the view handles an unsafe request, so a missing token may produce 403 before other validation errors.

### Validation Rules

* Requests must contain a non-empty items list.
* Each item must contain only product_id and quantity.
* Product IDs and quantities must be positive integers.
* Booleans, floats, and numeric strings are rejected.
* Repeated product rows are merged.
* Orders may contain at most 50 total product units.
* Unknown products are rejected rather than skipped.

## Tests

Run the automated test suite:

powershell
.venv\Scripts\python.exe manage.py test --verbosity 2


Run Django’s system checks:

powershell
.venv\Scripts\python.exe manage.py check


The recorded assistant-environment run passed **14 tests**. Coverage includes:

* Product rotation and exact-fit packing.
* A case where sufficient volume does not guarantee a fit.
* Weight limits and cost-based selection.
* Inactive boxes and unknown products.
* Invalid input and repeated product quantities.
* HTTP handling and CSRF protection.
* Database constraints.
* Dimension and volume rejection.

One test generates 100 seeded randomized packing cases. For successful packings, it separately checks box boundaries, non-overlap, and preservation of product dimensions. These checks do not prove that the algorithm finds every possible packing.

Actual captured terminal output is included in TEST_OUTPUT.md. No automated real-browser testing was performed.

After changing the code, rerun the tests and update TEST_OUTPUT.md with the output from the version being submitted.

## Project Files

| File                                      | Purpose                                                                     |
| ------------------------------------------| --------------------------------------------------------------------------- |
| config/settings.py                        | Django settings and database configuration                                  |
| config/urls.py                            | Application and admin routes                                                |
| shipping/models.py                        | Product and box models with validation constraints                          |
| shipping/packing.py                       | Packing algorithm and box selection                                         |
| shipping/views.py                         | Order validation and API responses                                          |
| shipping/admin.py                         | Catalog management through Django admin                                     |
| shipping/templates/shipping/home.html     | Order form and recommendation display                                       |
| shipping/management/commands/seed_demo.py | Sample catalog creation                                                     |
| shipping/tests.py                         | Automated test cases                                                        |
| DESIGN.md                                 | Design assumptions, algorithm, and limitations                              |
| AI_USAGE.md                               | AI tools, prompts, retained or modified outputs, mistakes, and verification |
| TEST_OUTPUT.md                            | Captured test-run output                                                    |
| SUBMISSION_CHECKLIST.md                   | Submission requirements and pending steps                                   |

## Scope and Limitations

* The catalog is stored in SQLite.
* Orders are evaluated without saving order history or customer details.
* Each order must fit into a single box.
* The algorithm does not model padding, fragility, stacking pressure, or physical support.
* Product rotations are unrestricted within axis-aligned orientations.
* Costs represent box purchase prices; carrier charges and currency conversion are not included.
* The recommendation does not reserve box inventory or purchase shipping.
* The demonstration recommendation endpoint is unauthenticated.
* The box catalog size is not capped.

Production deployment would require staff access controls, rate limiting, search-resource limits, production settings, HTTPS, and additional warehouse handling rules.

## AI Usage and Submission

AI assistance is documented in AI_USAGE.md.


## Reference

[Django 5.2 documentation](https://docs.djangoproject.com/en/5.2/)
