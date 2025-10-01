# Bank Account Example - Unit Testing with Coverage in Python

This Python project demonstrates the use of mocking in Python using a simple Inventory System example. The goal is to test the Inventory class, which depends on functionality that is not implemented yet. Additionally, these functionality will eventually depend on external services that we don't want to invoke every time we run our tests.

## Prerequisites

- **Python 3.6** or later
- **pip** (Python’s package installer)

## Used Libraries

The current tests use pytest. You can use [MagicMock](https://docs.python.org/3/library/unittest.mock.html) to mock what you need. Please read the documentation.

You can also check [https://docs.python.org/3/library/unittest.mock-examples.html](https://docs.python.org/3/library/unittest.mock-examples.html) for additional mocking syntax.

## Getting Started

1. **Clone the Repository**: Clone the project to your local machine.
    ```bash
    git clone <repository-url>
    cd <your-project-directory>
    ```

2. **Create a virtual environment and install requirements**:

```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

3. Run the unit tests

```bash
pytest
```

4. Generate a coverage report

```
coverage run -m pytest
coverage html
```

The first command will generate the coverage report in your terminal. The second will generate an html file in `htmlcov/index.html` which you can view in your browser. This is just to remember what we did before and to realize that inventory isn't tested at all.

## Your Task

You want to add tests for the `Inventory` class in `inventory.py`, but notice how neither DatabaseService nor NotificationService have any concrete implementations yet. Even when these classes are eventually implemented, theywill communicate with external services so we don't want to have their code execute while unit testing inventory.

Your goal is to test that the Inventory class does what it's supposed to do, even though these services are not yet implemented. Accordingly, you will use mocking to implement your tests.

You should be able to get 100% coverage for the Inventory class. You should think about the behavior you want to make sure happens when testing (e.g., when we add inventory, we want to make sure the Inventory class actually tells the DatabaseService class that it should store things in the DB or that it sent notifications when it's supposed to send them but not in other times.)

Go about the task systematically:

1, first explore the code and understand what each class is doing and how the classes interact with each other
2. run the current tests and observe the current coverage
3. take each function in the Inventory class and write tests for it to ensure its coverage and to ensure it covers the different expected behavior based on its specs (i.e., the docstring comments). Remember that it's a good practice to have tests for each "unit" in a separate file so you will need to create a new file `test_inventory.py` for your new tests. 

Use slides 16 - 22 to guide you on what your test might look like.

See [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) for documentation of the mocking library used and which methods and actions are available to you.
