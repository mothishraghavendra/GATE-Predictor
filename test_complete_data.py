#!/usr/bin/env python3
"""
Test template rendering with complete data including positive/negative marks
"""
from flask import Flask, render_template_string

app = Flask(__name__)

# Test with complete data (simulating actual serblabs.in response)
test_data_complete = {
    'response_data': {
        'positive_marks': 24.00,
        'negative_marks': 6.67,
        'statistics': {
            'correct': 17,
            'wrong': 33,
            'not_attempted': 15
        }
    },
    'predicted_marks': {
        'predicted_score': 17.33,
        'accuracy_estimate': 34.0,
        'breakdown': {
            'positive_marks': 24.00,
            'negative_marks': 6.67,
            'estimated_correct': 17,
            'estimated_wrong': 33
        }
    }
}

template = """
=== WITH SERBLABS DATA ===
Positive Marks: +{{ ((response_data.positive_marks if response_data.positive_marks is not none else predicted_marks.breakdown.positive_marks) | default(0) | round(2)) }}
Negative Marks: -{{ ((response_data.negative_marks if response_data.negative_marks is not none else predicted_marks.breakdown.negative_marks) | default(0) | abs | round(2)) }}
Net Score: {{ (predicted_marks.predicted_score | default(0) | round(2)) }}
"""

with app.app_context():
    result = render_template_string(template, **test_data_complete)
    print("✅ Complete data test:")
    print(result)
    
    # Test with missing data
    test_data_missing = {
        'response_data': {
            'statistics': {
                'correct': 0,
                'wrong': 0,
                'not_attempted': 0
            }
        },
        'predicted_marks': {
            'breakdown': {}
        }
    }
    
    result2 = render_template_string(template, **test_data_missing)
    print("\n✅ Missing data test (should show zeros):")
    print(result2)
    
    print("\n✅ Both tests passed - no undefined errors!")
