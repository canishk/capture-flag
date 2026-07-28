# Recognition Integration Review

Review the Recognition bounded context.

Verify

- Event subscriptions
- Event contracts
- Repository ownership
- CQRS compliance
- Domain boundaries
- Idempotent consumers
- Duplicate handling
- Retry behavior
- Transaction boundaries

Ensure Recognition depends only on published events.

No repository from Learning Workflow may be imported.