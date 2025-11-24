"""
USDA Economic Research Service ARMS API Client
Handles all API interactions with the ARMS database
"""

import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class USDAClient:
    """Client for interacting with USDA ERS ARMS API"""
    
    def __init__(self):
        self.api_key = os.getenv('USDA_API_KEY')
        self.base_url = 'https://api.ers.usda.gov/data/arms'
        
        if not self.api_key:
            raise ValueError("USDA_API_KEY not found in environment variables")
    
    def _make_request(self, endpoint, params=None, method='GET'):
        """Make HTTP request to USDA API"""
        url = f"{self.base_url}/{endpoint}"
        
        if params is None:
            params = {}
        
        try:
            if method == 'GET':
                # For GET, add api_key to URL params
                params['api_key'] = self.api_key
                response = requests.get(url, params=params, timeout=15)
            elif method == 'POST':
                # For POST, add api_key to URL and data in body
                url_with_key = f"{url}?api_key={self.api_key}"
                
                # CRITICAL: Remove None values from params
                clean_params = {k: v for k, v in params.items() if v is not None}
                
                # Debug logging (optional - remove in production)
                print(f"DEBUG: POST to {endpoint}")
                print(f"DEBUG: Body = {clean_params}")
                
                response = requests.post(url_with_key, json=clean_params, timeout=15)
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            # Get more detailed error info
            error_msg = f"API request failed: {str(e)}"
            try:
                error_detail = response.json()
                error_msg += f" - Details: {error_detail}"
            except:
                error_msg += f" - Response: {response.text[:300]}"
            return {'error': error_msg}
        except requests.exceptions.Timeout:
            return {'error': 'Request timed out. Please try again.'}
        except requests.exceptions.RequestException as e:
            return {'error': f'API request failed: {str(e)}'}
        except json.JSONDecodeError:
            return {'error': 'Invalid response from API'}
    
    def get_states(self):
        """Get all available states"""
        return self._make_request('state', method='GET')
    
    def get_years(self):
        """Get all available years"""
        return self._make_request('year', method='GET')
    
    def get_reports(self, report_name=None):
        """
        Get all available reports or specific report by name
        
        Args:
            report_name: Optional name of specific report
        """
        if report_name:
            params = {'name': report_name}
            return self._make_request('report', params, method='POST')
        return self._make_request('report', method='GET')
    
    def get_variables(self, report=None, name=None):
        """
        Get variables, optionally filtered by report or name
        
        Args:
            report: Report name to filter by
            name: Variable name to filter by
        """
        if report or name:
            params = {}
            if report:
                params['report'] = report
            if name:
                params['name'] = name
            return self._make_request('variable', params, method='POST')
        return self._make_request('variable', method='GET')
    
    def get_categories(self, category_name=None):
        """
        Get all categories or specific category by name
        
        Args:
            category_name: Optional name of specific category
        """
        if category_name:
            params = {'name': category_name}
            return self._make_request('category', params, method='POST')
        return self._make_request('category', method='GET')
    
    def get_farm_types(self, name=None):
        """
        Get all farm types or search by name
        
        Args:
            name: Optional farm type name to search
        """
        if name:
            params = {'name': name}
            return self._make_request('farmtype', params, method='POST')
        return self._make_request('farmtype', method='GET')
    
    def get_survey_data(self, years, state='all', report=None, variable=None,
                   farmtype=None, category=None, category_value=None, category2=None):
        """
        Get survey data with filters
        
        Args:
            years: List of years or single year (REQUIRED)
            state: State code or 'all' (default: 'all')
            report: Report name (e.g., 'income statement', 'balance sheet')
            variable: Variable ID (e.g., 'igcfi' for Gross Farm Income)
            farmtype: Farm type (e.g., 'operator households')
            category: Category name (e.g., 'NASS Regions')
            category_value: Category value filter
            category2: Second category for cross-tabulation
        
        Note: Either 'report' OR 'variable' is required
        """
        # Ensure years is a list
        if not isinstance(years, list):
            years = [years]
        
        # Validate years
        valid_years = [y for y in years if 1996 <= y <= 2023]
        if not valid_years:
            return {'error': 'Please select years between 1996 and 2023'}
        
        # Ensure state is a list
        if not isinstance(state, list):
            state = [state]

        params = {
            'year': valid_years,
            'state': state
        }

        # Add optional parameters only if they have values
        if report:
            if not isinstance(report, list):
                report = [report]
            params['report'] = report
        if variable:
            if not isinstance(variable, list):
                variable = [variable]
            params['variable'] = variable
        if farmtype:
            if not isinstance(farmtype, list):
                farmtype = [farmtype]
            params['farmtype'] = farmtype
        if category:
            if not isinstance(category, list):
                category = [category]
            params['category'] = category
        if category_value:
            params['category_value'] = category_value
        if category2:
            params['category2'] = category2
        
        # Validate required fields
        if not report and not variable:
            return {'error': 'Either report or variable parameter is required'}
        
        return self._make_request('surveydata', params, method='POST')
    
    def get_income_statement(self, years, state='all', farmtype=None, 
                        category=None, category_value=None):
        """Get farm business income statement data"""
        return self.get_survey_data(
            years=years,
            state=state,
            report='Farm Business Income Statement',  # CAPITALIZED!
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
    
    def get_balance_sheet(self, years, state='all', farmtype=None,
                     category=None, category_value=None):
        """Get farm business balance sheet data"""
        return self.get_survey_data(
            years=years,
            state=state,
            report='Farm Business Balance Sheet',  # CAPITALIZED!
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
    
    def get_financial_ratios(self, years, state='all', farmtype=None,
                        category=None, category_value=None):
        """Get farm business financial ratios"""
        return self.get_survey_data(
            years=years,
            state=state,
            report='Farm Business Financial Ratios',  # CAPITALIZED!
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
    
    def get_structural_characteristics(self, years, state='all', farmtype=None,
                                  category=None, category_value=None):
        """Get structural characteristics"""
        return self.get_survey_data(
            years=years,
            state=state,
            report='Structural Characteristics',  # CAPITALIZED!
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
    
    def get_government_payments(self, years, state='all', farmtype=None,
                           category=None, category_value=None):
        """Get government payments data"""
        return self.get_survey_data(
            years=years,
            state=state,
            report='Government Payments',  # CAPITALIZED!
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
    
    def get_operator_household_income(self, years, state='all', farmtype=None,
                                 category=None, category_value=None):
        """Get operator household income"""
        return self.get_survey_data(
            years=years,
            state=state,
            report='Operator Household Income',  # CAPITALIZED!
            farmtype=farmtype,
            category=category,
            category_value=category_value
        )
    
    def compare_by_farm_typology(self, year, report='Farm Business Income Statement'):
        """Compare data across different farm typologies"""
        return self.get_survey_data(
            years=[year],
            state='all',
            report=report,
            category='collapsed farm typology'
        )
    
    def compare_by_economic_class(self, year, report='Farm Business Income Statement'):
        """Compare data across different economic classes"""
        return self.get_survey_data(
            years=[year],
            state='all',
            report=report,
            category='economic class'
        )
    
    def compare_by_region(self, year, report='Farm Business Income Statement'):
        """Compare data across NASS regions"""
        return self.get_survey_data(
            years=[year],
            state='all',
            report=report,
            category='nass region'
        )
    
    def get_trend_analysis(self, start_year, end_year, variable, state='all'):
        """
        Get trend analysis for a specific variable across years
        
        Args:
            start_year: Starting year
            end_year: Ending year
            variable: Variable ID to analyze
            state: State or 'all'
        """
        years = list(range(start_year, end_year + 1))
        return self.get_survey_data(
            years=years,
            state=state,
            variable=variable
        )


# Test function
def test_client():
    """Test the API client with various endpoints"""
    try:
        client = USDAClient()
        print("=" * 60)
        print("USDA ARMS API Client Test")
        print("=" * 60)
        
        # Test 1: Get available years
        print("\n1. Testing get_years()...")
        years = client.get_years()
        if 'error' not in years:
            print(f"   ✓ Successfully retrieved years data")
            if 'data' in years:
                print(f"   Available years: {years['data']}")
        else:
            print(f"   ✗ Error: {years['error']}")
        
        # Test 2: Get states
        print("\n2. Testing get_states()...")
        states = client.get_states()
        if 'error' not in states:
            print(f"   ✓ Successfully retrieved states data")
        else:
            print(f"   ✗ Error: {states['error']}")
        
        # Test 3: Get reports
        print("\n3. Testing get_reports()...")
        reports = client.get_reports()
        if 'error' not in reports:
            print(f"   ✓ Successfully retrieved reports")
            if 'data' in reports:
                print(f"   Number of reports: {len(reports['data'])}")
        else:
            print(f"   ✗ Error: {reports['error']}")
        
        # Test 4: Get farm types
        print("\n4. Testing get_farm_types()...")
        farm_types = client.get_farm_types()
        if 'error' not in farm_types:
            print(f"   ✓ Successfully retrieved farm types")
            if 'data' in farm_types:
                print(f"   Number of farm types: {len(farm_types['data'])}")
        else:
            print(f"   ✗ Error: {farm_types['error']}")
        
        # Test 5: Get categories
        print("\n5. Testing get_categories()...")
        categories = client.get_categories()
        if 'error' not in categories:
            print(f"   ✓ Successfully retrieved categories")
        else:
            print(f"   ✗ Error: {categories['error']}")
        
        # Test 6: Get survey data (income statement)
        print("\n6. Testing get_income_statement()...")
        income_data = client.get_income_statement(years=[2020])
        if 'error' not in income_data:
            print(f"   ✓ Successfully retrieved income statement data")
            if 'data' in income_data:
                print(f"   Records returned: {len(income_data['data'])}")
        else:
            print(f"   ✗ Error: {income_data['error']}")
        
        print("\n" + "=" * 60)
        print("Test completed!")
        print("=" * 60)
        return True
    
    except Exception as e:
        print(f"\n✗ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    test_client()
