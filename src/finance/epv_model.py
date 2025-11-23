# src/finance/epv_model.py

class GreenwaldEPV:
    def calculate_reproduction_value(self, balance_sheet):
        """
        Estimate replacement cost of operating assets (simplified):
        - Excludes cash to avoid cash double-count when computing franchise value.
        - Uses invested-capital style proxy: working capital + PPE + capitalized current R&D (3-year).
        - If book equity is missing, falls back to net operating assets proxy (excluding cash).
        """
        cash = balance_sheet.get('cash', 0)
        accounts_receivable = balance_sheet.get('accounts_receivable', 0)
        pp_and_e = balance_sheet.get('pp_and_e', 0)
        other_assets = balance_sheet.get('other_assets', 0)
        total_current_liabilities = balance_sheet.get('total_current_liabilities', 0)

        # Net operating working capital (excluding cash)
        net_working_capital = (accounts_receivable + other_assets) - total_current_liabilities

        # Capitalize current R&D as a proxy for product/platform replacement
        rnd = balance_sheet.get('rnd', 0)
        capitalized_rnd = rnd * 3

        # Invested capital proxy (ex-cash)
        reproduction_value = net_working_capital + pp_and_e + capitalized_rnd

        # If book equity is available and higher, use it as a floor but still exclude cash double count
        book_equity = balance_sheet.get('book_value_equity')
        if book_equity not in (None, 0):
            reproduction_value = max(reproduction_value, book_equity - cash)

        # Do not allow negative reproduction values
        return max(reproduction_value, 0)

    def calculate_normalized_earnings(self, income_stmt, ai_adjustments):
        """
        Step 2: Calculate Distributable Cash Flow.
        
        Args:
            income_stmt (dict): Contains 'ebit', 'sga', 'rnd', 'tax_rate'
            ai_adjustments (dict): Contains 'maintenance_sga_percent', 'maintenance_rnd_percent'
            
        Returns:
            dict: Detailed breakdown of normalized earnings
        """
        reported_ebit = income_stmt.get('ebit', 0)
        sga = income_stmt.get('sga', 0)
        rnd = income_stmt.get('rnd', 0)
        tax_rate = income_stmt.get('tax_rate', 0.21)
        
        # Get AI Maintenance Estimates
        maint_sga_pct = ai_adjustments.get('maintenance_sga_percent', 1.0)
        maint_rnd_pct = ai_adjustments.get('maintenance_rnd_percent', 1.0)
        
        # Calculate Growth Spend (to be added back)
        # Growth % = 1 - Maintenance %
        growth_sga = sga * (1 - maint_sga_pct)
        growth_rnd = rnd * (1 - maint_rnd_pct)
        total_growth_capex = growth_sga + growth_rnd
        
        # Normalized EBIT = Reported EBIT + Growth Investments
        normalized_ebit = reported_ebit + total_growth_capex
        
        # NOPAT (Net Operating Profit After Tax)
        nopat = normalized_ebit * (1 - tax_rate)
        
        return {
            "normalized_ebit": normalized_ebit,
            "nopat": nopat,
            "growth_sga": growth_sga,
            "growth_rnd": growth_rnd,
            "reported_ebit": reported_ebit
        }

    def get_epv(self, normalized_earnings, cost_of_capital):
        """
        Step 3: EPV = Normalized Earnings / WACC
        Note: Assumes ZERO growth. This is the 'No-Growth' value.
        """
        if cost_of_capital == 0:
            return 0
        return normalized_earnings / cost_of_capital

    def calculate_equity_value(self, firm_epv, cash, debt):
        """
        Step 4: Equity Value = Firm EPV + Cash - Debt
        """
        return firm_epv + cash - debt

    def calculate_rule_of_40(self, revenue_growth_pct, profit_margin_pct):
        """
        Standard Rule of 40 calculation.
        """
        return revenue_growth_pct + profit_margin_pct
