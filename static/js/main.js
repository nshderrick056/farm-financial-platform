// Farm Financial Intelligence Platform - Frontend JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    loadYears();
    loadStates();
});

// Tab functionality
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            openTab(tabName, this);
        });
    });
}

function openTab(tabName, buttonElement) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    buttonElement.classList.add('active');
}

// Load available years
async function loadYears() {
    try {
        const response = await fetch('/api/years');
        const data = await response.json();
        
        if (data.data) {
            const years = data.data.sort((a, b) => b - a); // Most recent first
            const selects = ['income-years', 'balance-years', 'ratios-years', 'structure-years', 'compare-year'];
            
            selects.forEach(selectId => {
                const select = document.getElementById(selectId);
                years.forEach(year => {
                    const option = document.createElement('option');
                    option.value = year;
                    option.textContent = year;
                    select.appendChild(option);
                });
            });
        }
    } catch (error) {
        console.error('Error loading years:', error);
    }
}

// Load available states
async function loadStates() {
    try {
        const response = await fetch('/api/states');
        const data = await response.json();
        
        if (data.data) {
            const states = data.data;
            const selects = ['income-state', 'balance-state', 'ratios-state', 'structure-state'];
            
            selects.forEach(selectId => {
                const select = document.getElementById(selectId);
                states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state.id || state.name;
                    option.textContent = state.name;
                    select.appendChild(option);
                });
            });
        }
    } catch (error) {
        console.error('Error loading states:', error);
    }
}

// Fetch Income Statement
async function fetchIncomeStatement() {
    const yearsSelect = document.getElementById('income-years');
    const selectedYears = Array.from(yearsSelect.selectedOptions).map(o => parseInt(o.value));
    const state = document.getElementById('income-state').value;
    const category = document.getElementById('income-category').value;
    
    if (selectedYears.length === 0) {
        showError('income', 'Please select at least one year');
        return;
    }
    
    showLoading('income', true);
    hideError('income');
    
    try {
        const response = await fetch('/api/income-statement', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                years: selectedYears,
                state: state,
                category: category || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('income', data.error);
        } else if (data.data && data.data.length > 0) {
            displayTableData('income', data);
        } else {
            showError('income', 'No data available for the selected criteria. Try different filters.');
        }
    } catch (error) {
        showError('income', 'Failed to fetch data: ' + error.message);
    } finally {
        showLoading('income', false);
    }
}

// Fetch Balance Sheet
async function fetchBalanceSheet() {
    const yearsSelect = document.getElementById('balance-years');
    const selectedYears = Array.from(yearsSelect.selectedOptions).map(o => parseInt(o.value));
    const state = document.getElementById('balance-state').value;
    const category = document.getElementById('balance-category').value;
    
    if (selectedYears.length === 0) {
        showError('balance', 'Please select at least one year');
        return;
    }
    
    showLoading('balance', true);
    hideError('balance');
    
    try {
        const response = await fetch('/api/balance-sheet', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                years: selectedYears,
                state: state,
                category: category || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('balance', data.error);
        } else if (data.data && data.data.length > 0) {
            displayTableData('balance', data);
        } else {
            showError('balance', 'No data available for the selected criteria.');
        }
    } catch (error) {
        showError('balance', 'Failed to fetch data: ' + error.message);
    } finally {
        showLoading('balance', false);
    }
}

// Fetch Financial Ratios
async function fetchFinancialRatios() {
    const yearsSelect = document.getElementById('ratios-years');
    const selectedYears = Array.from(yearsSelect.selectedOptions).map(o => parseInt(o.value));
    const state = document.getElementById('ratios-state').value;
    const category = document.getElementById('ratios-category').value;
    
    if (selectedYears.length === 0) {
        showError('ratios', 'Please select at least one year');
        return;
    }
    
    showLoading('ratios', true);
    hideError('ratios');
    
    try {
        const response = await fetch('/api/financial-ratios', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                years: selectedYears,
                state: state,
                category: category || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('ratios', data.error);
        } else if (data.data && data.data.length > 0) {
            displayTableData('ratios', data);
        } else {
            showError('ratios', 'No data available for the selected criteria.');
        }
    } catch (error) {
        showError('ratios', 'Failed to fetch data: ' + error.message);
    } finally {
        showLoading('ratios', false);
    }
}

// Fetch Structural Characteristics
async function fetchStructuralCharacteristics() {
    const yearsSelect = document.getElementById('structure-years');
    const selectedYears = Array.from(yearsSelect.selectedOptions).map(o => parseInt(o.value));
    const state = document.getElementById('structure-state').value;
    const category = document.getElementById('structure-category').value;
    
    if (selectedYears.length === 0) {
        showError('structure', 'Please select at least one year');
        return;
    }
    
    showLoading('structure', true);
    hideError('structure');
    
    try {
        const response = await fetch('/api/structural-characteristics', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                years: selectedYears,
                state: state,
                category: category || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('structure', data.error);
        } else if (data.data && data.data.length > 0) {
            displayTableData('structure', data);
        } else {
            showError('structure', 'No data available for the selected criteria.');
        }
    } catch (error) {
        showError('structure', 'Failed to fetch data: ' + error.message);
    } finally {
        showLoading('structure', false);
    }
}

// Perform Comparison
async function performComparison() {
    const year = parseInt(document.getElementById('compare-year').value);
    const report = document.getElementById('compare-report').value;
    const compareType = document.getElementById('compare-type').value;
    
    if (!year) {
        showError('compare', 'Please select a year');
        return;
    }
    
    showLoading('compare', true);
    hideError('compare');
    
    let endpoint;
    switch(compareType) {
        case 'typology':
            endpoint = '/api/compare-farm-typology';
            break;
        case 'economic':
            endpoint = '/api/compare-economic-class';
            break;
        case 'region':
            endpoint = '/api/compare-regions';
            break;
        default:
            endpoint = '/api/compare-farm-typology';
    }
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ year, report })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('compare', data.error);
        } else if (data.data && data.data.length > 0) {
            displayTableData('compare', data);
        } else {
            showError('compare', 'No comparison data available for the selected criteria.');
        }
    } catch (error) {
        showError('compare', 'Failed to fetch data: ' + error.message);
    } finally {
        showLoading('compare', false);
    }
}

// Display table data
function displayTableData(section, data) {
    const thead = document.getElementById(`${section}-thead`);
    const tbody = document.getElementById(`${section}-tbody`);
    
    thead.innerHTML = '';
    tbody.innerHTML = '';
    
    if (!data.data || data.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">No data available</td></tr>';
        return;
    }
    
    // Create header
    const headerRow = document.createElement('tr');
    const keys = Object.keys(data.data[0]);
    
    keys.forEach((key, index) => {
        const th = document.createElement('th');
        th.textContent = formatColumnName(key);
        th.onclick = () => sortTable(`${section}-table`, index);
        th.style.cursor = 'pointer';
        th.title = 'Click to sort';
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    
    // Create rows
    data.data.forEach(row => {
        const tr = document.createElement('tr');
        keys.forEach(key => {
            const td = document.createElement('td');
            td.textContent = formatValue(row[key]);
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    
    document.getElementById(`${section}-results`).style.display = 'block';
    
    // Show summary if available
    if (section === 'income' && data.data.length > 0) {
        showSummary(section, data.data);
    }
}

// Show data summary
function showSummary(section, data) {
    const summaryDiv = document.getElementById(`${section}-summary`);
    if (!summaryDiv) return;
    
    summaryDiv.innerHTML = `
        <h4>Summary Statistics</h4>
        <div class="summary-grid">
            <div class="summary-item">
                <span class="summary-label">Total Records:</span>
                <span class="summary-value">${data.length}</span>
            </div>
        </div>
    `;
}

// Format column names
function formatColumnName(name) {
    return name
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Format values for display
function formatValue(value) {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'number') {
        // Format numbers with commas
        return value.toLocaleString('en-US', {maximumFractionDigits: 2});
    }
    return value;
}

// Search functionality
function searchTable(tableId, searchId) {
    const input = document.getElementById(searchId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {
        let found = false;
        const td = tr[i].getElementsByTagName('td');
        
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        tr[i].style.display = found ? '' : 'none';
    }
}

// Sort table
function sortTable(tableId, column) {
    const table = document.getElementById(tableId);
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    
    if (rows.length === 0) return;
    
    // Check if column contains numbers
    const firstValue = rows[0].getElementsByTagName('td')[column].textContent.replace(/,/g, '');
    const isNumeric = !isNaN(parseFloat(firstValue)) && isFinite(firstValue);
    
    // Determine sort direction
    const currentDirection = table.dataset[`sortDir${column}`] || 'asc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    table.dataset[`sortDir${column}`] = newDirection;
    
    rows.sort((a, b) => {
        const aVal = a.getElementsByTagName('td')[column].textContent;
        const bVal = b.getElementsByTagName('td')[column].textContent;
        
        if (isNumeric) {
            const aNum = parseFloat(aVal.replace(/,/g, '')) || 0;
            const bNum = parseFloat(bVal.replace(/,/g, '')) || 0;
            return newDirection === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        const comparison = aVal.localeCompare(bVal);
        return newDirection === 'asc' ? comparison : -comparison;
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Helper functions
function showLoading(section, show) {
    const loading = document.getElementById(`${section}-loading`);
    if (loading) {
        loading.classList.toggle('hidden', !show);
    }
}

function showError(section, message) {
    const error = document.getElementById(`${section}-error`);
    if (error) {
        error.textContent = message;
        error.classList.remove('hidden');
    }
}

function hideError(section) {
    const error = document.getElementById(`${section}-error`);
    if (error) {
        error.classList.add('hidden');
    }
}
