# Accuracy Fixes Summary

## Issues Fixed

### 1. **Statistics Calculation (scraper.py)**
**Problem:** The statistics were not accurately reflecting the actual question counts from serblabs.in API.

**Solution:**
- Enhanced statistics calculation to properly parse correct/wrong/unanswered counts from serblabs.in API
- Added logic to count from individual question data when summary is not available
- Fixed the attempted counter to correctly sum correct + wrong answers
- Ensured not_attempted is calculated correctly from total - attempted

**Changes:**
```python
# Now properly calculates:
- correct: Questions marked correctly
- wrong: Questions marked incorrectly  
- unanswered: Questions not attempted
- attempted: correct + wrong (not including unanswered)
```

### 2. **Question Type Detection (predictor.py)**
**Problem:** Question types (1-mark vs 2-mark) were estimated only from question numbers, leading to inaccurate calculations.

**Solution:**
- Created new `get_question_type()` method that:
  - First checks actual question 'type' field from serblabs.in API
  - Parses type strings like "1 Mark", "2 Marks", "NAT", "MSQ"
  - Falls back to question number estimation only if type not available
  
**Benefits:**
- More accurate marks calculation based on actual question types
- Better handling of NAT (Numerical Answer Type) and MSQ (Multiple Select Questions)

### 3. **Correct/Wrong Distribution (predictor.py)**
**Problem:** The predictor was estimating correct/wrong answers based on assumed accuracy, even when actual data was available.

**Solution:**
- Enhanced the prediction logic to:
  1. **First priority:** Use actual score and status from each question
  2. **Second priority:** Use aggregated correct/wrong counts from statistics
  3. **Last resort:** Estimate based on accuracy heuristics
  
- Track correct/wrong for both 1-mark and 2-mark questions separately
- Calculate marks accurately based on actual data

**Code Changes:**
```python
# Now tracks:
- one_mark_correct, one_mark_wrong
- two_mark_correct, two_mark_wrong
# And uses actual question score/status to determine correctness
```

### 4. **Accuracy Calculation (predictor.py)**
**Problem:** Accuracy was always estimated, even when real data was available.

**Solution:**
- Calculate actual accuracy when correct/wrong counts are available
- Formula: `(correct / (correct + wrong)) * 100`
- Only use estimated accuracy as fallback

### 5. **Display Improvements (result.html)**
**Problem:** Display was not clearly showing which values were actual vs estimated.

**Solution:**
- Updated stats cards to:
  - Always show actual attempted count
  - Show actual correct/wrong when available, otherwise show "Estimated Correct/Wrong"
  - Added "Not Attempted" card for better visibility
  - Show breakdown of correct/wrong within 1-mark and 2-mark questions

**Visual Improvements:**
```html
Stats now show:
- Questions Attempted (always actual)
- Correct (actual if available, otherwise "Estimated Correct")
- Wrong (actual if available, otherwise "Estimated Wrong")
- Not Attempted (actual count)
- Accuracy (actual percentage if data available)
```

### 6. **Detailed Breakdown Enhancement**
**Problem:** Breakdown table didn't show per-question-type accuracy.

**Solution:**
- Added correct/wrong counts for 1-mark and 2-mark questions in breakdown
- Format: "25 (✓20 / ✗5)" shows 25 attempted with 20 correct and 5 wrong

## Testing Recommendations

1. Test with a serblabs.in URL that has complete data
2. Verify that:
   - Attempted count matches actual marked questions
   - Correct/Wrong counts match serblabs.in summary
   - 1-mark and 2-mark questions are properly categorized
   - Predicted score matches the calculation: (correct_marks - wrong_marks)
   - Accuracy percentage = (correct / (correct + wrong)) * 100

## Key Improvements

1. **More Accurate:** Uses actual data from serblabs.in instead of estimates
2. **Transparent:** Clearly shows when values are actual vs estimated
3. **Detailed:** Provides breakdown by question type (1-mark vs 2-mark)
4. **Robust:** Falls back gracefully when complete data is not available
5. **Consistent:** Statistics match across scraper, predictor, and display

## Files Modified

- `scraper.py` - Fixed statistics calculation
- `predictor.py` - Enhanced question type detection and accuracy calculation  
- `templates/result.html` - Improved display of statistics and breakdown
