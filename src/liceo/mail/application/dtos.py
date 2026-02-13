from dataclasses import dataclass


@dataclass
class QueueMailDTO:
    recipient: str
    subject: str
    body: str
    created_by: str
