from liceo.infra.application.output import LedgerPort
from liceo.infra.domain.events import Event


class ConsoleLedger(LedgerPort):
    def persist(self, event: Event) -> None:
        print(event)
