# Back-end Testing

<h4>Time</h4>

~75 min

<h4>Purpose</h4>

Write unit and end-to-end tests, diagnose bugs from failing test output, and use an AI agent to generate additional test cases.

<h4>Context</h4>

The back-end contains intentional bugs that you will discover and fix by writing tests, then use an AI agent to generate additional coverage.

<!-- TODO diagram -->

<h4>Table of contents</h4>

- [1. Steps](#1-steps)
  - [1.1. Follow the `Git workflow`](#11-follow-the-git-workflow)
  - [1.2. Create a `Lab Task` issue](#12-create-a-lab-task-issue)
  - [1.3. Part A: Run unit tests locally](#13-part-a-run-unit-tests-locally)
    - [1.3.1. Create the environment file for unit tests](#131-create-the-environment-file-for-unit-tests)
    - [1.3.2. Run existing unit tests](#132-run-existing-unit-tests)
    - [1.3.3. Add a new unit test](#133-add-a-new-unit-test)
    - [1.3.4. Fix the bug](#134-fix-the-bug)
    - [1.3.5. Rerun unit tests](#135-rerun-unit-tests)
    - [1.3.6. Commit your changes](#136-commit-your-changes)
    - [1.3.7. Transfer the changes to your VM](#137-transfer-the-changes-to-your-vm)
    - [1.3.8. Deploy the fixed `app` service on your VM](#138-deploy-the-fixed-app-service-on-your-vm)
  - [1.4. Part B: Run end-to-end tests remotely](#14-part-b-run-end-to-end-tests-remotely)
    - [1.4.1. Create the environment file for end-to-end tests](#141-create-the-environment-file-for-end-to-end-tests)
    - [1.4.2. Run existing end-to-end tests](#142-run-existing-end-to-end-tests)
    - [1.4.3. Add three end-to-end tests](#143-add-three-end-to-end-tests)
    - [1.4.4. Diagnose the bug](#144-diagnose-the-bug)
    - [1.4.5. Fix the bug](#145-fix-the-bug)
    - [1.4.6. Redeploy and rerun](#146-redeploy-and-rerun)
    - [1.4.7. Commit the fix](#147-commit-the-fix)
  - [1.5. Part C: Generate tests with an AI agent](#15-part-c-generate-tests-with-an-ai-agent)
    - [1.5.1. Generate tests](#151-generate-tests)
    - [1.5.2. Review and curate the tests](#152-review-and-curate-the-tests)
    - [1.5.3. Run the full test suite](#153-run-the-full-test-suite)
    - [1.5.4. Commit the curated tests](#154-commit-the-curated-tests)
  - [1.6. Finish the task](#16-finish-the-task)
- [2. Acceptance criteria](#2-acceptance-criteria)

## 1. Steps

### 1.1. Follow the `Git workflow`

Follow the [`Git workflow`](../../../wiki/git-workflow.md) to complete this task.

> [!IMPORTANT]
> You work on the [`<task-branch>`](../../../wiki/git-workflow.md#task-branch).

### 1.2. Create a `Lab Task` issue

Title: `[Task] Back-end Testing`

### 1.3. Part A: Run unit tests locally

<!-- no toc -->
- [1.3.1. Create the environment file for unit tests](#131-create-the-environment-file-for-unit-tests)
- [1.3.2. Run existing unit tests](#132-run-existing-unit-tests)
- [1.3.3. Add a new unit test](#133-add-a-new-unit-test)
- [1.3.4. Fix the bug](#134-fix-the-bug)
- [1.3.5. Rerun unit tests](#135-rerun-unit-tests)
- [1.3.6. Commit your changes](#136-commit-your-changes)
- [1.3.7. Transfer the changes to your VM](#137-transfer-the-changes-to-your-vm)
- [1.3.8. Deploy the fixed `app` service on your VM](#138-deploy-the-fixed-app-service-on-your-vm)

> [!NOTE]
> Unit tests do not require a running server. They test individual functions in isolation.

#### 1.3.1. Create the environment file for unit tests

1. To copy the content of [`.env.tests.unit.example`](../../../.env.tests.unit.example) to [`.env.tests.unit.secret`](../../../wiki/dotenv-tests-unit-secret.md#what-is-envtestsunitsecret),

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cp .env.tests.unit.example .env.tests.unit.secret
   ```

#### 1.3.2. Run existing unit tests

1. To run the existing unit tests,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test-unit
   ```

2. All existing tests should pass.

   The output should be similar to this:

   ```terminal
   ===================== 3 passed in X.XXs =====================
   ```

#### 1.3.3. Add a new unit test

> [!TIP]
> Feel free to use AI to generate the tests. Make sure to provide them with necessary context.

1. [Open the file](../../../wiki/vs-code.md#open-the-file):
   [`backend/tests/unit/test_interactions.py`](../../../backend/tests/unit/test_interactions.py).

2. Add a new unit test that targets the following [boundary-value case](../../../wiki/testing.md#boundary-value-analysis):

   An interaction whose `item_id` is exactly equal to `max_item_id` — for example, `item_id=2` and `max_item_id=2`. This interaction should appear in the results because the filter condition is "less than or equal to."

   Name the test `test_filter_includes_interaction_at_boundary`.

3. <details><summary>Click to open a hint</summary>

   The code for the new case should be almost the same as for the existing tests.

   </details>

4. <details><summary>Click to open the solution</summary>

   ```python
   def test_filter_includes_interaction_at_boundary() -> None:
       interactions = [_make_log(1, 1, 2)]
       result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
       assert len(result) == 1
       assert result[0].id == 1
   ```

   </details>

5. To run the tests,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test-unit
   ```

6. Observe that the new test fails.

   The output should be similar to this:

   ```terminal
   FAILED backend/tests/unit/test_interactions.py::test_filter_includes_interaction_at_boundary - assert 0 == 1
   ```

   This line means the following:
   - The test failed (`FAILED`).
   - The test is in the file `backend/tests/unit/test_interactions.py`.
   - The name of the failing test is `test_filter_includes_interaction_at_boundary`.
   - The failed [assertion](../../../wiki/testing.md#assertion) is `assert 0 == 1` — the filter returned 0 interactions, but 1 was expected.

#### 1.3.4. Fix the bug

1. [Open the file](../../../wiki/vs-code.md#open-the-file):
   [`backend/app/routers/interactions.py`](../../../backend/app/routers/interactions.py).

2. Fix the bug in the `filter_by_max_item_id` function.

3. <details><summary>Click to open a hint</summary>

   The filter is applied in-memory after all interactions are fetched from the database.
   Look at the comparison operator in the condition that decides which interactions to include — it excludes the boundary value.

   </details>

4. <details><summary>Click to open the solution</summary>

   Find this line in `filter_by_max_item_id`:

   ```python
   return [i for i in interactions if i.item_id < max_item_id]
   ```

   Change it to:

   ```python
   return [i for i in interactions if i.item_id <= max_item_id]
   ```

   </details>

#### 1.3.5. Rerun unit tests

1. To rerun the unit tests,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test-unit
   ```

2. All tests should pass.

   The output should be similar to this:

   ```terminal
   ===================== 4 passed in X.XXs =====================
   ```

#### 1.3.6. Commit your changes

1. [Commit](../../../wiki/git-workflow.md#commit) your changes.

   Use this commit message:

   ```text
   fix: use <= instead of < in max_item_id filter
   ```

#### 1.3.7. Transfer the changes to your VM

> [!NOTE]
> See [`origin`](../../../wiki/github.md#origin).

1. [Push commits to `<task-branch>` on `origin`](../../../wiki/git-workflow.md#push-commits).

   Replace [`<task-branch>`](../../../wiki/git-workflow.md#task-branch).

2. [Open a new `VS Code Terminal`](../../../wiki/vs-code.md#open-a-new-vs-code-terminal).

3. [Connect to the VM](../../../wiki/ssh.md#connect-to-the-vm).

4. To navigate to the repository directory on the VM,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cd se-toolkit-lab-4
   ```

5. [Pull the latest changes from `<task-branch>` on `origin`](../../../wiki/git-vscode.md#pull-changes-from-branch-on-remote-using-the-vs-code-terminal).

   Replace [`<task-branch>`](../../../wiki/git-workflow.md#task-branch).

6. [Switch to `<task-branch>`](../../../wiki/git-vscode.md#switch-to-an-existing-branch-using-vs-code-terminal).

   Replace [`<task-branch>`](../../../wiki/git-workflow.md#task-branch).

#### 1.3.8. Deploy the fixed `app` service on your VM

1. To rebuild and start the [`app` service](../../../wiki/docker-compose-yml.md#app-service) in [background](../../../wiki/operating-system.md#background-process),

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret up app --build --force-recreate -d
   ```

2. To verify the service is running,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret ps app --format "table {{.Service}}\t{{.Status}}"
   ```

   The output should be similar to this:

   ```terminal
   SERVICE   STATUS
   app       Up 1 minute
   ```

### 1.4. Part B: Run end-to-end tests remotely

<!-- no toc -->
- [1.4.1. Create the environment file for end-to-end tests](#141-create-the-environment-file-for-end-to-end-tests)
- [1.4.2. Run existing end-to-end tests](#142-run-existing-end-to-end-tests)
- [1.4.3. Add three end-to-end tests](#143-add-three-end-to-end-tests)
- [1.4.4. Diagnose the bug](#144-diagnose-the-bug)
- [1.4.5. Fix the bug](#145-fix-the-bug)
- [1.4.6. Redeploy and rerun](#146-redeploy-and-rerun)
- [1.4.7. Commit the fix](#147-commit-the-fix)

> [!NOTE]
> [End-to-end (E2E) tests](../../../wiki/testing.md#end-to-end-test) run on your local machine and send real [`HTTP` requests](../../../wiki/http.md#http-request) to the deployed version on the VM.
>
> In [Part A](#13-part-a-run-unit-tests-locally), a unit test caught a logic error inside a single function. Some bugs only appear when all components interact during a real request — for example, a mismatch between layers of the stack. End-to-end tests catch these integration-level failures.

#### 1.4.1. Create the environment file for end-to-end tests

1. To copy the content of [`.env.tests.e2e.example`](../../../.env.tests.e2e.example) to [`.env.tests.e2e.secret`](../../../wiki/dotenv-tests-e2e-secret.md#what-is-envtestse2esecret),

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cp .env.tests.e2e.example .env.tests.e2e.secret
   ```

2. [Open](../../../wiki/vs-code.md#open-the-file) `.env.tests.e2e.secret`.

3. Set [`API_BASE_URL`](../../../wiki/dotenv-tests-e2e-secret.md#api_base_url) to `http://<your-vm-ip-address>:<caddy-port>`. Replace:

   - [`<your-vm-ip-address>`](../../../wiki/vm.md#your-vm-ip-address)
   - [`<caddy-port>`](../../../wiki/caddy.md#caddy-port)

4. Set [`API_KEY`](../../../wiki/dotenv-tests-e2e-secret.md#api_key) to the same value as [`API_KEY`](../../../wiki/dotenv-docker-secret.md#api_key) in [`.env.docker.secret`](../../../wiki/dotenv-docker-secret.md#what-is-envdockersecret) on the VM.

#### 1.4.2. Run existing end-to-end tests

1. To run the end-to-end tests,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test-e2e
   ```

2. All existing end-to-end tests should pass.

   The output should be similar to this:

   ```terminal
   ===================== 2 passed in X.XXs =====================
   ```

#### 1.4.3. Add three end-to-end tests

1. [Open the file](../../../wiki/vs-code.md#open-the-file):
   [`backend/tests/e2e/test_interactions.py`](../../../backend/tests/e2e/test_interactions.py).

2. Add three end-to-end tests that cover the following cases:

   - Test 1: `GET /interactions/` returns [`HTTP` status code](../../../wiki/http.md#http-response-status-code) `200`.
   - Test 2: `GET /interactions/` response items contain the expected fields (`id`, `item_id`, `created_at`).
   - Test 3: `GET /interactions/?max_item_id=1` returns a non-empty list where every item has `item_id` less than or equal to `1`. This confirms the [Part A fix](#134-fix-the-bug) at the API level.

   <details><summary>Click to open the solution</summary>

   ```python
   import httpx


   def test_get_interactions_returns_200(client: httpx.Client) -> None:
       response = client.get("/interactions/")
       assert response.status_code == 200


   def test_get_interactions_response_items_have_expected_fields(client: httpx.Client) -> None:
       response = client.get("/interactions/")
       data = response.json()
       assert len(data) > 0
       assert "id" in data[0]
       assert "item_id" in data[0]
       assert "created_at" in data[0]


   def test_get_interactions_filter_includes_boundary(client: httpx.Client) -> None:
       response = client.get("/interactions/?max_item_id=1")
       assert response.status_code == 200
       data = response.json()
       assert len(data) > 0
       assert all(item["item_id"] <= 1 for item in data)
   ```

   </details>

3. To run the end-to-end tests,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test-e2e
   ```

4. Observe that all three new tests fail.

   The output should be similar to this:

   ```terminal
   FAILED backend/tests/e2e/test_interactions.py::test_get_interactions_returns_200 - assert 500 == 200
   FAILED backend/tests/e2e/test_interactions.py::test_get_interactions_response_items_have_expected_fields - json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
   FAILED backend/tests/e2e/test_interactions.py::test_get_interactions_filter_includes_boundary - assert 500 == 200
   ```

   The `500` status code means the server encountered an internal error while building the response.

#### 1.4.4. Diagnose the bug

1. Switch to the `VS Code Terminal` connected to your VM (the one you used in [section 1.3.8](#138-deploy-the-fixed-app-service-on-your-vm)).

2. To read the recent `app` service logs,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose --env-file .env.docker.secret logs app --tail 30
   ```

3. Look for a traceback near the bottom of the output.

   The output should include lines similar to this:

   ```terminal
   app-1  | fastapi.exceptions.ResponseValidationError: 12 validation errors:
   app-1  |   {'type': 'missing', 'loc': ('response', 0, 'timestamp'), 'msg': 'Field required', 'input': InteractionLog(kind='view', id=1, learner_id=1, item_id=1, created_at=datetime.datetime(2025, 9, 2, 10, 0))}
   ...
   app-1  |   {'type': 'missing', 'loc': ('response', 11, 'timestamp'), 'msg': 'Field required', 'input': InteractionLog(kind='view', id=12, learner_id=5, item_id=6, created_at=datetime.datetime(2025, 10, 16, 9, 30))}
   app-1  | 
   app-1  |   File "/app/backend/app/routers/interactions.py", line 26, in get_interactions
   ```

   This tells you that something bad happened in [`backend/app/routers/interactions.py`](../../../backend/app/routers/interactions.py) at the line 26.

   Namely, the `timestamp` field is missing but `InteractionLog` has only the `created_at` field.

4. Look at the code on that line:

   ```python
   @router.get("/", response_model=list[InteractionModel])
   ```

5. Look at the code inside `get_interactions`.

   First, `interactions` are read from the database.

   ```python
   interactions = await read_interactions(session)
   ```

   Then, they're filtered:

   ```python
   return filter_by_max_item_id(interactions, max_item_id)
   ```

   The type of the returned value is `list[InteractionLog]`.

   Look at the definition of `InteractionLog` in [`backend/app/models/interaction.py`](../../../backend/app/models/interaction.py).

   It has the field `created_at`.

   Now, look at the definition of `InteractionModel` below in the same file.

   It has all the same fields as `InteractionLog` except it has `timestamp` instead of `created_at`.

   So, `FastAPI` tries but can't convert `InteractionLog` to `InteractionModel` because of this field name mismatch.

#### 1.4.5. Fix the bug

1. Based on the traceback, fix the bug in `InteractionModel`.

2. <details><summary>Click to open the solution</summary>

   Find this line in `InteractionModel`:

   ```python
   timestamp: datetime
   ```

   Change it to:

   ```python
   created_at: datetime
   ```

   </details>

#### 1.4.6. Redeploy and rerun

1. [Transfer the changes to your VM](#137-transfer-the-changes-to-your-vm)

2. [Deploy the fixed `app` service on your VM](#138-deploy-the-fixed-app-service-on-your-vm).

3. To run the end-to-end tests,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test-e2e
   ```

4. All end-to-end tests should pass.

   The output should be similar to this:

   ```terminal
   ===================== 5 passed in X.XXs =====================
   ```

#### 1.4.7. Commit the fix

1. [Commit](../../../wiki/git-workflow.md#commit) your changes.

   Use this commit message:

   ```text
   fix: rename timestamp to created_at in InteractionModel
   ```

> [!IMPORTANT]
> Each fix must be a **separate commit**. Do not combine the Part A and Part B fixes into one commit.

### 1.5. Part C: Generate tests with an AI agent

<!-- no toc -->
- [1.5.1. Generate tests](#151-generate-tests)
- [1.5.2. Review and curate the tests](#152-review-and-curate-the-tests)
- [1.5.3. Run the full test suite](#153-run-the-full-test-suite)
- [1.5.4. Commit the curated tests](#154-commit-the-curated-tests)

#### 1.5.1. Generate tests

1. Open the [coding agent](../../../wiki/coding-agents.md#what-is-a-coding-agent).

2. Give it this prompt:

   > "Read the back-end source code under `backend/` and the existing unit tests in `backend/tests/unit/test_interactions.py`. Generate five new unit tests that cover edge cases and boundary values not already tested. Write them to a new file `backend/tests/unit/test_interactions_ai.py`."

3. Wait for the agent to generate the tests.

#### 1.5.2. Review and curate the tests

1. [Open the file](../../../wiki/vs-code.md#open-the-file):
   [`backend/tests/unit/test_interactions_ai.py`](../../../backend/tests/unit/test_interactions_ai.py).

2. Review each generated test against the following criteria:

   - **Keep** — the test is correct, targets a real case, and adds coverage not already present.
   - **Fix** — the test has a minor error (wrong assertion, wrong expected value) but the idea is sound — correct it.
   - **Discard** — the test duplicates an existing test, is logically wrong, or tests behaviour outside the scope of the module.

3. Keep at least two tests and discard at least one.

4. For each generated test, add a one-line comment that documents your decision and reason:
   - For a kept or fixed test: `# KEPT: <reason>` or `# FIXED: <reason>`
   - For a discarded test: paste it commented out with `# DISCARDED: <reason>` above it

   Example:

   ```python
   # KEPT: covers the empty-list edge case, not tested elsewhere
   def test_filter_returns_empty_list_when_no_interactions() -> None:
       ...

   # DISCARDED: duplicates test_filter_includes_interaction_at_boundary
   # def test_filter_boundary_duplicate() -> None:
   #     ...
   ```

#### 1.5.3. Run the full test suite

1. To run the full test suite,

   [run in the `VS Code Terminal`](../../../wiki/vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe test
   ```

2. All tests (including the curated AI-generated ones) should pass.

#### 1.5.4. Commit the curated tests

1. [Commit](../../../wiki/git-workflow.md#commit) your changes.

   Use the following commit message:

   ```text
   test: add curated AI-generated unit tests
   ```

### 1.6. Finish the task

1. [Create a PR](../../../wiki/git-workflow.md#create-a-pr-to-the-main-branch-in-your-fork) with your changes.
2. [Get a PR review](../../../wiki/git-workflow.md#get-a-pr-review) and complete the subsequent steps in the `Git workflow`.

---

## 2. Acceptance criteria

- [ ] Issue has the correct title.
- [ ] All unit tests pass.
- [ ] All end-to-end tests pass.
- [ ] AI-generated tests include at least two kept tests and at least one discarded test.
- [ ] Each kept, fixed, or discarded test has a one-line comment explaining the decision.
- [ ] The Part A fix and Part B fix are separate commits.
- [ ] PR is approved.
- [ ] PR is merged.
