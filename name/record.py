from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Record:
    type: str
    host: str
    domain: str
    ttl: int
    answer: str

    @property
    def fqdn(self) -> str:
        return f"{self.host}.{self.domain}." if self.host != "" else f"{self.domain}."

    @property
    def payload(self) -> str:
        return json.dumps(dict(host=self.host, type=self.type, answer=self.answer, ttl=self.ttl))
