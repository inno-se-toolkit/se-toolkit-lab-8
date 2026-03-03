# Testing

<h2>Table of contents</h2>

- [What is testing](#what-is-testing)
- [Assertion](#assertion)
- [Dynamic analysis](#dynamic-analysis)
- [Static analysis](#static-analysis)
- [Boundary value analysis](#boundary-value-analysis)
- [Unit test](#unit-test)
- [End-to-end test](#end-to-end-test)

## What is testing

Testing is the practice of verifying that software behaves as expected by running it with specific inputs and checking that the outputs match the expected results.

This is a form of dynamic analysis — the code is actually executed, as opposed to static analysis which inspects code without running it.

Tests catch bugs early, prevent regressions when code changes, and document the intended behavior of a program.

Examples:

- [Testing in `Python`](./python.md#testing)

## Assertion

An assertion is a statement that checks whether a given condition is true. If the condition is false, the assertion fails and raises an error, stopping the test immediately. Assertions are the primary mechanism for verifying expected behavior in tests — each test typically ends with one or more assertions that confirm the code produced the right result.

Examples:

- [The `assert` statement in `Python`](./python.md#the-assert-statement)

## Dynamic analysis

Dynamic analysis checks code behavior by executing it. Errors are only detected when the relevant code path actually runs.

Examples:

- [Testing in `Python`](./python.md#testing)

## Static analysis

Static analysis checks code for errors without running it. It can detect type errors, undefined variables, and style issues.

Examples:

- [`Pylance`](./python.md#pylance)

## Boundary value analysis

<!-- TODO -->

## Unit test

<!-- TODO -->

End-to-end (E2E) tests

## End-to-end test

<!-- TODO -->

End-to-end (E2E) tests are ...
