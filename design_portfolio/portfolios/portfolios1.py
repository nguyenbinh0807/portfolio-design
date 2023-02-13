import pandas as pd
import numpy as np

from scipy.optimize import minimize


def daily_returns(price_stock):
    returns = np.log(1+price_stock.pct_change()).dropna(how='all')
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    return returns, mean_returns, cov_matrix


def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(
        cov_matrix, weights))) * np.sqrt(252)
    return std, returns


def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_var, p_ret = portfolio_annualised_performance(
        weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var


def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]


def min_variance(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)

    return result


def display_ef_with_selected(table, mean_returns, cov_matrix):
    min_vol = min_variance(mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(
        min_vol.x, index=table.columns, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i*100, 2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    return min_vol_allocation
