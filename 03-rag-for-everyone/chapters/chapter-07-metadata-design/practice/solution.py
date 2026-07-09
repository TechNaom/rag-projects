SCENARIOS = [
    {"name": "EU security policy", "authority": "approved", "access_level": "restricted", "region": "EU", "has_source_position": True},
    {"name": "Draft HR policy", "authority": "draft", "access_level": "internal", "region": "GLOBAL", "has_source_position": True},
    {"name": "Versioned refund policy", "authority": "approved", "access_level": "internal", "region": "US", "effective_from": "2026-01-01", "expires_at": ""},
    {"name": "Restricted pricing table", "authority": "approved", "access_level": "restricted", "region": "GLOBAL", "has_row_id": True},
    {"name": "Developer docs page", "authority": "approved", "access_level": "public", "region": "GLOBAL", "has_heading_path": True},
]


def recommend_metadata_action(scenario):
    if scenario["authority"] in {"draft", "retired"}:
        return "review: source is not authoritative enough for production answers"
    if scenario["access_level"] == "restricted":
        return "publish_with_permission_filter: enforce allowed roles before retrieval"
    if scenario.get("effective_from") and not scenario.get("expires_at"):
        return "publish_with_freshness_monitor: current policy needs review schedule"
    if scenario.get("has_row_id"):
        return "publish: preserve row id, tier, region, and source URI for citations"
    if scenario.get("has_heading_path"):
        return "publish: preserve canonical URL and heading path"
    return "publish: metadata is sufficient for basic retrieval"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], recommend_metadata_action(scenario))
