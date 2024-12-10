import json
from financial_plots import FinancialPlotter

# Load data
with open('src/sample_data.json', 'r') as f:
    data = json.load(f)

# Create plotter instance
plotter = FinancialPlotter()

# Create all plots
market_plot = plotter.create_market_plot(data['market_data'])
income_plot = plotter.create_income_statement_plot(data['income_statement'])
revenue_plot = plotter.create_revenue_breakdown_plot(data['revenue_breakdown'])
metrics_plot = plotter.create_metrics_plot(data['metrics'])

# Show plots
market_plot.show()
income_plot.show()
revenue_plot.show()
metrics_plot.show() 