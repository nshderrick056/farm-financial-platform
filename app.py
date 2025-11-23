"""
Farm Financial Intelligence Platform
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify
from api_client import USDAClient
import json

app = Flask(__name__)
client = USDAClient()


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/years', methods=['GET'])
def get_years():
    """Get all available years"""
    try:
        years = client.get_years()
        return jsonify(years)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/states', methods=['GET'])
def get_states():
    """Get all available states"""
    try:
        states = client.get_states()
        return jsonify(states)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all available reports"""
    try:
        reports = client.get_reports()
        return jsonify(reports)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/farm-types', methods=['GET'])
def get_farm_types():
    """Get all farm types"""
    try:
        farm_types = client.get_farm_types()
        return jsonify(farm_types)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = client.get_categories()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/variables', methods=['GET'])
def get_variables():
    """Get variables, optionally filtered by report"""
    try:
        report = request.args.get('report')
        variables = client.get_variables(report=report)
        return jsonify(variables)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/income-statement', methods=['POST'])
def get_income_statement():
    """Get income statement data"""
    try:
        data = request.json
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        farmtype = data.get('farmtype')
        category = data.get('category')
        category_value = data.get('category_value')
        
        result = client.get_income_statement(
            years=years,
            state=state,
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/balance-sheet', methods=['POST'])
def get_balance_sheet():
    """Get balance sheet data"""
    try:
        data = request.json
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        farmtype = data.get('farmtype')
        category = data.get('category')
        category_value = data.get('category_value')
        
        result = client.get_balance_sheet(
            years=years,
            state=state,
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/financial-ratios', methods=['POST'])
def get_financial_ratios():
    """Get financial ratios"""
    try:
        data = request.json
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        farmtype = data.get('farmtype')
        category = data.get('category')
        category_value = data.get('category_value')
        
        result = client.get_financial_ratios(
            years=years,
            state=state,
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/structural-characteristics', methods=['POST'])
def get_structural_characteristics():
    """Get structural characteristics"""
    try:
        data = request.json
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        farmtype = data.get('farmtype')
        category = data.get('category')
        
        result = client.get_structural_characteristics(
            years=years,
            state=state,
            farmtype=farmtype,
            category=category
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/government-payments', methods=['POST'])
def get_government_payments():
    """Get government payments data"""
    try:
        data = request.json
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        farmtype = data.get('farmtype')
        category = data.get('category')
        
        result = client.get_government_payments(
            years=years,
            state=state,
            farmtype=farmtype,
            category=category
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/operator-household-income', methods=['POST'])
def get_operator_household_income():
    """Get operator household income"""
    try:
        data = request.json
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        farmtype = data.get('farmtype')
        category = data.get('category')
        
        result = client.get_operator_household_income(
            years=years,
            state=state,
            farmtype=farmtype,
            category=category
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare-farm-typology', methods=['POST'])
def compare_farm_typology():
    """Compare different farm typologies"""
    try:
        data = request.json
        year = data.get('year', 2020)
        report = data.get('report', 'Farm business income statement')
        
        result = client.compare_by_farm_typology(year, report)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare-economic-class', methods=['POST'])
def compare_economic_class():
    """Compare different economic classes"""
    try:
        data = request.json
        year = data.get('year', 2020)
        report = data.get('report', 'Farm business income statement')
        
        result = client.compare_by_economic_class(year, report)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare-regions', methods=['POST'])
def compare_regions():
    """Compare different NASS regions"""
    try:
        data = request.json
        year = data.get('year', 2020)
        report = data.get('report', 'Farm business income statement')
        
        result = client.compare_by_region(year, report)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trend-analysis', methods=['POST'])
def get_trend_analysis():
    """Get trend analysis for a variable"""
    try:
        data = request.json
        start_year = data.get('start_year', 2015)
        end_year = data.get('end_year', 2020)
        variable = data.get('variable')
        state = data.get('state', 'all')
        
        if not variable:
            return jsonify({'error': 'Variable is required'}), 400
        
        result = client.get_trend_analysis(start_year, end_year, variable, state)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/custom-query', methods=['POST'])
def custom_query():
    """Custom query with all available filters"""
    try:
        data = request.json
        
        # Extract all possible parameters
        years = data.get('years', [2020])
        state = data.get('state', 'all')
        report = data.get('report')
        variable = data.get('variable')
        farmtype = data.get('farmtype')
        category = data.get('category')
        category_value = data.get('category_value')
        category2 = data.get('category2')
        
        # Validate required fields
        if not report and not variable:
            return jsonify({'error': 'Either report or variable is required'}), 400
        
        result = client.get_survey_data(
            years=years,
            state=state,
            report=report,
            variable=variable,
            farmtype=farmtype,
            category=category,
            category_value=category_value,
            category2=category2
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancer"""
    return jsonify({
        'status': 'healthy',
        'service': 'farm-financial-platform',
        'version': '1.0.0'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # For local development
    print("=" * 60)
    print("Farm Financial Intelligence Platform")
    print("=" * 60)
    print("Server starting on http://0.0.0.0:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
