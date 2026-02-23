# GATE Mark Predictor

A Flask web application that predicts GATE exam marks by submitting response sheet URLs to serblabs.in and scraping the predicted results. Features CSRF protection, beautiful UI, and seamless integration with serblabs.in prediction engine.

## 🚀 Features

- **URL-based Response Sheet Analysis**: Simply paste the response sheet URL
- **Powered by serblabs.in**: Leverages serblabs.in's prediction engine for accurate results
- **Automated Scraping**: Automatically submits URLs to serblabs.in and retrieves predictions
- **CSRF Protection**: Secure forms with Flask-WTF CSRF protection
- **Beautiful UI**: Modern, responsive design with gradient backgrounds
- **Detailed Breakdown**: View comprehensive statistics and mark distribution
- **API Endpoint**: Programmatic access for integration with other tools

## 🔧 How It Works

1. User submits a GATE response sheet URL through the web form
2. Application submits this URL to **serblabs.in** (your prediction website)
3. Scrapes the predicted marks result from serblabs.in
4. Displays the prediction with detailed breakdown and analysis
5. Uses serblabs.in as the primary prediction source with fallback estimation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /home/mothish/Desktop/gatepridictor
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   # On Linux/Mac
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

## 🎯 Usage

### Running the Application

1. **Start the Flask development server**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

3. **Enter Response Sheet URL**:
   - Paste the URL of your GATE response sheet
   - Click "Predict Marks"
   - View your predicted score and detailed breakdown

### API Usage

You can also use the API endpoint for programmatic access:

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/response-sheet"}'
```

## 📁 Project Structure

```
gatepridictor/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── scraper.py              # Web scraping logic
├── predictor.py            # Mark prediction algorithms
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page with form
│   └── result.html        # Results page
└── static/
    └── css/
        └── style.css      # Styling
```

## 🔒 Security Features

- **CSRF Protection**: All forms are protected against Cross-Site Request Forgery
- **URL Validation**: Input URLs are validated before processing
- **Error Handling**: Comprehensive error handling for failed requests
- **Secure Headers**: Security best practices implemented

## 🎨 Customization

### Changing the Secret Key

For production, always set a strong secret key:

```bash
export SECRET_KEY='your-very-secure-random-secret-key'
```

Or in your `.env` file:
```
SECRET_KEY=your-very-secure-random-secret-key
```

### Modifying Prediction Algorithm

Edit `predictor.py` to customize:
- Mark distribution (1-mark vs 2-mark questions)
- Accuracy estimation algorithm
- Grade cutoffs
- Negative marking scheme

### Styling

Modify `static/css/style.css` to change:
- Color scheme (CSS variables in `:root`)
- Layout and spacing
- Animations and transitions

## 📊 How It Works

1. **URL Scraping**: The application fetches the response sheet page
2. **Data Extraction**: BeautifulSoup parses HTML to extract responses
3. **Pattern Recognition**: Identifies question numbers and marked answers
4. **Mark Calculation**: Applies GATE marking scheme (+1/+2 for correct, -1/3 or -2/3 for wrong)
5. **Accuracy Estimation**: Uses heuristics based on attempt count
6. **Score Prediction**: Calculates predicted, best-case, and worst-case scores

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found error
```bash
pip install -r requirements.txt
```

**Issue**: Port already in use
```bash
# Change port in app.py or kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

**Issue**: CSRF token missing
- Ensure cookies are enabled
- Check that WTF_CSRF_ENABLED is True in config

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, visit [SerbLabs](https://serblabs.in)

## ⚠️ Disclaimer

This tool provides estimated marks based on algorithms and may not reflect actual GATE results. Use it as a guide only. Actual marks depend on the official answer key, normalization, and other factors.
