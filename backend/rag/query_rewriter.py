class QueryRewriter:
    def __init__(self):
        self.expansions = {
            "leave": ["annual leave", "vacation", "leave entitlement", "time off"],
            "hr": ["human resources", "personnel department"],
            "policy": ["policy guidelines", "company rules", "official regulations"],
            "payroll": ["salary details", "compensation structure", "pay slip"],
            "epm": ["enterprise project management", "project tracking"],
            "mfa": ["multi factor authentication", "two step verification"]
        }

    def rewrite(self, query: str) -> str:
        words = query.lower().split()
        expanded = []
        for w in words:
            clean = w.strip("?,.!")
            expanded.append(w)
            if clean in self.expansions:
                expanded.extend(self.expansions[clean])
        return " ".join(dict.fromkeys(expanded))

query_rewriter = QueryRewriter()
