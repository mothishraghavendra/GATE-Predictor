#!/usr/bin/env python3
"""
Debug script to see what serblabs.in actually returns
"""

import requests
from bs4 import BeautifulSoup
import json

# First, let's check the HTML structure
print("=" * 60)
print("Fetching serblabs.in homepage...")
print("=" * 60)

response = requests.get('https://serblabs.in/')
html = response.text

print(f"\nStatus Code: {response.status_code}")
print(f"Content Length: {len(html)} bytes")

# Parse HTML to find form and input fields
soup = BeautifulSoup(html, 'html.parser')

# Find the form
forms = soup.find_all('form')
print(f"\n📋 Found {len(forms)} form(s)")

for i, form in enumerate(forms):
    print(f"\n--- Form {i+1} ---")
    print(f"Action: {form.get('action', 'N/A')}")
    print(f"Method: {form.get('method', 'N/A')}")
    
    inputs = form.find_all('input')
    print(f"Input fields: {len(inputs)}")
    for inp in inputs:
        print(f"  - {inp.get('name', 'no-name')}: type={inp.get('type', 'text')}, id={inp.get('id', 'N/A')}")
    
    textareas = form.find_all('textarea')
    for ta in textareas:
        print(f"  - {ta.get('name', 'no-name')}: textarea, id={ta.get('id', 'N/A')}")

# Find all input fields (even outside forms)
print("\n" + "=" * 60)
print("All Input Fields on Page:")
print("=" * 60)
all_inputs = soup.find_all('input')
for inp in all_inputs:
    print(f"  - name='{inp.get('name', 'N/A')}', id='{inp.get('id', 'N/A')}', type='{inp.get('type', 'text')}'")

# Find buttons
buttons = soup.find_all('button')
print(f"\n🔘 Found {len(buttons)} button(s)")
for btn in buttons:
    print(f"  - {btn.get_text(strip=True)}: onclick={btn.get('onclick', 'N/A')}, id={btn.get('id', 'N/A')}")

# Look for JavaScript code that handles form submission
print("\n" + "=" * 60)
print("JavaScript Code (looking for fetch/ajax/submit):")
print("=" * 60)
scripts = soup.find_all('script')
for i, script in enumerate(scripts):
    script_text = script.string or script.get_text()
    if script_text and ('fetch' in script_text or 'ajax' in script_text or 'calculate' in script_text.lower()):
        print(f"\n--- Script {i+1} (relevant) ---")
        print(script_text[:800])
        print("...")

# Look for API endpoints in the HTML
print("\n" + "=" * 60)
print("Looking for API endpoints...")
print("=" * 60)
import re
api_patterns = [
    r'/api/\w+',
    r'/calculate',
    r'/predict',
    r'/analyze',
    r'fetch\(["\']([^"\']+)["\']',
    r'\.post\(["\']([^"\']+)["\']',
]

for pattern in api_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"Pattern '{pattern}': {set(matches)}")

print("\n" + "=" * 60)
print("Now let's try to understand the actual submission mechanism")
print("=" * 60)

# Find the specific input field for URL
url_input = soup.find('input', {'type': 'url'}) or soup.find('input', {'type': 'text'}) or soup.find('textarea')
if url_input:
    print(f"\nPrimary URL input field:")
    print(f"  Name: {url_input.get('name', 'N/A')}")
    print(f"  ID: {url_input.get('id', 'N/A')}")
    print(f"  Placeholder: {url_input.get('placeholder', 'N/A')}")

print("\n" + "=" * 60)
print("Full HTML (first 2000 chars):")
print("=" * 60)
print(html[:2000])
