import random
from typing import Dict, List

class MarkPredictor:
    """Processes marks prediction from serblabs.in and provides additional analysis"""
    
    def __init__(self):
        # GATE marking scheme (typical)
        self.marks_per_question = {
            '1_mark': 1,
            '2_mark': 2
        }
        self.negative_marking = {
            '1_mark': 1/3,  # -0.33 for wrong answer
            '2_mark': 2/3   # -0.66 for wrong answer
        }
        
        # Default distribution (can be customized based on exam)
        self.question_distribution = {
            '1_mark': 25,
            '2_mark': 40
        }
        
        # Max marks (typical GATE)
        self.max_marks = 100
        
    def get_question_type(self, question_data):
        """Get question type from question data or estimate based on number"""
        # First try to get from actual data
        q_type = question_data.get('type', '')
        
        # Parse type from serblabs data (might be "1 Mark", "2 Marks", "MSQ", "NAT", etc.)
        if '1' in str(q_type).upper() or 'NAT' in str(q_type).upper():
            return '1_mark'
        elif '2' in str(q_type).upper() or 'MSQ' in str(q_type).upper():
            return '2_mark'
        
        # Fallback: estimate based on question number (typical GATE pattern)
        # Questions 1-25 are typically 1 mark, 26-65 are typically 2 marks
        question_number = question_data.get('number', 0)
        if question_number <= 25:
            return '1_mark'
        else:
            return '2_mark'
    
    def calculate_accuracy_estimate(self, total_attempted):
        """
        Estimate accuracy based on typical performance
        This can be enhanced with ML models trained on historical data
        """
        # Higher attempt count might mean better preparation
        # This is a simplified heuristic
        if total_attempted < 20:
            base_accuracy = 0.50
        elif total_attempted < 40:
            base_accuracy = 0.60
        elif total_attempted < 55:
            base_accuracy = 0.70
        else:
            base_accuracy = 0.65  # Very high attempts might include guesses
        
        # Add some randomness for realistic prediction
        accuracy = base_accuracy + random.uniform(-0.05, 0.05)
        return max(0.3, min(0.9, accuracy))  # Clamp between 30% and 90%
    
    def predict(self, response_data: Dict) -> Dict:
        """
        Process marks prediction from serblabs.in result
        
        Returns a dictionary with:
        - predicted_score (from serblabs.in if available)
        - best_case_score
        - worst_case_score
        - breakdown
        - source (serblabs or local estimate)
        """
        questions = response_data.get('questions', [])
        statistics = response_data.get('statistics', {})
        
        # Check if serblabs.in provided a predicted score
        serblabs_score = response_data.get('predicted_marks')
        
        attempted = statistics.get('attempted', 0)
        not_attempted = statistics.get('not_attempted', 0)
        total_questions = statistics.get('total_questions', 0)
        
        # If serblabs provided a score, use it as primary prediction
        if serblabs_score is not None:
            predicted_score = float(serblabs_score)
            source = 'serblabs.in'
            
            # Estimate the breakdown based on the score
            # This is a reverse calculation to provide context
            if total_questions > 0:
                avg_accuracy = min(0.9, max(0.3, predicted_score / self.max_marks))
            else:
                avg_accuracy = 0.5
                
        else:
            # Fallback to local estimation if serblabs didn't provide a score
            source = 'local_estimate'
            
            if attempted == 0:
                return {
                    'predicted_score': 0,
                    'best_case_score': 0,
                    'worst_case_score': 0,
                    'accuracy_estimate': 0,
                    'breakdown': {
                        'attempted': 0,
                        'not_attempted': not_attempted,
                        'estimated_correct': 0,
                        'estimated_wrong': 0
                    },
                    'grade': 'N/A',
                    'source': source,
                    'raw_result': response_data.get('raw_result', 'N/A')
                }
            
            # Estimate accuracy
            avg_accuracy = self.calculate_accuracy_estimate(attempted)
        
        # Calculate marks for each question to provide breakdown
        total_positive_marks = 0
        total_negative_marks = 0
        
        one_mark_attempted = 0
        two_mark_attempted = 0
        one_mark_correct = 0
        two_mark_correct = 0
        one_mark_wrong = 0
        two_mark_wrong = 0
        
        # Count by question type using actual data
        for question in questions:
            if question.get('marked', False):
                q_type = self.get_question_type(question)
                score = question.get('score', 0)
                status = question.get('status', '').lower()
                
                if q_type == '1_mark':
                    one_mark_attempted += 1
                    # Determine if correct or wrong from actual data
                    if score > 0 or 'correct' in status:
                        one_mark_correct += 1
                    elif score < 0 or 'wrong' in status or 'incorrect' in status:
                        one_mark_wrong += 1
                else:
                    two_mark_attempted += 1
                    if score > 0 or 'correct' in status:
                        two_mark_correct += 1
                    elif score < 0 or 'wrong' in status or 'incorrect' in status:
                        two_mark_wrong += 1
        
        # If we have actual correct/wrong counts from statistics, use them to estimate distribution
        actual_correct = statistics.get('correct', 0)
        actual_wrong = statistics.get('wrong', 0)
        
        # If we counted correct/wrong from questions, use that
        if one_mark_correct > 0 or two_mark_correct > 0:
            estimated_correct_1m = one_mark_correct
            estimated_wrong_1m = one_mark_wrong
            estimated_correct_2m = two_mark_correct
            estimated_wrong_2m = two_mark_wrong
        # Otherwise use actual totals with accuracy-based distribution
        elif actual_correct > 0 or actual_wrong > 0:
            # Distribute actual counts proportionally
            total_attempted = one_mark_attempted + two_mark_attempted
            if total_attempted > 0:
                ratio_1m = one_mark_attempted / total_attempted
                estimated_correct_1m = int(actual_correct * ratio_1m)
                estimated_wrong_1m = int(actual_wrong * ratio_1m)
                estimated_correct_2m = actual_correct - estimated_correct_1m
                estimated_wrong_2m = actual_wrong - estimated_wrong_1m
            else:
                estimated_correct_1m = estimated_wrong_1m = 0
                estimated_correct_2m = estimated_wrong_2m = 0
        else:
            # Fallback to accuracy estimation
            estimated_correct_1m = int(one_mark_attempted * avg_accuracy)
            estimated_wrong_1m = one_mark_attempted - estimated_correct_1m
            estimated_correct_2m = int(two_mark_attempted * avg_accuracy)
            estimated_wrong_2m = two_mark_attempted - estimated_correct_2m
        
        # Calculate marks for breakdown
        positive_marks_1m = estimated_correct_1m * self.marks_per_question['1_mark']
        negative_marks_1m = estimated_wrong_1m * self.negative_marking['1_mark']
        
        positive_marks_2m = estimated_correct_2m * self.marks_per_question['2_mark']
        negative_marks_2m = estimated_wrong_2m * self.negative_marking['2_mark']
        
        total_positive_marks = positive_marks_1m + positive_marks_2m
        total_negative_marks = negative_marks_1m + negative_marks_2m
        
        # Check if serblabs provided actual positive/negative marks
        serblabs_positive_marks = response_data.get('positive_marks')
        serblabs_negative_marks = response_data.get('negative_marks')
        
        if serblabs_positive_marks is not None:
            total_positive_marks = float(serblabs_positive_marks)
        if serblabs_negative_marks is not None:
            total_negative_marks = float(serblabs_negative_marks)
        
        # If serblabs didn't provide score, calculate it from our breakdown
        if serblabs_score is None:
            predicted_score = round(total_positive_marks - total_negative_marks, 2)
        
        # Calculate actual accuracy if we have real correct/wrong data
        total_correct = estimated_correct_1m + estimated_correct_2m
        total_wrong = estimated_wrong_1m + estimated_wrong_2m
        total_answered = total_correct + total_wrong
        
        if total_answered > 0 and (actual_correct > 0 or actual_wrong > 0):
            # Use actual accuracy from data
            actual_accuracy = (actual_correct / (actual_correct + actual_wrong)) * 100 if (actual_correct + actual_wrong) > 0 else avg_accuracy * 100
        else:
            actual_accuracy = avg_accuracy * 100
        
        # Best case: all attempted are correct
        best_case = round(
            one_mark_attempted * self.marks_per_question['1_mark'] +
            two_mark_attempted * self.marks_per_question['2_mark'],
            2
        )
        
        # Worst case: all attempted are wrong
        worst_case = round(
            -(one_mark_attempted * self.negative_marking['1_mark'] +
              two_mark_attempted * self.negative_marking['2_mark']),
            2
        )
        
        # Determine grade estimate
        grade = self.estimate_grade(predicted_score)
        
        return {
            'predicted_score': predicted_score,
            'best_case_score': best_case,
            'worst_case_score': worst_case,
            'accuracy_estimate': round(actual_accuracy, 1),
            'breakdown': {
                'total_questions': total_questions if total_questions > 0 else len(questions),
                'attempted': attempted,
                'not_attempted': not_attempted,
                '1_mark_attempted': one_mark_attempted,
                '2_mark_attempted': two_mark_attempted,
                'estimated_correct': total_correct if total_correct > 0 else estimated_correct_1m + estimated_correct_2m,
                'estimated_wrong': total_wrong if total_wrong > 0 else estimated_wrong_1m + estimated_wrong_2m,
                'positive_marks': round(total_positive_marks, 2),
                'negative_marks': round(total_negative_marks, 2),
                '1_mark_correct': estimated_correct_1m,
                '1_mark_wrong': estimated_wrong_1m,
                '2_mark_correct': estimated_correct_2m,
                '2_mark_wrong': estimated_wrong_2m
            },
            'grade': grade,
            'source': source,
            'processed_by': response_data.get('processed_by', 'local'),
            'raw_result': response_data.get('raw_result', '')
        }
    
    def estimate_grade(self, score):
        """Estimate grade based on typical GATE cutoffs"""
        if score >= 55:
            return 'Excellent (Likely to qualify with good rank)'
        elif score >= 45:
            return 'Very Good (Likely to qualify)'
        elif score >= 35:
            return 'Good (May qualify depending on category)'
        elif score >= 25:
            return 'Average (Border line)'
        else:
            return 'Needs Improvement'
