# Submission Checklist

Use this checklist to prepare the final submission. Update each status after completing and verifying the corresponding requirement.

## Required Deliverables

| Requirement                | Current Status                                            | Action Required                                                                                                                            |
| -------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------|
| GitHub repository link     | Not yet recorded                                          | Upload the extracted project files to GitHub and provide the actual repository URL.                                                        |
| README.md                | Prepared                                                  | Ensure the latest version is saved and its setup instructions match the submitted code.                                                    |
| AI_USAGE.md              | Prepared; candidate review pending                        | Record the AI tools and prompts used, outputs you accepted or rejected, modifications, mistakes found, and your actual verification steps. |
| Original chat transcript   | Not yet included                                          | Export the actual assignment conversation directly. Attach the original export to the submission and include it in the repository.         |
| Personal learning response | To be written by the candidate                            | Write what you learned in your own words, without AI assistance. Include it as required by the employer.                                   |
| Test cases                 | Included in shipping/tests.py                           | Review and run the tests against the final submitted code.                                                                                 |
| Test-run evidence          | Assistant-environment output included in TEST_OUTPUT.md | Run the final version locally and capture the actual terminal output, or provide a successful GitHub Actions run link for that version.    |

## AI Usage Disclosure

Before submission, check that AI_USAGE.md includes:

* The AI tools you used.
* The prompts you supplied, including follow-up requests.
* The outputs you personally reviewed and accepted.
* The outputs you rejected or modified, with reasons.
* Mistakes found during development and how they were corrected.
* Verification commands you actually ran and the results observed.

Clearly distinguish assistant-performed work from work you completed yourself. Do not claim reviews, modifications, or tests that you did not perform.

## Original Chat Transcript

* Export the genuine conversation directly.
* Include any additional assignment-related AI conversations.
* Attach the export to the submission and include it in the repository.
* Do not generate, reconstruct, summarize, or rewrite the transcript using AI.

The prompt excerpts in AI_USAGE.md are disclosure records. They do not replace the required original chat export.

## Personal Learning Response

Write the answer to “What did you learn in this assignment?” yourself, without AI assistance.

This project package does not include a generated learning response.

## Test Verification

Run these commands from the folder containing manage.py:

powershell
.venv\Scripts\python.exe manage.py test --verbosity 2
.venv\Scripts\python.exe manage.py check


For terminal-based evidence, include the following in TEST_OUTPUT.md:

* The commands executed.
* The Python and Django versions used.
* The actual terminal output.
* The test-run date and final result.

If the code changes afterward, rerun the tests and update the evidence. Do not edit failed output to make it appear successful.

A GitHub Actions run link may be submitted instead, as permitted by the assignment.


