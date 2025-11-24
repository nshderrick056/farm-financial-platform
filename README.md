🌾 Farm Financial Intelligence Platform

A comprehensive web application for analyzing U.S. farm financial performance using USDA Agricultural Resource Management Survey (ARMS) data.

📋 Table of Contents

Overview
Features
Live Demo
Technology Stack
Getting Started
Deployment
API Documentation
Usage Examples
Project Structure
Challenges & Solutions
Future Enhancements
Contributing
Credits
License


🎯 **Overview**
The Farm Financial Intelligence Platform empowers farmers, agricultural consultants, researchers, and policymakers to make data-driven decisions by providing easy access to comprehensive USDA farm financial data. The platform transforms complex agricultural economic data into actionable insights through interactive visualizations and comparative analysis tools.
Problem Statement
Agricultural professionals often struggle to:

Access and analyze comprehensive farm financial data
Compare their operations against industry benchmarks
Identify financial trends and patterns across different farm types
Make informed business decisions based on reliable data

Our Solution
A user-friendly web platform that:

✅ Provides instant access to USDA's comprehensive ARMS database
✅ Enables multi-year trend analysis and comparisons
✅ Offers interactive data exploration with search and sort capabilities
✅ Presents complex financial data in easy-to-understand formats
✅ Scales efficiently with load-balanced architecture


✨ Features
📊 Financial Analysis Tools

Farm Business Income Statement

Revenue and expense analysis
Net farm income calculations
Multi-year trend comparisons
Breakdown by production specialty


Balance Sheet Analysis

Assets and liabilities tracking
Net worth calculations
Debt-to-asset ratios
Equity position analysis


Financial Performance Ratios

Profitability metrics
Liquidity indicators
Solvency ratios
Efficiency measurements


Structural Characteristics

Farm size and acreage data
Production specialties
Operator demographics
Resource allocation patterns


Comparative Analysis

Farm typology comparisons
Economic class benchmarking
Regional performance analysis
Historical trend identification



🔍 Interactive Features

Smart Search: Real-time filtering across all data fields
Dynamic Sorting: Click any column header to sort data
Multi-Year Selection: Analyze trends across multiple years
Category Filtering: Segment data by farm type, region, size, and more
Responsive Design: Seamless experience on desktop and mobile devices

🚀 Technical Features

Load Balanced Architecture: High availability across multiple servers
RESTful API: Clean, documented endpoints for data access
Error Handling: Graceful degradation with informative error messages
Secure: API key management and input validation
Scalable: Designed to handle concurrent users efficiently


🌐 Live Demo
Production URL (Load Balanced): http://98.93.205.189
Individual Servers:

Web01: http://18.212.56.252
Web02: http://3.84.115.138

Demo Video: Watch on YouTube https://youtu.be/Jeb0Jv5HddM

🛠 Technology Stack
Backend

Python 3.8+: Core programming language
Flask 3.0.0: Web application framework
Gunicorn 21.2.0: WSGI HTTP server for production
Requests 2.31.0: HTTP library for API communication
Python-dotenv 1.0.0: Environment variable management

Frontend

HTML5: Semantic markup
CSS3: Modern styling with flexbox and grid
Vanilla JavaScript: Interactive features without dependencies
Responsive Design: Mobile-first approach

Infrastructure

Nginx: Web server and reverse proxy
Ubuntu 20.04 LTS: Server operating system
Load Balancer: Distributes traffic across multiple servers
Systemd: Service management

External APIs

USDA Economic Research Service (ERS): ARMS Data API

Base URL: https://www.ers.usda.gov/developer
Documentation: USDA ARMS API Docs




🚀 Getting Started
Prerequisites

Python 3.8 or higher
pip (Python package manager)
Virtual environment support
USDA API key (free registration at api.data.gov)

Installation

Clone the repository

bash   git clone https://github.com/yourusername/farm-financial-platform.git
   cd farm-financial-platform

Create and activate virtual environment

bash   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

bash   pip install -r requirements.txt

Configure environment variables

bash   # Create .env file
   cp .env.example .env
   
   # Edit .env and add your API key
   nano .env
Add the following:
   USDA_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here

Run the application

bash   python app.py

Access the application

Open your browser and navigate to: http://localhost:5000



Testing
bash# Test API client
python api_client.py

# Test CLI version
python cli_app.py

# Run health check
curl http://localhost:5000/health

🌍 Deployment
Architecture Overview
Internet → Load Balancer (Lb01) → Web Server 01 (Flask + Gunicorn + Nginx)
                                 → Web Server 02 (Flask + Gunicorn + Nginx)
Deployment Steps
1. Prepare Servers
On both Web01 and Web02:
bash# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone repository
cd /var/www
sudo mkdir farm-app
sudo chown $USER:$USER farm-app
cd farm-app
git clone https://github.com/yourusername/farm-financial-platform.git .
2. Set Up Application
bash# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
nano .env
# Add USDA_API_KEY and SECRET_KEY
3. Create Systemd Service
bashsudo nano /etc/systemd/system/farm-app.service
Add:
ini[Unit]
Description=Farm Financial Platform
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/farm-app
Environment="PATH=/var/www/farm-app/venv/bin"
EnvironmentFile=/var/www/farm-app/.env
ExecStart=/var/www/farm-app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
Start service:
bashsudo systemctl daemon-reload
sudo systemctl start farm-app
sudo systemctl enable farm-app
4. Configure Nginx
bashsudo nano /etc/nginx/sites-available/farm-app
Add:
nginxserver {
    listen 80;
    server_name your_server_ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }
}
Enable site:
bashsudo ln -s /etc/nginx/sites-available/farm-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
5. Configure Load Balancer
On Lb01:
bashsudo nano /etc/nginx/sites-available/farm-lb
Add:
nginxupstream farm_backend {
    least_conn;
    server web01_ip:80 max_fails=3 fail_timeout=30s;
    server web02_ip:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name lb_ip;

    location / {
        proxy_pass http://farm_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        proxy_pass http://farm_backend/health;
    }
}
Enable and restart:
bashsudo ln -s /etc/nginx/sites-available/farm-lb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
Verification
bash# Test individual servers
curl http://web01-ip/health
curl http://web02-ip/health

# Test load balancer
curl http://lb-ip/health

# Test failover
# Stop one server and verify requests still work

📚 API Documentation
Base Endpoints
Health Check
httpGET /health
Response:
json{
  "status": "healthy",
  "service": "farm-financial-platform",
  "version": "1.0.0"
}
Get Available Years
httpGET /api/years
Get Available States
httpGET /api/states
Get Income Statement
httpPOST /api/income-statement
Content-Type: application/json

{
  "years": [2020, 2019],
  "state": "all",
  "category": "collapsed farm typology"
}
Get Balance Sheet
httpPOST /api/balance-sheet
Content-Type: application/json

{
  "years": [2020],
  "state": "all"
}
Full API Reference
For complete API documentation, see API.md

💡 Usage Examples
Example 1: Analyze Income Trends
pythonfrom api_client import USDAClient

client = USDAClient()

# Get income data for multiple years
data = client.get_income_statement(
    years=[2020, 2019, 2018],
    state='all',
    category='economic class'
)

# Process results
for record in data['data']:
    print(f"Year: {record['year']}, Income: {record['net_farm_income']}")
Example 2: Compare Farm Types
python# Compare different farm types for 2020
comparison = client.compare_by_farm_typology(
    year=2020,
    report='Farm Business Income Statement'
)
Example 3: Regional Analysis
python# Analyze by NASS regions
regional_data = client.compare_by_region(
    year=2020,
    report='Farm Business Financial Ratios'
)

📁 Project Structure
farm-financial-platform/
│
├── api_client.py           # USDA API client
├── app.py                  # Main Flask application
├── wsgi.py                 # WSGI entry point
├── cli_app.py              # Command-line interface
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
│
├── templates/
│   └── index.html          # Main HTML template
│
├── static/
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── main.js         # Frontend JavaScript
│
│
└── README.md               # This file

🔧 Challenges & Solutions
Challenge 1: USDA API Data Format Requirements
Problem: The USDA API returned 400 errors with cryptic messages about JSON conversion failures.
Solution:

Discovered through detailed error logging that the API requires ALL parameters to be arrays/lists, not strings
Implemented automatic conversion of all parameters to lists before sending requests
Added parameter cleaning to remove None values from requests

Key Learning: Always thoroughly test API requirements with direct API calls before integrating into application code.
Challenge 2: Report Name Capitalization
Problem: API requests failed because report names were case-sensitive.
Solution:

Retrieved exact report names from the /report endpoint
Updated all report references to use proper capitalization
Created constants for report names to prevent future errors

Challenge 3: Load Balancer Configuration
Problem: Nginx default site was intercepting requests before reaching the application.
Solution:

Removed the default Nginx site
Configured application site as default_server
Implemented proper health check endpoints for load balancer monitoring

Challenge 4: Directory Structure Inconsistency
Problem: Different directory structures between Web01 and Web02 caused deployment issues.
Solution:

Standardized directory structure across all servers
Created deployment scripts to ensure consistency
Documented exact paths in systemd service files




Development Setup
bash# Clone your fork
git clone https://github.com/yourusername/farm-financial-platform.git

# Create development branch
git checkout -b develop

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

🙏 Credits
Data Sources
USDA Economic Research Service (ERS)

Website: https://www.ers.usda.gov/
API Documentation: https://www.ers.usda.gov/developer/data-apis/arms-data-api/
Data Source: Agricultural Resource Management Survey (ARMS)

The ARMS survey is the USDA's primary source of information on the financial condition, production practices, resource use, and economic well-being of America's farm households.
Technologies & Libraries

Flask: Web framework by Pallets Projects
Gunicorn: WSGI HTTP Server
Nginx: Web server and reverse proxy
Python: Programming language
API Management: api.data.gov

Acknowledgments

USDA Economic Research Service for providing comprehensive agricultural data
The open-source community for excellent tools and frameworks
Agricultural Extension Service for feedback and testing


📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including, without limitation, the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

📞 Contact & Support
Author: Gatete Derrick

GitHub: @nshderrick056
Email: d.gatete@alustudent.com

Project Link: https://github.com/nshderrick056/farm-financial-platform.git
📊 Project Status
Current Version: 1.0.0
Status: ✅ Production Ready
Last Updated: November 2024
Version History

v1.0.0 (November 2024)

Initial release
Full ARMS data integration
Load-balanced deployment
Five analysis modules
Interactive search and sort
Mobile-responsive design
