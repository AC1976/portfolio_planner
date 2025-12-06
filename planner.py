import pandas as pd
from datetime import datetime

class Planner:
    def __init__(self,
                 start_equity: int = 2_000_000,
                 start_bonds: int = 1_100_000,
                 start_property: int = 1_800_000,
                 start_cash: int = 0,
                 equity_growth_rate: float = 0.065,
                 equity_dividend_yield: float = 0,
                 bond_coupon: float = 0.065,
                 property_net_yield: float = 0.088,
                 cash_rate: float = 0.0125,
                 box3_return_on_cash_current: float = 0.015,
                 box3_return_on_other_current: float = 0.06,
                 box3_rate_current: float = 0.36,
                 box3_exemption_current: int = 104000,
                 box3_rate_future: float = 0.36,
                 box3_exemption_future: int = 5000,
                 box3_new_start_year: int = 2028,
                 excess_cash_reinvestment_in_equity: float = 0,
                 inflation_rate: float = 0.0225,
                 planning_horizon_years: int = 10,
                 planning_start_year: int = 2026,
                 drawdown_per_year: int = 60000,
                 drawdown_start_year: int = 2028,                 
                 ) -> None:
    
        self.results = {}
        self.start_equity = start_equity
        self.start_bonds = start_bonds
        self.start_property = start_property
        self.start_cash = start_cash
        self.equity_growth_rate = equity_growth_rate
        self.equity_dividend_yield = equity_dividend_yield
        self.bond_coupon = bond_coupon
        self.property_net_yield = property_net_yield
        self.cash_rate = cash_rate
        self.box3_return_on_cash_current = box3_return_on_cash_current
        self.box3_return_on_other_current = box3_return_on_other_current
        self.box3_rate_current = box3_rate_current
        self.box3_exemption_current = box3_exemption_current
        self.box3_rate_future = box3_rate_future
        self.box3_exemption_future = box3_exemption_future
        self.box3_new_start_year = box3_new_start_year
        self.excess_cash_reinvestment_in_equity = excess_cash_reinvestment_in_equity
        self.inflation_rate = inflation_rate
        self.planning_horizon_years = planning_horizon_years
        self.planning_start_year = planning_start_year
        self.drawdown_per_year = drawdown_per_year
        self.drawdown_start_year = drawdown_start_year
        self.column_names = [
            "Year",
            "start_Equity",
            "start_Bonds",
            "start_Property",
            "start_Cash",
            "income_Equity_Growth",
            "income_Equity_Dividend",
            "income_Bonds_Coupon",
            "income_Rentals",
            "income_Interest_on_Cash",
            "box3_Old_or_New",
            "box3_Income",
            "box3_Tax",
            "cashflow_Equity_Dividend",
            "cashflow_Bonds_Coupon",
            "cashflow_Rentals",
            "cashflow_Interest_on_Cash",
            "cashflow_Drawdown",
            "cashflow_Box3_Tax",
            "cashflow_Total",
            "Total_Value"]
  
    def get_previous_year_value(self, current_year: datetime, column_name: str, default_value: float = 0.0) -> float:
        """Get value from previous year for a specific column using datetime."""
        previous_year = datetime(current_year.year - 1, 1, 1)
        
        if previous_year in self.results:
            return float(self.results[previous_year][column_name])
        else:
            return default_value
        
    def calculate_year(self, year: datetime) -> dict:
        """Calculate financial values for a given year."""
        year_result = {}
        year_result["Year"] = year.year

        # Logic for start_Equity field
        if year.year == self.planning_start_year:
            year_result["start_Equity"] = self.start_equity
        else:
            if self.get_previous_year_value(year, "cashflow_Total") > 0:
                reinvested_amount = self.excess_cash_reinvestment_in_equity * self.get_previous_year_value(year, "cashflow_Total")
            else:
                reinvested_amount = 0

            year_result["start_Equity"] = (
                self.get_previous_year_value(year, "start_Equity") +
                self.get_previous_year_value(year, "income_Equity_Growth") +
                reinvested_amount
            )
            
        # Logic for start_Bonds
        if year.year == self.planning_start_year:
            year_result["start_Bonds"] = self.start_bonds
        else:
            year_result["start_Bonds"] = self.get_previous_year_value(year, "start_Bonds")

        # Logic for start_Property
        if year.year == self.planning_start_year:
            year_result["start_Property"] = self.start_property
        else:
            year_result["start_Property"] = self.get_previous_year_value(year, "start_Property") 

        # Logic for start_Cash field
        if year.year == self.planning_start_year:
            year_result["start_Cash"] = self.start_cash
        else:
            if self.get_previous_year_value(year, "cashflow_Total") > 0:
                reinvested_amount = (1 - self.excess_cash_reinvestment_in_equity) * self.get_previous_year_value(year, "cashflow_Total")
            else:
                reinvested_amount = 0

            if self.get_previous_year_value(year, "cashflow_Total") < 0:
                cash_reducing_amount = self.get_previous_year_value(year, "cashflow_Total")
            else:
                cash_reducing_amount = 0

            year_result["start_Cash"] = (
                self.get_previous_year_value(year, "start_Cash") +
                reinvested_amount + 
                cash_reducing_amount
            )
        
        # Income calculations
        year_result["income_Equity_Growth"] = year_result["start_Equity"] * self.equity_growth_rate
        year_result["income_Equity_Dividend"] = year_result["start_Equity"] * self.equity_dividend_yield
        year_result["income_Bonds_Coupon"] = year_result["start_Bonds"] * self.bond_coupon
        year_result["income_Interest_on_Cash"] = year_result["start_Cash"] * self.cash_rate

        # Inflation adjusted rental
        if year.year == self.planning_start_year:
            year_result["income_Rentals"] = year_result["start_Property"] * self.property_net_yield
        else:
            year_result["income_Rentals"] = self.get_previous_year_value(year, "income_Rentals") * (1 + self.inflation_rate) 

        # Determine Box 3 income based on the year
        if year.year < self.box3_new_start_year: 
            year_result["box3_Old_or_New"] = "Old"
            year_result["box3_Income"] = ((
                year_result["start_Equity"] + 
                year_result["start_Bonds"] + 
                year_result["start_Property"] - 
                self.box3_exemption_current) * self.box3_return_on_other_current) + (
                    self.box3_return_on_cash_current * year_result["start_Cash"]
                )
            year_result["box3_Tax"] = max(0, (year_result["box3_Income"] * self.box3_rate_current))
        else:
            year_result["box3_Old_or_New"] = "New"
            year_result["box3_Income"] = (
                year_result["income_Equity_Growth"] + 
                year_result["income_Equity_Dividend"] + 
                year_result["income_Bonds_Coupon"] + 
                year_result["income_Rentals"] + 
                year_result["income_Interest_on_Cash"] - 
                self.box3_exemption_future)
            year_result["box3_Tax"] = max(0, (year_result["box3_Income"] * self.box3_rate_future))
        
        # Cashflow calculations
        year_result["cashflow_Equity_Dividend"] = year_result["income_Equity_Dividend"]
        year_result["cashflow_Bonds_Coupon"] = year_result["income_Bonds_Coupon"]
        year_result["cashflow_Rentals"] = year_result["income_Rentals"]
        year_result["cashflow_Interest_on_Cash"] = year_result["income_Interest_on_Cash"]           

        # Handle drawdown
        if year.year == self.drawdown_start_year:
            year_result["cashflow_Drawdown"] = self.drawdown_per_year
        elif year.year > self.drawdown_start_year:
            year_result["cashflow_Drawdown"] = self.get_previous_year_value(year, "cashflow_Drawdown") * (1 + self.inflation_rate)
        else:
            year_result['cashflow_Drawdown'] = 0 
         
        year_result["cashflow_Box3_Tax"] = year_result["box3_Tax"]          
        
        # Calculate total cash flow
        year_result["cashflow_Total"] = (year_result["cashflow_Equity_Dividend"] +
                                        year_result["cashflow_Bonds_Coupon"] +
                                        year_result["cashflow_Rentals"] +
                                        year_result["cashflow_Interest_on_Cash"] -
                                        year_result["cashflow_Drawdown"] -
                                        year_result["cashflow_Box3_Tax"])  
        
        # Calculate total value at the end of the year
        year_result["Total_Value"] = (year_result["start_Equity"] +
                                    year_result["start_Bonds"] +
                                    year_result["start_Property"] +
                                    year_result["start_Cash"] +
                                    year_result["income_Equity_Growth"] +
                                    year_result["income_Equity_Dividend"] +
                                    year_result["income_Bonds_Coupon"] +
                                    year_result["income_Rentals"] +
                                    year_result["income_Interest_on_Cash"] -
                                    year_result["cashflow_Box3_Tax"] -
                                    year_result["cashflow_Drawdown"])    
        
        self.results[year] = year_result
        return year_result

    def run_model(self):
        """Run the model for specified number of years starting from start_year."""
        for i in range(self.planning_horizon_years):
            year = datetime(self.planning_start_year + i, 1, 1)
            self.calculate_year(year)
        
        results_list = [self.results[datetime(self.planning_start_year + i, 1, 1)] for i in range(self.planning_horizon_years)]
        df = pd.DataFrame(results_list)
        return df

    def run_model_as_dict(self):
        """Run the model and return results as a list of dictionaries (JSON-serializable)."""
        df = self.run_model()
        return df.to_dict(orient='records')
