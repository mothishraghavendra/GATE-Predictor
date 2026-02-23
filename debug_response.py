#!/usr/bin/env python3
"""
Debug script to check what data is being extracted
"""
import sys

# Mock response data to test the flow
mock_response_data = {
    'predicted_marks': 17.33,
    'questions': [],
    'candidate_info': {},
    'exam_info': {
        'section_marks': {
            'General Aptitude (GA)': 1.67,
            'Data Science & AI (DA)': 15.67
        },
        'section_possible': {
            'General Aptitude (GA)': 15,
            'Data Science & AI (DA)': 85
        },
        'type_stats': {
            'MCQ': {'correct': 10, 'wrong': 13, 'marks': '+6.33'},
            'MSQ': {'correct': 2, 'wrong': 12, 'marks': '+3.00'},
            'NAT': {'correct': 5, 'wrong': 8, 'marks': '+8.00'}
        }
    },
    'statistics': {
        'total_questions': 65,
        'attempted': 50,
        'not_attempted': 15,
        'correct': 17,
        'wrong': 33,
        'unanswered': 15
    },
    'predicted_rank': 1447,
    'total_students': 2428,
    'positive_marks': 24.00,
    'negative_marks': 6.67,
    'raw_result': '...'
}

print("=" * 70)
print("CHECKING RESPONSE DATA STRUCTURE")
print("=" * 70)

print("\n📊 Response Data Keys:")
for key in mock_response_data.keys():
    print(f"  - {key}")

print("\n💰 Marking Details:")
print(f"  positive_marks: {mock_response_data.get('positive_marks')}")
print(f"  negative_marks: {mock_response_data.get('negative_marks')}")
print(f"  predicted_marks: {mock_response_data.get('predicted_marks')}")

print("\n📈 Statistics:")
for key, value in mock_response_data.get('statistics', {}).items():
    print(f"  {key}: {value}")

print("\n🎯 Exam Info:")
if 'section_marks' in mock_response_data.get('exam_info', {}):
    print("  ✅ Section marks available")
    for section, marks in mock_response_data['exam_info']['section_marks'].items():
        print(f"    {section}: {marks}")

if 'type_stats' in mock_response_data.get('exam_info', {}):
    print("  ✅ Type stats available")
    for qtype, stats in mock_response_data['exam_info']['type_stats'].items():
        print(f"    {qtype}: {stats}")

print("\n" + "=" * 70)
print("TESTING PREDICTOR WITH THIS DATA")
print("=" * 70)

from predictor import MarkPredictor

predictor = MarkPredictor()
predicted_marks = predictor.predict(mock_response_data)

print("\n📝 Predicted Marks Output:")
print(f"  predicted_score: {predicted_marks.get('predicted_score')}")
print(f"  best_case_score: {predicted_marks.get('best_case_score')}")
print(f"  worst_case_score: {predicted_marks.get('worst_case_score')}")
print(f"  accuracy_estimate: {predicted_marks.get('accuracy_estimate')}%")

print("\n💰 Breakdown:")
breakdown = predicted_marks.get('breakdown', {})
print(f"  total_questions: {breakdown.get('total_questions')}")
print(f"  attempted: {breakdown.get('attempted')}")
print(f"  not_attempted: {breakdown.get('not_attempted')}")
print(f"  estimated_correct: {breakdown.get('estimated_correct')}")
print(f"  estimated_wrong: {breakdown.get('estimated_wrong')}")
print(f"  positive_marks: {breakdown.get('positive_marks')}")
print(f"  negative_marks: {breakdown.get('negative_marks')}")

print("\n" + "=" * 70)
print("CHECKING TEMPLATE VARIABLES")
print("=" * 70)

print("\nWhat template will see:")
print(f"  response_data.positive_marks: {mock_response_data.get('positive_marks')}")
print(f"  response_data.negative_marks: {mock_response_data.get('negative_marks')}")
print(f"  predicted_marks.breakdown.positive_marks: {breakdown.get('positive_marks')}")
print(f"  predicted_marks.breakdown.negative_marks: {breakdown.get('negative_marks')}")
print(f"  predicted_marks.predicted_score: {predicted_marks.get('predicted_score')}")

if mock_response_data.get('positive_marks') is not None:
    print("\n✅ positive_marks is available in response_data")
else:
    print("\n❌ positive_marks is NOT available in response_data")
    
if mock_response_data.get('negative_marks') is not None:
    print("✅ negative_marks is available in response_data")
else:
    print("❌ negative_marks is NOT available in response_data")

print("\n" + "=" * 70)
