"""Solution: classify quality failures."""
FAILURE = {"unsupported": True, "off_topic": False, "bad_citation": True}
def classify(failure):
    labels = []
    if failure["unsupported"]:
        labels.append("faithfulness_failure")
    if failure["off_topic"]:
        labels.append("relevance_failure")
    if failure["bad_citation"]:
        labels.append("citation_correctness_failure")
    return labels
if __name__ == "__main__":
    print(classify(FAILURE))
