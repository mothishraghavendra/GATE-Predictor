#!/usr/bin/env python3
"""
Test to verify template renders without undefined errors
"""
from flask import Flask, render_template_string
import sys

app = Flask(__name__)

# Test with minimal data (simulating when some fields might be missing)
test_data = {
    'url': 'test-url',
    'response_data': {
        'statistics': {
            'total_questions': 65,
            'attempted': 50,
            'not_attempted': 15,
            'correct': 17,
            'wrong': 33,
            'unanswered': 15
        },
        'exam_info': {},
        'submitted_url': 'test-url',
        'processed_by': 'serblabs.in'
    },
    'predicted_marks': {
        'predicted_score': 17.33,
        'best_case_score': 75.00,
        'worst_case_score': -25.00,
        'accuracy_estimate': 34.0,
        'breakdown': {
            'total_questions': 65,
            'attempted': 50,
            'not_attempted': 15,
            '1_mark_attempted': 20,
            '2_mark_attempted': 30,
            'estimated_correct': 17,
            'estimated_wrong': 33,
            'positive_marks': 24.00,
            'negative_marks': 6.67,
            '1_mark_correct': 10,
            '1_mark_wrong': 10,
            '2_mark_correct': 7,
            '2_mark_wrong': 23
        },
        'grade': 'Average (Border line)',
        'source': 'serblabs.in',
        'processed_by': 'serblabs.in'
    },
    'form': None
}

# Test template snippet with default filters
template = """
Test Values:
- Predicted Score: {{ predicted_marks.predicted_score | default(0) }}
- Best Case: {{ predicted_marks.best_case_score | default(0) }}
- Worst Case: {{ predicted_marks.worst_case_score | default(0) }}
- Positive Marks: {{ ((response_data.positive_marks if response_data.positive_marks is not none else predicted_marks.breakdown.positive_marks) | default(0) | round(2)) }}
- Negative Marks: {{ ((response_data.negative_marks if response_data.negative_marks is not none else predicted_marks.breakdown.negative_marks) | default(0) | abs | round(2)) }}
- Net Score: {{ (predicted_marks.predicted_score | default(0) | round(2)) }}
- Accuracy: {{ predicted_marks.accuracy_estimate | default(0) }}%
- Correct: {{ (response_data.statistics.correct if response_data.statistics.correct > 0 else predicted_marks.breakdown.estimated_correct) | default(0) }}
- Wrong: {{ (response_data.statistics.wrong if response_data.statistics.wrong > 0 else predicted_marks.breakdown.estimated_wrong) | default(0) }}
"""

with app.app_context():
    try:
        result = render_template_string(template, **test_data)
        print("✅ Template rendering successful!")
        print(result)
        print("\n✅ No 'Undefined doesn't define __round__ method' errors!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        sys.exit(1)
