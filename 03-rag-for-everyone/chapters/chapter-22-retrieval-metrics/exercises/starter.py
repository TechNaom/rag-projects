"""Chapter 22 exercise: calculate retrieval metrics."""

CASE = {"gold": {"S2", "S4"}, "retrieved": ["S1", "S2", "S3", "S4", "S8"]}


def metric_report(case, k=3):
    # TODO: compute recall@k, precision@k, and reciprocal rank.
    return {}


if __name__ == "__main__":
    print(metric_report(CASE, k=3))
