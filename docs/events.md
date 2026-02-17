## Event Sourcing

In Liceo audit trail is important as the system could be potentially handling very sensitive data. Because of that, all important changes over the different parts of the system need to record who did what when. The implementation is a series of events containing all the changes made by users in the system recording:

- who did the change
- what the user did
- when the user did it
- which order of the changes over the aggregate did the event took 

### Patterns

#### Mutating an aggregate

- Service
    - Service method starts a transaction
    - Service loads current database aggregate version
    - If no aggregate is found return not found
- Aggregate
    - If the aggregate exists then apply the command to the required action
    - The command should have the expected_version
    - The expected version is checked by the aggregate
    - If all invariants are met then we proceed to persist projection
- Repository
    - Use aggregate repository to store projection
    - Use event store to store events
    - Close transaction (as the end of the service invocation)

```python
@transactional
def update_aggregate(self, dto: DTO) -> Aggregate | None:
    # loading aggregate
    loaded = self.repository.load(dto.id)

    # checking existence
    if not loaded:
        return None

    # mutate aggregate respecting invatiants
    updated = loaded.change_something(Aggregate.Command(
        # add expected version
        expected_version=dto.expected_version,
        ...
    ))

    # persist changes
    self.repository.persist(updated)
    self.event_store.persist(updated)
    # return updated aggregate
    return updated
```

#### Listing aggregates

When listing aggregates there is no need to worry about aggregate versions. So we should not include the version.

#### Getting specific aggregates

When getting an specific aggregate we should get the version as is the expected version the client will use to make the subsequent mutation to succeed.

### Premises

- Events are generated from aggregates
- Aggregates contain invariants
- All mutations require `expected_version` to match the latest version from aggregate
- If `expected_version` doesn't match the system will throw a concurrent modification exception type

### TODO

- `correlation ID`: Sometimes a given change can span multiple aggregates producing several events. Without the correlation ID is difficult to correlate events between aggregates.