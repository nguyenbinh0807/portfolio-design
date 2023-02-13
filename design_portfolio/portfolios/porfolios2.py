import pandas as pd
import numpy as np


def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(
        cov_matrix, weights))) * np.sqrt(252)
    return std, returns


def sum_to_x(n, x):
    values = [0.0, x] + list(np.random.uniform(low=0.0, high=x, size=n-1))
    values.sort()
    return [values[i+1] - values[i] for i in range(n)]


def random_portfolios_new_data(new_data, num_portfolios, mean_returns, cov_matrix, risk_free_rate):

    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        if len(new_data.T.loc[new_data.T['allocation'] == 0.3, :].values) > 0:
            weights = np.hstack((
                sum_to_x(len(new_data.T.loc[new_data.T['allocation'] != 0.3, :]),
                         1-0.3*len(new_data.T.loc[new_data.T['allocation'] == 0.3, :])),
                np.array(
                    new_data.T.loc[new_data.T['allocation'] == 0.3, :].values[0])
            ))
        else:
            weights = np.array([1.0/len(mean_returns)
                               for i in range(len(mean_returns))])
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(
            weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record


def display_simulated_ef_with_random(table, mean_returns, cov_matrix, num_portfolios, risk_free_rate):

    results, weights = random_portfolios_new_data(
        table, num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    min_vol_idx = np.argmin(results[0])

    min_vol_allocation = pd.DataFrame(
        weights[min_vol_idx], index=table.columns, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i*100, 2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    return min_vol_allocation
