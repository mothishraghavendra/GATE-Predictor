#!/usr/bin/env python3
"""
Test script to validate the name filtering logic
"""

import re

def is_valid_name(text):
    """Validate if text looks like a candidate name"""
    if not text or len(text) < 3:
        return False
    
    # Exclude common UI elements and invalid patterns
    excluded_words = [
        'print', 'download', 'back', 'home', 'logout', 'login', 'submit',
        'close', 'cancel', 'save', 'edit', 'delete', 'search', 'filter',
        'candidate name', 'name:', 'name', 'label', 'button', 'link',
        'click here', 'view', 'show', 'hide', 'menu', 'nav', 'header',
        'footer', 'copyright', 'privacy', 'terms', 'contact', 'about'
    ]
    
    text_lower = text.lower().strip()
    
    # Check if text matches excluded words
    if text_lower in excluded_words:
        return False
    
    # Check if any excluded word is in the text
    if any(word in text_lower for word in excluded_words):
        return False
    
    # Must have at least some alphabetic characters
    if not re.search(r'[a-zA-Z]{3,}', text):
        return False
    
    # Should not be too long (names are usually < 50 chars)
    if len(text) > 100:
        return False
    
    # Should not be all uppercase (unless it's a proper name format)
    # But should have at least some letters
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count < 3:
        return False
    
    # Should not contain too many special characters
    special_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
    if special_count > len(text) / 3:
        return False
    
    return True


def test_validation():
    """Test various inputs to validate the filtering logic"""
    print("=" * 70)
    print("Testing Name Validation Logic")
    print("=" * 70)
    
    test_cases = [
        # (input, expected_result, description)
        ("print", False, "Should reject 'print' UI element"),
        ("Print", False, "Should reject 'Print' (case insensitive)"),
        ("download", False, "Should reject 'download' button"),
        ("Click here to print", False, "Should reject text containing 'print'"),
        ("John Doe", True, "Should accept valid name"),
        ("RAJESH KUMAR", True, "Should accept uppercase name"),
        ("Amit Kumar Singh", True, "Should accept full name"),
        ("Dr. Sarah Johnson", True, "Should accept name with title"),
        ("Mohammed Ali", True, "Should accept name with spaces"),
        ("name", False, "Should reject 'name' label"),
        ("Name:", False, "Should reject 'Name:' label"),
        ("Candidate Name", False, "Should reject 'Candidate Name' label"),
        ("AB", False, "Should reject too short names"),
        ("123", False, "Should reject numbers only"),
        ("", False, "Should reject empty string"),
        ("View Response Sheet", False, "Should reject UI text"),
        ("Priya Sharma", True, "Should accept valid Indian name"),
        ("A" * 150, False, "Should reject very long strings"),
    ]
    
    print("\nTest Results:")
    print("-" * 70)
    
    passed = 0
    failed = 0
    
    for test_input, expected, description in test_cases:
        result = is_valid_name(test_input)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} | {description}")
        print(f"       Input: '{test_input}' | Expected: {expected} | Got: {result}")
        print()
    
    print("-" * 70)
    print(f"\nSummary: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    if failed == 0:
        print("\n✅ All validation tests passed!")
        print("The 'print' issue has been fixed - UI elements are now filtered out.")
    else:
        print(f"\n⚠️  {failed} test(s) failed - validation may need adjustment")
    
    print("=" * 70)


if __name__ == "__main__":
    test_validation()
