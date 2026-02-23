import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseSheetScraper:
    """Submits URL to serblabs.in and scrapes the predicted marks result"""
    
    def __init__(self, url, timeout=30, max_retries=3):
        self.response_sheet_url = url  # The URL user provides
        self.target_website = "https://serblabs.in/"  # The website to submit to
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.responses = []
        
    def validate_url(self):
        """Validate the response sheet URL format"""
        try:
            result = urlparse(self.response_sheet_url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def scrape_candidate_name(self):
        """Scrape candidate name directly from the GATE response sheet URL"""
        
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
        
        try:
            # Fetch the actual GATE response sheet page
            response = self.session.get(self.response_sheet_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'noscript']):
                script.decompose()
            
            candidate_name = None
            
            # Pattern 1: Look for text containing "Candidate Name" or "Name" label
            for label in soup.find_all(['td', 'th', 'label', 'span', 'div']):
                text = label.get_text(strip=True)
                if text and re.search(r'\bCandidate\s*Name\b|\bName\s*:\s*$|\bName\s*$', text, re.IGNORECASE):
                    # Try to get the next sibling or adjacent element
                    if label.name == 'td':
                        next_td = label.find_next_sibling('td')
                        if next_td:
                            potential_name = next_td.get_text(strip=True)
                            if is_valid_name(potential_name):
                                candidate_name = potential_name
                                break
                    elif label.name == 'th':
                        # Look in the same row for td
                        row = label.find_parent('tr')
                        if row:
                            tds = row.find_all('td')
                            for td in tds:
                                potential_name = td.get_text(strip=True)
                                if is_valid_name(potential_name):
                                    candidate_name = potential_name
                                    break
                    else:
                        # Look for next elements
                        next_elem = label.find_next(['span', 'div', 'td'])
                        if next_elem:
                            potential_name = next_elem.get_text(strip=True)
                            if is_valid_name(potential_name):
                                candidate_name = potential_name
                                break
                    
                    if candidate_name:
                        break
            
            # Pattern 2: Look for input fields with name-related attributes
            if not candidate_name:
                name_inputs = soup.find_all('input', {
                    'id': re.compile(r'.*\bname\b.*', re.IGNORECASE),
                    'name': re.compile(r'.*\bname\b.*', re.IGNORECASE)
                })
                for inp in name_inputs:
                    if inp.get('value'):
                        potential_name = inp.get('value').strip()
                        if is_valid_name(potential_name):
                            candidate_name = potential_name
                            break
            
            # Pattern 3: Look in tables specifically for name rows
            if not candidate_name:
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        for i, cell in enumerate(cells):
                            cell_text = cell.get_text(strip=True)
                            # Check if this cell is a "name" label
                            if re.search(r'\bCandidate\s*Name\b|\bName\b', cell_text, re.IGNORECASE) and i + 1 < len(cells):
                                potential_name = cells[i + 1].get_text(strip=True)
                                if is_valid_name(potential_name):
                                    candidate_name = potential_name
                                    break
                        if candidate_name:
                            break
                    if candidate_name:
                        break
            
            # Clean up the name if found
            if candidate_name:
                # Remove extra whitespace
                candidate_name = ' '.join(candidate_name.split())
                return candidate_name
            
            return "Candidate"
            
        except Exception as e:
            logger.error(f"Error scraping candidate name: {str(e)}")
            return "Candidate"
    
    def get_serblabs_page(self):
        """Fetch the serblabs.in webpage to get the form"""
        try:
            response = self.session.get(self.target_website, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch serblabs.in: {str(e)}")
    
    def submit_to_serblabs(self):
        """Submit the response sheet URL to serblabs.in API and get the result"""
        if not self.validate_url():
            raise ValueError("Invalid response sheet URL format")
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # serblabs.in uses a REST API endpoint /calculate
                api_endpoint = self.target_website.rstrip('/') + '/calculate'
                
                # Prepare JSON payload as per their API
                payload = {
                    'response_url': self.response_sheet_url
                }
                
                # Update headers for JSON API submission
                api_headers = self.headers.copy()
                api_headers['Content-Type'] = 'application/json'
                api_headers['Accept'] = 'application/json'
                api_headers['Referer'] = self.target_website
                api_headers['Origin'] = self.target_website.rstrip('/')
                
                # Debug logging
                logger.info(f"[Attempt {attempt + 1}/{self.max_retries}] Submitting to {api_endpoint}")
                
                # Submit to the API endpoint
                response = self.session.post(
                    api_endpoint, 
                    json=payload,  # requests will handle JSON encoding
                    headers=api_headers, 
                    timeout=self.timeout
                )
                
                # Debug logging
                logger.info(f"Response Status: {response.status_code}")
                logger.debug(f"Response Headers: {dict(response.headers)}")
                logger.info(f"Response Length: {len(response.text)} bytes")
                
                response.raise_for_status()
                
                # Check if response is empty
                if not response.text or len(response.text.strip()) == 0:
                    raise Exception("Received empty response from serblabs.in API")
                
                # Check content type
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    # Log the actual response for debugging
                    response_preview = response.text[:500] if len(response.text) > 500 else response.text
                    logger.warning(f"Unexpected content type: {content_type}")
                    logger.warning(f"Response preview: {response_preview}")
                    raise Exception(f"Invalid response format (expected JSON, got {content_type}). Response: {response_preview}")
                
                # Try to parse JSON with better error handling
                try:
                    json_data = response.json()
                    logger.info(f"Successfully parsed JSON response")
                    return json_data
                except json.JSONDecodeError as je:
                    response_preview = response.text[:500] if len(response.text) > 500 else response.text
                    logger.error(f"JSON decode error: {str(je)}")
                    logger.error(f"Response text: {response_preview}")
                    raise Exception(f"Invalid JSON response from serblabs.in: {str(je)}. Response: {response_preview}")
                
            except requests.HTTPError as he:
                # Handle HTTP errors specifically
                status_code = he.response.status_code if hasattr(he, 'response') else 'unknown'
                response_text = he.response.text[:500] if hasattr(he, 'response') and he.response.text else 'No response body'
                last_error = f"HTTP {status_code} error from serblabs.in: {response_text}"
                logger.error(f"HTTP Error on attempt {attempt + 1}: {last_error}")
                
                # Don't retry on 4xx client errors (except 429 rate limit)
                if hasattr(he, 'response') and 400 <= he.response.status_code < 500 and he.response.status_code != 429:
                    raise Exception(last_error)
                    
                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except requests.Timeout:
                last_error = f"Request timed out after {self.timeout} seconds. serblabs.in may be slow or unavailable."
                logger.error(f"Timeout on attempt {attempt + 1}: {last_error}")
                
                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except requests.ConnectionError as ce:
                last_error = f"Connection failed to serblabs.in. Please check your internet connection or the service may be down: {str(ce)}"
                logger.error(f"Connection error on attempt {attempt + 1}: {last_error}")
                
                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except requests.RequestException as e:
                last_error = f"Failed to submit to serblabs.in: {str(e)}"
                logger.error(f"Request error on attempt {attempt + 1}: {last_error}")
                
                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                last_error = str(e)
                logger.error(f"General error on attempt {attempt + 1}: {last_error}")
                
                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
        
        # If we've exhausted all retries, raise the last error
        raise Exception(f"Failed after {self.max_retries} attempts. Last error: {last_error}")
    
    def parse_serblabs_result(self, json_response):
        """Parse the JSON result from serblabs.in API to extract predicted marks"""
        
        result_data = {
            'predicted_marks': None,
            'positive_marks': None,
            'negative_marks': None,
            'questions': [],
            'candidate_info': {},
            'exam_info': {},
            'raw_result': json_response
        }
        
        # Validate json_response
        if not json_response:
            result_data['error'] = 'Empty API response'
            return result_data
        
        # If json_response is a string (error case), try to parse it
        if isinstance(json_response, str):
            try:
                json_response = json.loads(json_response)
            except json.JSONDecodeError as e:
                result_data['error'] = f'Failed to parse API response: {str(e)}'
                return result_data
        
        # Check if the response indicates an error
        if isinstance(json_response, dict):
            if 'error' in json_response:
                result_data['error'] = json_response['error']
                return result_data
            if 'message' in json_response and not json_response.get('summary'):
                # If there's a message but no summary, might be an error
                result_data['error'] = json_response['message']
                return result_data
        
        # serblabs.in API returns: { "summary": {...}, "results": [...] }
        # Extract summary data
        summary = json_response.get('summary', {})
        
        if not summary:
            # If no summary, the response might not be in the expected format
            result_data['error'] = f'Unexpected API response format. Keys found: {list(json_response.keys()) if isinstance(json_response, dict) else "N/A"}'
            result_data['raw_result'] = str(json_response)[:1000]
            return result_data
        
        # Extract predicted marks (total_marks from summary)
        if 'total_marks' in summary:
            try:
                result_data['predicted_marks'] = float(summary['total_marks'])
            except (ValueError, TypeError):
                pass
        
        # Extract additional summary statistics
        if 'correct' in summary:
            result_data['correct_count'] = summary['correct']
        if 'wrong' in summary:
            result_data['wrong_count'] = summary['wrong']
        if 'unanswered' in summary:
            result_data['unanswered_count'] = summary['unanswered']
        if 'total_questions' in summary:
            result_data['total_questions_count'] = summary['total_questions']
        
        # Extract normalized marks if available (CS only)
        if 'normalized_marks' in summary and summary['normalized_marks'] is not None:
            try:
                result_data['normalized_marks'] = float(summary['normalized_marks'])
            except (ValueError, TypeError):
                pass
        
        # Extract rank if available
        if 'rank' in summary and summary['rank']:
            try:
                result_data['predicted_rank'] = int(summary['rank'])
            except (ValueError, TypeError):
                pass
        
        if 'total_students' in summary:
            result_data['total_students'] = summary['total_students']
        
        # Extract normalized rank if available
        if 'normalized_rank' in summary and summary['normalized_rank']:
            try:
                result_data['normalized_rank'] = int(summary['normalized_rank'])
            except (ValueError, TypeError):
                pass
        
        # Extract subject and shift info
        if 'subject' in summary:
            result_data['exam_info']['subject'] = summary['subject']
        if 'shift' in summary:
            result_data['exam_info']['shift'] = summary['shift']
        
        # Extract candidate information
        candidate = json_response.get('candidate', {})
        if candidate:
            if 'name' in candidate:
                result_data['candidate_info']['name'] = candidate['name']
            if 'registration_number' in candidate or 'enrollment_id' in candidate:
                result_data['candidate_info']['registration_number'] = candidate.get('registration_number', candidate.get('enrollment_id', ''))
            if 'email' in candidate:
                result_data['candidate_info']['email'] = candidate['email']
        
        # Alternative: Extract from summary if not in candidate object
        if not result_data['candidate_info'].get('name'):
            if 'candidate_name' in summary:
                result_data['candidate_info']['name'] = summary['candidate_name']
            elif 'name' in summary:
                result_data['candidate_info']['name'] = summary['name']
        
        if not result_data['candidate_info'].get('registration_number'):
            if 'enrollment_id' in summary:
                result_data['candidate_info']['registration_number'] = summary['enrollment_id']
            elif 'registration_number' in summary:
                result_data['candidate_info']['registration_number'] = summary['registration_number']
        
        # Extract section-wise marks
        if 'section_marks' in summary:
            result_data['exam_info']['section_marks'] = summary['section_marks']
        if 'section_possible' in summary:
            result_data['exam_info']['section_possible'] = summary['section_possible']
        
        # Extract question type statistics
        if 'type_stats' in summary:
            result_data['exam_info']['type_stats'] = summary['type_stats']
        
        # Extract marking details (positive/negative marks)
        if 'positive_marks' in summary:
            try:
                result_data['positive_marks'] = float(summary['positive_marks'])
            except (ValueError, TypeError):
                pass
            
        if 'negative_marks' in summary:
            try:
                result_data['negative_marks'] = float(summary['negative_marks'])
            except (ValueError, TypeError):
                pass
        
        # Extract question-wise data from results array
        results_array = json_response.get('results', [])
        if isinstance(results_array, list):
            result_data['questions'] = []
            for i, q in enumerate(results_array, 1):
                if isinstance(q, dict):
                    result_data['questions'].append({
                        'number': q.get('qno', q.get('question_number', i)),
                        'response': q.get('marked_option', q.get('response', '')),
                        'correct_answer': q.get('answer_key', q.get('correct', '')),
                        'status': q.get('status', ''),
                        'score': q.get('score', 0),
                        'section': q.get('section', ''),
                        'type': q.get('type', ''),
                        'marked': bool(q.get('marked_option')) or bool(q.get('response'))
                    })
        
        # Store the entire response for debugging (limit size)
        result_data['raw_result'] = str(json_response)[:1000]
        
        return result_data
    
    def extract_responses(self):
        """Main method to submit URL to serblabs.in and extract predicted marks"""
        try:
            # Submit the URL to serblabs.in API (returns JSON)
            result_json = self.submit_to_serblabs()
            
            # Parse the JSON result from serblabs.in
            result_data = self.parse_serblabs_result(result_json)
            
            # Check if parsing resulted in an error
            if 'error' in result_data and result_data['error']:
                raise Exception(result_data['error'])
            
            # Sort questions by number if any
            if result_data.get('questions'):
                result_data['questions'].sort(key=lambda x: x.get('number', 0))
            
            # Calculate statistics from parsed data
            # Use serblabs.in summary if available, otherwise calculate
            total_questions = result_data.get('total_questions_count', len(result_data.get('questions', [])))
            
            # Try to get counts from serblabs summary first
            correct = result_data.get('correct_count', 0)
            wrong = result_data.get('wrong_count', 0)
            unanswered = result_data.get('unanswered_count', 0)
            
            # Calculate attempted from questions if summary not available
            if correct == 0 and wrong == 0 and result_data.get('questions'):
                # Count from questions array
                for q in result_data.get('questions', []):
                    if q.get('marked', False):
                        status = q.get('status', '').lower()
                        if 'correct' in status or q.get('score', 0) > 0:
                            correct += 1
                        elif 'wrong' in status or 'incorrect' in status:
                            wrong += 1
                        else:
                            # If status not clear, mark as attempted but unknown
                            wrong += 1
                    else:
                        unanswered += 1
            
            attempted = correct + wrong
            
            # Ensure not_attempted is calculated correctly
            if unanswered == 0 and total_questions > 0:
                not_attempted = total_questions - attempted
            else:
                not_attempted = unanswered
            
            result_data['statistics'] = {
                'total_questions': total_questions,
                'attempted': attempted,
                'not_attempted': not_attempted,
                'correct': correct,
                'wrong': wrong,
                'unanswered': not_attempted
            }
            
            # Add the original URL that was submitted
            result_data['submitted_url'] = self.response_sheet_url
            result_data['processed_by'] = self.target_website
            
            return result_data
        
        except Exception as e:
            # Re-raise with clear context
            error_msg = str(e)
            if "Failed to submit to serblabs.in" not in error_msg:
                error_msg = f"Failed to process response sheet: {error_msg}"
            raise Exception(error_msg)

