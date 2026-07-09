SOURCES = [
    {"id": "parental_leave_policy.pdf", "format": "pdf", "authority": "approved", "access": "internal", "fresh": True},
    {"id": "refund_edge_cases.docx", "format": "docx", "authority": "draft", "access": "support", "fresh": True},
    {"id": "pricing_2024.pdf", "format": "pdf", "authority": "retired", "access": "sales", "fresh": False},
    {"id": "product_catalog.json", "format": "json", "authority": "approved", "access": "public", "fresh": True},
    {"id": "customers_table", "format": "database", "authority": "approved", "access": "restricted", "fresh": True},
]


def decide(source):
    # TODO: return decision, risk, and required metadata.
    return {"id": source["id"]}


if __name__ == "__main__":
    for source in SOURCES:
        print(decide(source))
