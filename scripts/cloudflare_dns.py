#!/usr/bin/env python3
"""Prepare the kvase.ai GitHub Pages records in Cloudflare DNS.

Requires CLOUDFLARE_API_TOKEN with Zone Read and DNS Edit. Creating the zone
also requires CLOUDFLARE_ACCOUNT_ID. No token is stored in this repository.

Run without --apply to inspect the plan. This script changes only the apex
website records and www; it leaves mail and other names untouched.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

API = "https://api.cloudflare.com/client/v4"
ZONE = "kvase.ai"
TARGETS = (
    ("A", ZONE, "185.199.108.153"),
    ("A", ZONE, "185.199.109.153"),
    ("A", ZONE, "185.199.110.153"),
    ("A", ZONE, "185.199.111.153"),
    ("CNAME", f"www.{ZONE}", "kvase-ai.github.io"),
)
WEB_TYPES = {"A", "AAAA", "CNAME"}


@dataclass(frozen=True)
class Change:
    method: str
    path: str
    label: str
    body: dict | None = None


def request(method: str, path: str, body: dict | None = None) -> dict:
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        raise RuntimeError("Set CLOUDFLARE_API_TOKEN outside this repository")
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        payload = json.load(error)
        messages = "; ".join(
            item.get("message", "") for item in payload.get("errors", [])
        )
        raise RuntimeError(f"Cloudflare HTTP {error.code}: {messages}") from None
    if not payload.get("success"):
        messages = "; ".join(
            item.get("message", "") for item in payload.get("errors", [])
        )
        raise RuntimeError(f"Cloudflare API: {messages}")
    return payload


def zone(apply: bool) -> dict:
    result = request("GET", "/zones?" + urllib.parse.urlencode({"name": ZONE}))[
        "result"
    ]
    if result:
        return result[0]
    if not apply:
        return {"id": "<new-zone>", "status": "not created", "name_servers": []}
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if not account_id:
        raise RuntimeError("Set CLOUDFLARE_ACCOUNT_ID to create the zone")
    return request(
        "POST", "/zones", {"name": ZONE, "type": "full", "account": {"id": account_id}}
    )["result"]


def records(zone_id: str) -> list[dict]:
    found = []
    page = 1
    while True:
        payload = request(
            "GET", f"/zones/{zone_id}/dns_records?per_page=100&page={page}"
        )
        found.extend(payload["result"])
        if page >= payload.get("result_info", {}).get("total_pages", 1):
            return found
        page += 1


def normal(value: str) -> str:
    return value.rstrip(".").lower()


def plan(zone_id: str, existing: list[dict]) -> list[Change]:
    path = f"/zones/{zone_id}/dns_records"
    changes = []
    desired = {(kind, normal(name), normal(content)) for kind, name, content in TARGETS}
    current = set()
    for record in existing:
        kind = record["type"]
        name = normal(record["name"])
        if name not in (ZONE, f"www.{ZONE}") or kind not in WEB_TYPES:
            continue
        key = (kind, name, normal(record["content"]))
        if key not in desired:
            changes.append(
                Change(
                    "DELETE",
                    f"{path}/{record['id']}",
                    f"remove {kind} {name} → {record['content']}",
                )
            )
        else:
            current.add(key)
            if record.get("proxied"):
                changes.append(
                    Change(
                        "PATCH",
                        f"{path}/{record['id']}",
                        f"set DNS-only {kind} {name} → {record['content']}",
                        {"proxied": False},
                    )
                )
    for kind, name, content in TARGETS:
        if (kind, normal(name), normal(content)) not in current:
            changes.append(
                Change(
                    "POST",
                    path,
                    f"add DNS-only {kind} {name} → {content}",
                    {
                        "type": kind,
                        "name": name,
                        "content": content,
                        "proxied": False,
                        "ttl": 1,
                    },
                )
            )
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply", action="store_true", help="Create/update Cloudflare zone and records"
    )
    args = parser.parse_args()
    try:
        selected_zone = zone(args.apply)
        existing = (
            []
            if selected_zone["status"] == "not created"
            else records(selected_zone["id"])
        )
        changes = plan(selected_zone["id"], existing)
        print(f"{ZONE}: Cloudflare zone is {selected_zone['status']}")
        if selected_zone["status"] == "not created":
            print("--apply would create the zone before adding website records.")
        for item in changes:
            print(item.label)
            if args.apply:
                request(item.method, item.path, item.body)
        if not changes:
            print("Website records already match.")
        if not args.apply and changes:
            print("Dry run only. Re-run with --apply to make these changes.")
        print(
            "Existing MX records:",
            [r["content"] for r in existing if r["type"] == "MX"],
        )
        print("Review all mail and subdomain records before changing nameservers.")
        print(
            "Cloudflare nameservers:", ", ".join(selected_zone.get("name_servers", []))
        )
    except RuntimeError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
