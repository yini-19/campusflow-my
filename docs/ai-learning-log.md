# CampusFlow — Individual AI Learning Log

**Fellow:** YIYAKAZAH NICODEMUS
**Role:** Engineer A
**Project:** CampusFlow — AI-Native Engineering Sprint

---

## Interaction #1 — Managing Ticket Status and Valid Transitions

### Problem

I needed to understand how to enforce ticket lifecycle rules in CampusFlow. A ticket should move through `open`, `in_progress`, and `resolved`. An unassigned ticket must not move into `in_progress`, and a resolved ticket must be explicitly reopened before it can be modified again.

### My initial understanding

I understood that a ticket's status describes its current state, but I was not sure how to prevent invalid transitions. I also needed to understand how to check a ticket's current state before updating it.

### Prompt to AI

"Explain how to implement a state transition system in Python using a small example unrelated to a helpdesk application. Show how to prevent invalid transitions, check the current state before updating it, and test the behavior. Do not write my CampusFlow implementation for me."

### Useful AI guidance

I learned that a state transition function should check the current state and the requested next state before changing anything. If the transition is invalid, it should raise an exception and leave the original state unchanged.

For example, consider a simple machine that can be turned on or off:

```python
def change_power_state(current_state, new_state):
    allowed_transitions = {
        "off": ["on"],
        "on": ["off"],
    }

    if new_state not in allowed_transitions.get(current_state, []):
        raise ValueError("Invalid power-state transition.")

    return new_state
```

This example only allows `off` to change to `on`, or `on` to change to `off`.

### My independent experiment/test

I planned to test three cases:

1. Change the state from `off` to `on`.
2. Change the state from `on` to `off`.
3. Attempt to change the state from `off` to `sleep`.

I predicted that the first two operations would succeed and the third would raise a `ValueError`.

### Verification source or result

[Record the actual output from running the experiment and whether each result matched the prediction.]

Reference: Python documentation — https://docs.python.org/3/tutorial/errors.html

### Decision

I accepted the principle of validating transitions before making changes. I will apply it to CampusFlow by checking the existing ticket status and assignment before updating the ticket.

### Related file/commit

* File: `campusflow/workflow.py`
* Test: [Add actual status-transition test name]
* Commit or PR: [Add actual commit SHA or PR link]

### What I can now explain without AI

A state transition function must validate the current state and requested next state before updating a record. In CampusFlow, an unassigned ticket cannot move into `in_progress`, and a resolved ticket must be explicitly reopened before further modification. Tests should confirm both valid and invalid transitions.

---

## Interaction #2 — Sorting Tickets by Priority and Numeric ID

### Problem

CampusFlow must display unresolved tickets in priority order: critical, high, medium, and low. Tickets with the same priority must be sorted by their numeric ticket IDs, with earlier IDs first. I needed to understand how to implement this without accidentally sorting priority names alphabetically.

### My initial understanding

I knew Python could sort lists using `sorted()`, but I was unsure how to apply a custom priority order and then use a second condition to break ties.

### Prompt to AI

"Teach me how Python's `sorted()` function and sorting keys work. Use an unrelated example of sorting tasks by importance and then by task number. Explain why alphabetical sorting may give the wrong order and give me a small experiment to verify the result. Do not use CampusFlow code."

### Useful AI guidance

I learned that a sorting key can return a tuple containing multiple values. Python sorts by the first value and then uses the next value when the first values are equal.

For example:

```python
tasks = [
    {"number": 3, "importance": "normal"},
    {"number": 2, "importance": "urgent"},
    {"number": 1, "importance": "urgent"},
]

importance_order = {
    "urgent": 0,
    "normal": 1,
    "low": 2,
}

ordered_tasks = sorted(
    tasks,
    key=lambda task: (
        importance_order[task["importance"]],
        task["number"],
    ),
)

print(ordered_tasks)
```

The dictionary converts importance levels into numeric ranks, while the second key sorts tasks with equal importance by their task numbers.

### My independent experiment/test

I planned to run the example and predict that the urgent task numbered 1 would appear before the urgent task numbered 2, followed by the normal task numbered 3.

I would then change the task numbers and importance levels to confirm that both sorting conditions work correctly.

### Verification source or result

[Record the actual output and confirm whether the tasks appeared in the expected order.]

Reference: Python documentation — https://docs.python.org/3/howto/sorting.html

### Decision

I accepted the custom sorting-key approach after verifying the example. For CampusFlow, I will use an explicit priority ranking instead of sorting priority names alphabetically. I will also ensure that resolved tickets are excluded before returning the work queue.

### Related file/commit

* File: `campusflow/workflow.py`
* Test: [Add actual queue-ordering test name]
* Commit or PR: [Add actual commit SHA or PR link]

### What I can now explain without AI

Python's `sorted()` can use a tuple as a sorting key to apply multiple ordering rules. In CampusFlow, the first key will represent priority, and the second will represent the numeric ticket ID. This produces the required order even when multiple tickets have the same priority.

---

## Interaction #3 — Testing Reports and Empty Data

### Problem

CampusFlow must report the total number of tickets and the breakdown by status and priority. The reporting function must also work when the ticket collection is empty.

I needed to understand how to count values in a list of dictionaries and how to test both normal and empty cases.

### My initial understanding

I knew that Python loops could count records, but I was not sure how to organize the results into a dictionary or how to ensure that statuses and priorities with no tickets still appeared with a count of zero.

### Prompt to AI

"Explain how to count categories in a list of dictionaries in Python. Use an unrelated example involving library books grouped by availability. Show how to handle an empty list and how to test the expected counts with unittest. Give me a small experiment instead of writing my project function."

### Useful AI guidance

I learned that a loop can count records by category. Initializing expected categories with zero ensures that categories with no matching records are still represented in the result.

Example:

```python
def count_books(books):
    counts = {
        "available": 0,
        "borrowed": 0,
    }

    for book in books:
        status = book["status"]
        counts[status] += 1

    return counts
```

For an empty list, the function returns:

```python
{
    "available": 0,
    "borrowed": 0,
}
```

For a list containing two available books and one borrowed book, the counts should be two and one, respectively.

### My independent experiment/test

I planned to run the function with:

1. An empty list.
2. A list containing two available books and one borrowed book.
3. A list containing only borrowed books.

I predicted that the counts would be zero for both categories in the first case, two and one in the second, and zero and the total number of books in the third.

I would verify the results using assertions in a small `unittest.TestCase`.

### Verification source or result

[Record the actual test output, including whether all assertions passed.]

Reference: Python documentation — https://docs.python.org/3/library/unittest.html

### Decision

I accepted the approach of initializing the category counts before counting records. I will use the same principle for CampusFlow reports so every supported status and priority has a count, even when no tickets belong to that category.

### Related file/commit

* File: `campusflow/reports.py`
* Test: [Add actual report test name]
* Commit or PR: [Add actual commit SHA or PR link]

### What I can now explain without AI

A report can count tickets by examining each ticket's status and priority. Initializing all supported categories with zero makes the output consistent and ensures the report works when there are no tickets. I will test both populated and empty ticket collections.

---

## Final Reflection

These three learning interactions helped me understand state transitions, multi-condition sorting, and report generation in Python.

As Engineer B, I will apply these concepts to ticket assignment, lifecycle management, the unresolved-ticket queue, and reporting. I will verify my implementation with automated tests and review Engineer A's code to ensure that our modules work together.

### Evidence Checklist

* [ ] I ran the state-transition experiment and recorded the actual result.
* [ ] I ran the sorting experiment and verified the ordering.
* [ ] I ran the report-counting experiment and recorded the test results.
* [ ] I updated the test names and related file paths to match my implementation.
* [ ] I added actual commit SHAs or PR links where available.
* [ ] I can explain all three concepts in my own words.
* [ ] I documented at least one AI suggestion that I independently corrected, improved, or rejected after verification.


# CampusFlow — Individual AI Learning Log

**Fellow:** Michael Bulus
**Role:** Engineer B
**Project:** CampusFlow — AI-Native Engineering Sprint

---

## Interaction #1 — JSON Persistence in Python

**Problem:**

I needed to understand how CampusFlow can save support tickets to a JSON file and load them again when the application restarts. I also needed to understand the difference between `json.dump()` and `json.load()`.

**My initial understanding:**

I knew that JSON stores data in a file, but I was not sure how Python converts dictionaries and lists into JSON or how it retrieves the saved information. I also thought `json.dump()` and `json.load()` might perform the same operation.

**Prompt to AI:**

"Explain `json.dump()`, `json.load()` and JSON persistence with examples. Use a small Python example unrelated to CampusFlow. Explain how data is saved to a file and loaded again, and give me a small experiment I can run to verify the result."

**Useful AI guidance:**

I learned that Python's `json` module provides different functions for writing and reading JSON data.

* `json.dump(data, file)` converts Python data into JSON and writes it to a file.
* `json.load(file)` reads JSON from a file and converts it back into Python data.
* JSON persistence means saving data so it can be recovered after a program stops.

Example:

```python
import json

student = {
    "name": "Ada",
    "score": 85
}

with open("student.json", "w", encoding="utf-8") as file:
    json.dump(student, file)

with open("student.json", "r", encoding="utf-8") as file:
    loaded_student = json.load(file)

print(loaded_student)
```

Expected output:

```text
{'name': 'Ada', 'score': 85}
```

**My independent experiment/test:**

I planned to run the example and predict that the loaded dictionary would contain the same values as the original dictionary. I would then change the score, save the dictionary again, and reload it to check whether the new value was preserved.

**Verification source or result:**

[Record the actual output from your experiment and confirm whether the saved and loaded values matched.]

Reference: Python documentation — https://docs.python.org/3/library/json.html

**Decision:**

I accepted the explanation after checking the Python documentation and running the example. I understood that saving data and loading data are separate operations.

**Related file/commit:**

* File: `campusflow/storage.py`
* Test: `test_save_and_load_tickets` (planned test name; replace with the actual test name)
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`json.dump()` saves Python data to a JSON file, while `json.load()` reads that file and recreates the corresponding Python data. CampusFlow needs both so tickets are not lost when the application closes. I also need to test that the saved tickets can be loaded correctly after restarting the program.

---

## Interaction #2 — Python Exceptions and Input Validation

**Problem:**

CampusFlow must reject invalid inputs, such as a blank ticket title, zero affected users, or an unknown ticket ID. I needed to understand how Python exceptions help handle these errors without crashing the application or changing ticket data incorrectly.

**My initial understanding:**

I knew that invalid input could cause a problem, but I was not sure when to use `raise` and when to use `try` and `except`. I also wanted to understand how to show a useful error message to the user.

**Prompt to AI:**

"Explain Python exceptions, `raise`, `try`, and `except` using a small example unrelated to CampusFlow. Show how to reject an invalid value and handle the error without terminating the whole program. Give me an experiment to verify the behavior."

**Useful AI guidance:**

I learned that:

* `raise` signals that an operation cannot continue because a condition is invalid.
* `try` contains code that might raise an exception.
* `except` handles a matching exception.
* A function can raise a clear exception while the CLI catches it and displays a friendly message.

Example:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("The divisor cannot be zero.")
    return a / b


try:
    print(divide(10, 0))
except ValueError as error:
    print(f"Error: {error}")
```

Expected output:

```text
Error: The divisor cannot be zero.
```

**My independent experiment/test:**

I planned to run the example twice: first with a divisor of zero, then with a valid divisor such as two. The first call should raise a `ValueError`, while the second should return `5.0`. I would verify that the error is handled by the `except` block.

**Verification source or result:**

[Record the actual output from both runs and whether the observed behavior matched the prediction.]

Reference: Python documentation — https://docs.python.org/3/tutorial/errors.html

**Decision:**

I accepted the approach after verifying the example. For CampusFlow, I will use exceptions for invalid operations and handle expected errors in `main.py`. I will avoid catching every possible exception indiscriminately because that could hide programming errors.

**Related file/commit:**

* File: `campusflow/tickets.py` or `campusflow/workflow.py`
* Test: [Add the actual invalid-input or unknown-ticket test name]
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`raise` allows a function to reject invalid data, while `try` and `except` allow the calling code to respond appropriately. In CampusFlow, a blank title or unknown ticket ID should produce a clear error instead of causing an incorrect update.

---

## Interaction #3 — Automated Testing with Python `unittest`

**Problem:**

CampusFlow must have at least eight meaningful automated tests. I needed to understand how to write a test that checks whether a function returns the expected result and how to test invalid inputs.

**My initial understanding:**

I understood that tests help find bugs, but I was unsure how `unittest` discovers test methods, how assertions work, and how to test a function that is expected to raise an exception.

**Prompt to AI:**

"Explain Python's `unittest` module with a small example unrelated to CampusFlow. Show how to test a normal result, an incorrect input, and an expected exception. Explain how to run the test and interpret the output."

**Useful AI guidance:**

I learned that `unittest.TestCase` provides methods for checking expected behavior.

* `assertEqual(actual, expected)` checks whether two values are equal.
* `assertTrue(condition)` checks whether a condition is true.
* `assertRaises(ExceptionType)` checks whether an operation raises the expected exception.

Example:

```python
import unittest


def square(number):
    if not isinstance(number, (int, float)) or isinstance(number, bool):
        raise ValueError("A number is required.")
    return number * number


class TestSquare(unittest.TestCase):

    def test_square_positive_number(self):
        self.assertEqual(square(4), 16)

    def test_square_zero(self):
        self.assertEqual(square(0), 0)

    def test_reject_invalid_input(self):
        with self.assertRaises(ValueError):
            square("four")


if __name__ == "__main__":
    unittest.main()
```

Save the example as `test_square.py` and run:

```bash
python -m unittest -v test_square
```

**My independent experiment/test:**

I planned to run the three tests and predict that all would pass. I would then temporarily change the expected result from `16` to `15` and rerun the tests to observe how `unittest` reports a failure. Afterward, I would restore the correct assertion.

**Verification source or result:**

[Record the actual test output, including the number of tests run and whether they passed. Also record the result of the temporary incorrect assertion.]

Reference: Python documentation — https://docs.python.org/3/library/unittest.html

**Decision:**

I accepted the testing approach after verifying the example. I learned that a test should contain a clear expectation and assertion, and that a failing test can reveal a mismatch between the implementation and the expected behavior.

**Related file/commit:**

* File: `tests/test_tickets.py` or `tests/test_workflow.py`
* Test: [Add the actual test name]
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`unittest` lets me verify program behavior automatically. I can test successful operations, invalid inputs, and expected exceptions without manually interacting with the CLI. In CampusFlow, this helps verify priority rules, ticket assignment, workflow restrictions, and JSON persistence before the changes are merged into `main`.

---

## Final Reflection

Through these learning interactions, I learned about JSON persistence, exception handling, and automated testing. I understand how these concepts contribute to a reliable command-line application.

My next step is to apply the concepts to CampusFlow, run the relevant tests, inspect the actual output, and document any corrections or improvements I make after verification.

**Evidence checklist:**

* [ ] Ran the JSON experiment and recorded the actual result.
* [ ] Ran the exception-handling experiment and recorded the actual result.
* [ ] Ran the `unittest` experiment, including the deliberate failure.
* [ ] Updated each entry with actual test names and project files.
* [ ] Added real commit SHAs or pull request links where available.
* [ ] Can explain each concept without reading the AI response.
* [ ] Documented at least one AI suggestion that I independently corrected, improved, or rejected after checking it.
