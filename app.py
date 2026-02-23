from flask import Flask, render_template, request, jsonify, session
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import os
import logging
from scraper import ResponseSheetScraper
from predictor import MarkPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
csrf = CSRFProtect(app)

# Configure Flask logging
if not app.debug:
    app.logger.setLevel(logging.INFO)
    # Ensure logs go to stdout for cloud deployment platforms
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

class URLForm(FlaskForm):
    response_sheet_url = StringField('Response Sheet URL', 
                                     validators=[DataRequired(), URL()],
                                     render_kw={"placeholder": "Enter your response sheet URL"})
    submit = SubmitField('Predict Marks')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.response_sheet_url.data
        logger.info(f"Processing request for URL: {url}")
        
        try:
            # Scrape the response sheet
            scraper = ResponseSheetScraper(url)
            
            # Scrape candidate name from the original URL
            username = scraper.scrape_candidate_name()
            logger.info(f"Scraped username: {username}")
            
            # Extract responses and predict marks
            response_data = scraper.extract_responses()
            logger.info(f"Successfully extracted response data")
            
            # Predict marks
            predictor = MarkPredictor()
            predicted_marks = predictor.predict(response_data)
            logger.info(f"Predicted marks: {predicted_marks}")
            
            return render_template('result.html', 
                                 url=url,
                                 response_data=response_data,
                                 predicted_marks=predicted_marks,
                                 username=username,
                                 form=URLForm())
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}", exc_info=True)
            return render_template('index.html', 
                                 form=form, 
                                 error=f"Error processing URL: {str(e)}")
    
    return render_template('index.html', form=form)

@app.route('/api/scrape-username', methods=['POST'])
def api_scrape_username():
    """API endpoint to scrape only the username from a response sheet URL"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        scraper = ResponseSheetScraper(url)
        username = scraper.scrape_candidate_name()
        
        return jsonify({
            'success': True,
            'username': username,
            'url': url
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Scrape the response sheet
        scraper = ResponseSheetScraper(url)
        
        # Scrape candidate name
        username = scraper.scrape_candidate_name()
        
        # Extract responses and predict marks
        response_data = scraper.extract_responses()
        
        # Predict marks
        predictor = MarkPredictor()
        predicted_marks = predictor.predict(response_data)
        
        return jsonify({
            'success': True,
            'url': url,
            'username': username,
            'response_data': response_data,
            'predicted_marks': predicted_marks
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', form=URLForm(), error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', form=URLForm(), error="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
