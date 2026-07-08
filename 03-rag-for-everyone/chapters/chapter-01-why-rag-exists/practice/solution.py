eval_case = {
    "question": "Can I report fraud directly to the SEC without telling my manager?",
    "expected_source": "10_whistleblower_policy.md",
    "expected_behavior": "Answer from the whistleblower policy and cite the source.",
    "failure_condition": "The answer guesses, omits the source, or retrieves an unrelated policy.",
}

print(eval_case)

