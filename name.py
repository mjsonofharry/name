from dataclasses import dataclass
import json
from typing import List, Optional, Tuple
import requests


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


@dataclass(frozen=True)
class NameClient:
    username: str
    token: str

    @property
    def base_url(self):
        return "https://api.name.com"

    @property
    def auth(self) -> Tuple[str, str]:
        return (self.username, self.token)

    def get_records_if_exists(self, domain: str) -> List[dict]:
        response = requests.get(
            url=f"{self.base_url}/v4/domains/{domain}/records",
            auth=self.auth,
        )
        if response.status_code != 200:
            raise RuntimeError(f"<{response.status_code}> {response.text}")
        data = response.json()
        return data.get("records", [])

    def get_record_if_exists(self, record: Record) -> Optional[dict]:
        records = self.get_records_if_exists(domain=record.domain)
        matches = [
            x
            for x in records
            if x["type"] == record.type
            and x["domainName"] == record.domain
            and x["fqdn"] == record.fqdn
        ]
        if len(matches) > 1:
            raise RuntimeError(
                f"Expected to find up to 1 matching records (found {len(matches)})"
            )
        return next(iter(matches), None)

    def update_record(self, record: Record) -> None:
        preexisting = self.get_record_if_exists(record=record)
        if preexisting:
            print(f"Updating DNS record: {record}")
            record_id = preexisting["id"]
            response = requests.put(
                url=f"{self.base_url}/v4/domains/{record.domain}/records/{record_id}",
                auth=self.auth,
                data=record.payload,
            )
        else:
            print(f"Creating DNS record: {record}")
            response = requests.post(
                url=f"{self.base_url}/v4/domains/{record.domain}/records",
                auth=self.auth,
                data=record.payload,
            )
        if response.status_code != 200:
            raise RuntimeError(f"<{response.status_code}> {response.text}")
        print("Finished updating record!")
