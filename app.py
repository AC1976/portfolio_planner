from flask import Flask, render_template, request, jsonify
from planner import Planner

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API endpoint to run the financial model."""
    try:
        data = request.get_json()
        
        # Create planner with user-provided parameters
        planner = Planner(
            start_equity=int(data.get('start_equity', 2_000_000)),
            start_bonds=int(data.get('start_bonds', 1_100_000)),
            start_property=int(data.get('start_property', 1_800_000)),
            start_cash=int(data.get('start_cash', 0)),
            equity_growth_rate=float(data.get('equity_growth_rate', 0.065)),
            equity_dividend_yield=float(data.get('equity_dividend_yield', 0)),
            bond_coupon=float(data.get('bond_coupon', 0.065)),
            property_net_yield=float(data.get('property_net_yield', 0.088)),
            cash_rate=float(data.get('cash_rate', 0.0125)),
            box3_return_on_cash_current=float(data.get('box3_return_on_cash_current', 0.015)),
            box3_return_on_other_current=float(data.get('box3_return_on_other_current', 0.06)),
            box3_rate_current=float(data.get('box3_rate_current', 0.36)),
            box3_exemption_current=int(data.get('box3_exemption_current', 104000)),
            box3_rate_future=float(data.get('box3_rate_future', 0.36)),
            box3_exemption_future=int(data.get('box3_exemption_future', 5000)),
            box3_new_start_year=int(data.get('box3_new_start_year', 2028)),
            excess_cash_reinvestment_in_equity=float(data.get('excess_cash_reinvestment_in_equity', 0)),
            inflation_rate=float(data.get('inflation_rate', 0.0225)),
            planning_horizon_years=int(data.get('planning_horizon_years', 10)),
            planning_start_year=int(data.get('planning_start_year', 2026)),
            drawdown_per_year=int(data.get('drawdown_per_year', 60000)),
            drawdown_start_year=int(data.get('drawdown_start_year', 2028)),
        )
        
        results = planner.run_model_as_dict()
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
