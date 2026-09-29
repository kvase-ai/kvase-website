import unittest

from cloudflare_dns import plan


class PlanTests(unittest.TestCase):
    def test_replaces_only_website_records_and_keeps_mail(self):
        existing = [
            {"id": "old", "type": "A", "name": "kvase.ai", "content": "66.241.124.231"},
            {
                "id": "ipv6",
                "type": "AAAA",
                "name": "kvase.ai",
                "content": "2a09:8280:1::9c:169e:0",
            },
            {
                "id": "www",
                "type": "A",
                "name": "www.kvase.ai",
                "content": "66.241.124.231",
            },
            {"id": "mx", "type": "MX", "name": "kvase.ai", "content": "mail.kvase.ai"},
            {
                "id": "other",
                "type": "A",
                "name": "api.kvase.ai",
                "content": "192.0.2.1",
            },
        ]
        changes = plan("zone", existing)
        self.assertEqual([change.method for change in changes[:3]], ["DELETE"] * 3)
        self.assertEqual(sum(change.method == "POST" for change in changes), 5)
        self.assertTrue(all("/mx" not in change.path for change in changes))
        self.assertTrue(all("/other" not in change.path for change in changes))

    def test_matching_records_are_idempotent_and_unproxied(self):
        existing = [
            {
                "id": str(i),
                "type": "A",
                "name": "kvase.ai",
                "content": address,
                "proxied": False,
            }
            for i, address in enumerate(
                (
                    "185.199.108.153",
                    "185.199.109.153",
                    "185.199.110.153",
                    "185.199.111.153",
                )
            )
        ]
        existing.append(
            {
                "id": "www",
                "type": "CNAME",
                "name": "www.kvase.ai",
                "content": "kvase-ai.github.io.",
                "proxied": True,
            }
        )
        changes = plan("zone", existing)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].method, "PATCH")
        self.assertEqual(changes[0].body, {"proxied": False})


if __name__ == "__main__":
    unittest.main()
