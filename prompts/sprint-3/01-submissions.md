Implement ONLY the Submissions module.

Read all documentation first.

Submissions are immutable.

Every learner attempt creates a new Submission.

Responsibilities

- Create submission
- Attempt numbering
- Submission history
- Status tracking
- Validation
- Ownership verification

Do NOT:

- Evaluate submissions
- Calculate progress
- Award XP
- Unlock levels

Create:

- migration
- domain models
- SQLAlchemy models
- repository
- repository interface
- service
- API
- schemas
- events
- README
- unit tests
- integration tests

Publish:

SubmissionCreated

SubmissionUpdatedStatus

Never update submission answers.

Stop after completion.