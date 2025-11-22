"""
Farm Financial Intelligence Platform - CLI Version
Command-line interface for analyzing USDA ARMS data
"""

from api_client import USDAClient
import sys
from tabulate import tabulate


class FarmCLI:
    def __init__(self):
        self.client = USDAClient()
        self.running = True
    
    def print_header(self):
        print("\n" + "=" * 70)
        print(" " * 10 + "🌾 FARM FINANCIAL INTELLIGENCE PLATFORM 🌾")
        print(" " * 15 + "USDA ARMS Data Analysis Tool")
        print("=" * 70 + "\n")
    
    def print_menu(self):
        print("\n" + "-" * 70)
        print("MAIN MENU")
        print("-" * 70)
        print("1. View Farm Income Statement")
        print("2. View Farm Balance Sheet")
        print("3. View Financial Ratios")
        print("4. Compare Farm Types")
        print("5. View Structural Characteristics")
        print("6. Available Years and States")
        print("7. Exit")
        print("-" * 70)
    
    def get_years_input(self):
        """Get year selection from user"""
        print("\nEnter years (comma-separated, e.g., 2020,2019):")
        years_input = input("> ").strip()
        try:
            years = [int(y.strip()) for y in years_input.split(',')]
            return years
        except ValueError:
            print("❌ Invalid year format. Using 2020 as default.")
            return [2020]
    
    def get_state_input(self):
        """Get state selection from user"""
        print("\nEnter state code (or 'all' for all states):")
        state = input("> ").strip() or 'all'
        return state
    
    def get_category_input(self):
        """Get category selection from user"""
        print("\nSelect category (optional, press Enter to skip):")
        print("  1. Farm Typology")
        print("  2. Economic Class")
        print("  3. NASS Region")
        print("  4. Operator Age")
        print("  5. None")
        
        choice = input("> ").strip()
        
        categories = {
            '1': 'collapsed farm typology',
            '2': 'economic class',
            '3': 'nass region',
            '4': 'operator age',
            '5': None
        }
        
        return categories.get(choice, None)
    
    def display_table(self, data, title="Results"):
        """Display data in table format"""
        if not data or 'data' not in data or len(data['data']) == 0:
            print("\n❌ No data available for the selected criteria.\n")
            return
        
        print("\n" + "=" * 70)
        print(f" {title}")
        print("=" * 70)
        
        # Get headers and rows
        headers = list(data['data'][0].keys())
        rows = []
        
        for item in data['data']:
            row = [self.format_value(item.get(h)) for h in headers]
            rows.append(row)
        
        # Display table
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        print(f"\nTotal Records: {len(data['data'])}")
        print("=" * 70 + "\n")
    
    def format_value(self, value):
        """Format value for display"""
        if value is None:
            return 'N/A'
        if isinstance(value, (int, float)):
            return f"{value:,.2f}"
        return str(value)
    
    def option_income_statement(self):
        """Handle income statement option"""
        print("\n" + "=" * 70)
        print("FARM BUSINESS INCOME STATEMENT")
        print("=" * 70)
        
        years = self.get_years_input()
        state = self.get_state_input()
        category = self.get_category_input()
        
        print("\n⏳ Fetching data from USDA...")
        
        data = self.client.get_income_statement(
            years=years,
            state=state,
            category=category
        )
        
        if 'error' in data:
            print(f"\n❌ Error: {data['error']}\n")
        else:
            self.display_table(data, f"Income Statement - {', '.join(map(str, years))}")
    
    def option_balance_sheet(self):
        """Handle balance sheet option"""
        print("\n" + "=" * 70)
        print("FARM BUSINESS BALANCE SHEET")
        print("=" * 70)
        
        years = self.get_years_input()
        state = self.get_state_input()
        category = self.get_category_input()
        
        print("\n⏳ Fetching data from USDA...")
        
        data = self.client.get_balance_sheet(
            years=years,
            state=state,
            category=category
        )
        
        if 'error' in data:
            print(f"\n❌ Error: {data['error']}\n")
        else:
            self.display_table(data, f"Balance Sheet - {', '.join(map(str, years))}")
    
    def option_financial_ratios(self):
        """Handle financial ratios option"""
        print("\n" + "=" * 70)
        print("FARM BUSINESS FINANCIAL RATIOS")
        print("=" * 70)
        
        years = self.get_years_input()
        state = self.get_state_input()
        category = self.get_category_input()
        
        print("\n⏳ Fetching data from USDA...")
        
        data = self.client.get_financial_ratios(
            years=years,
            state=state,
            category=category
        )
        
        if 'error' in data:
            print(f"\n❌ Error: {data['error']}\n")
        else:
            self.display_table(data, f"Financial Ratios - {', '.join(map(str, years))}")
    
    def option_compare_farms(self):
        """Handle farm comparison option"""
        print("\n" + "=" * 70)
        print("COMPARE FARM TYPES")
        print("=" * 70)
        
        print("\nEnter year:")
        year_input = input("> ").strip()
        try:
            year = int(year_input)
        except ValueError:
            print("❌ Invalid year. Using 2020.")
            year = 2020
        
        print("\nSelect comparison type:")
        print("  1. Farm Typology")
        print("  2. Economic Class")
        print("  3. NASS Region")
        
        choice = input("> ").strip()
        
        print("\n⏳ Fetching comparison data...")
        
        if choice == '1':
            data = self.client.compare_by_farm_typology(year)
            title = f"Comparison by Farm Typology - {year}"
        elif choice == '2':
            data = self.client.compare_by_economic_class(year)
            title = f"Comparison by Economic Class - {year}"
        elif choice == '3':
            data = self.client.compare_by_region(year)
            title = f"Comparison by NASS Region - {year}"
        else:
            print("❌ Invalid choice.")
            return
        
        if 'error' in data:
            print(f"\n❌ Error: {data['error']}\n")
        else:
            self.display_table(data, title)
    
    def option_structural_characteristics(self):
        """Handle structural characteristics option"""
        print("\n" + "=" * 70)
        print("FARM STRUCTURAL CHARACTERISTICS")
        print("=" * 70)
        
        years = self.get_years_input()
        state = self.get_state_input()
        
        print("\n⏳ Fetching data from USDA...")
        
        data = self.client.get_structural_characteristics(
            years=years,
            state=state
        )
        
        if 'error' in data:
            print(f"\n❌ Error: {data['error']}\n")
        else:
            self.display_table(data, f"Structural Characteristics - {', '.join(map(str, years))}")
    
    def option_view_metadata(self):
        """View available years and states"""
        print("\n" + "=" * 70)
        print("AVAILABLE DATA")
        print("=" * 70)
        
        print("\n⏳ Fetching metadata...")
        
        # Get years
        years_data = self.client.get_years()
        if 'data' in years_data:
            print("\n📅 Available Years:")
            print("  " + ", ".join(map(str, sorted(years_data['data'], reverse=True))))
        
        # Get states
        states_data = self.client.get_states()
        if 'data' in states_data:
            print("\n🗺️  Available States:")
            for state in states_data['data'][:10]:  # Show first 10
                name = state.get('name', 'Unknown')
                print(f"  - {name}")
            if len(states_data['data']) > 10:
                print(f"  ... and {len(states_data['data']) - 10} more")
        
        print("\n" + "=" * 70)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main CLI loop"""
        self.print_header()
        
        while self.running:
            self.print_menu()
            choice = input("Select an option (1-7): ").strip()
            
            if choice == '1':
                self.option_income_statement()
            elif choice == '2':
                self.option_balance_sheet()
            elif choice == '3':
                self.option_financial_ratios()
            elif choice == '4':
                self.option_compare_farms()
            elif choice == '5':
                self.option_structural_characteristics()
            elif choice == '6':
                self.option_view_metadata()
            elif choice == '7':
                print("\n👋 Thank you for using Farm Financial Intelligence Platform!")
                print("Data provided by USDA Economic Research Service\n")
                self.running = False
            else:
                print("\n❌ Invalid option. Please choose 1-7.\n")
            
            if self.running and choice in ['1', '2', '3', '4', '5']:
                input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    try:
        cli = FarmCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
