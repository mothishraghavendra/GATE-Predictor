#!/usr/bin/env python3
"""
Test script to verify marking details scraping
"""

# Sample response from serblabs.in API
sample_api_response = {
    "summary": {
        "total_marks": 17.33,
        "total_questions": 65,
        "correct": 17,
        "wrong": 33,
        "unanswered": 15,
        "positive_marks": 24.00,
        "negative_marks": 6.67,
        "rank": 1447,
        "total_students": 2428,
        "section_marks": {
            "General Aptitude (GA)": 1.67,
            "Data Science & AI (DA)": 15.67
        },
        "section_possible": {
            "General Aptitude (GA)": 15,
            "Data Science & AI (DA)": 85
        },
        "type_stats": {
            "MCQ": {
                "correct": 10,
                "wrong": 13,
                "marks": "+6.33"
            },
            "MSQ": {
                "correct": 2,
                "wrong": 12,
                "marks": "+3.00"
            },
            "NAT": {
                "correct": 5,
                "wrong": 8,
                "marks": "+8.00"
            }
        }
    },
    "results": []
}

print("=" * 60)
print("MARKING DETAILS SCRAPING TEST")
print("=" * 60)

# Simulate scraper extraction
summary = sample_api_response.get('summary', {})

positive_marks = None
negative_marks = None

if 'positive_marks' in summary:
    try:
        positive_marks = float(summary['positive_marks'])
        print(f"✅ Positive Marks extracted: {positive_marks}")
    except (ValueError, TypeError):
        print("❌ Failed to extract positive marks")

if 'negative_marks' in summary:
    try:
        negative_marks = float(summary['negative_marks'])
        print(f"✅ Negative Marks extracted: {negative_marks}")
    except (ValueError, TypeError):
        print("❌ Failed to extract negative marks")

# Calculate net score
if positive_marks is not None and negative_marks is not None:
    net_score = round(positive_marks - negative_marks, 2)
    print(f"✅ Net Score calculated: {net_score}")
else:
    print("❌ Cannot calculate net score")

print("\n" + "=" * 60)
print("EXPECTED DISPLAY IN MARKING DETAILS CARD:")
print("=" * 60)
print(f"Positive Marks:    +{positive_marks:.2f}")
print(f"Negative Marks:    -{negative_marks:.2f}")
print(f"Net Score:         {net_score:.2f}")
print("=" * 60)

# Verify it matches the expected output
expected_positive = 24.00
expected_negative = 6.67
expected_net = 17.33

if (positive_marks == expected_positive and 
    negative_marks == expected_negative and 
    net_score == expected_net):
    print("\n✅ ALL VALUES MATCH EXPECTED OUTPUT!")
else:
    print("\n❌ Values don't match expected output")
    
print("\nData is being scraped from serblabs.in API field: 'summary'")
print("Fields used: positive_marks, negative_marks")
