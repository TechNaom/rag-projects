REQUESTS = [
    {"id": "support", "query": "How do I regenerate credentials?", "risk": "low"},
    {"id": "ops", "query": "AZ-4032-B after key rotation", "risk": "medium"},
    {"id": "legal", "query": "Policy 7.3 termination clause", "risk": "high"},
]


def build_route_plan(request):
    # TODO: return route, reason, controls, and metric.
    raise NotImplementedError


if __name__ == "__main__":
    for request in REQUESTS:
        print(build_route_plan(request))
