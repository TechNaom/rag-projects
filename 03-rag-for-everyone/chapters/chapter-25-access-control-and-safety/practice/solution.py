"""Solution: classify safety denial."""
CASE = {"tenant_match": True, "role_match": False, "contains_instruction": True}
def classify(case):
    labels = []
    if not case["tenant_match"]:
        labels.append("tenant_denied")
    if not case["role_match"]:
        labels.append("role_denied")
    if case["contains_instruction"]:
        labels.append("prompt_injection_risk")
    return labels
if __name__ == "__main__":
    print(classify(CASE))
