from api_client import USDAClient

client = USDAClient()

print("Testing API connectivity...")
print("=" * 60)

# Test 1: Get available years
print("\n1. Getting available years...")
years_data = client.get_years()
print(f"Response: {years_data}")

# Test 2: Get available reports
print("\n2. Getting available reports...")
reports_data = client.get_reports()
if 'data' in reports_data:
    print(f"Found {len(reports_data['data'])} reports:")
    for report in reports_data['data']:
        print(f"  - {report}")
else:
    print(f"Response: {reports_data}")

# Test 3: Try a simple survey data request
print("\n3. Testing survey data request...")
test_data = client.get_survey_data(
    years=[2020],
    state='all',
    report='income statement'
)
print(f"Response: {test_data}")
