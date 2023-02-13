import pandas as pd
import numpy as np
import plotly.graph_objs as go


def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(
        cov_matrix, weights))) * np.sqrt(252)
    return std, returns


def sum_to_x(n, x):
    values = [0.0, x] + list(np.random.uniform(low=0, high=x, size=n-1))
    values.sort()
    return [values[i+1] - values[i] for i in range(n)]


def random_portfolios_new_data1(new_data1, num_portfolios, mean_returns, cov_matrix, risk_free_rate):

    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.hstack((
            sum_to_x(2, 1-(new_data1.values[0, 4]/100+round(
                new_data1.values[0, 3], 0)/100+round(new_data1.values[0, 2], 0)/100)),
            round(new_data1.values[0, 2], 0)/100,
            round(new_data1.values[0, 3], 0)/100,
            round(new_data1.values[0, 4], 0)/100
        ))
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(
            weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record

def converse_properties_to_frame(data):
    lines=data.strip().split('\n')
    header=lines[0]
    annualised_return = float(lines[1].split(':')[1].strip())
    annualised_volatility = float(lines[2].split(':')[1].strip())
    columns=lines[3].strip().split()
    values=[float(x) for x in lines[4].strip().split()[1:]]
    df = pd.DataFrame({columns[i]: [values[i]] for i in range(len(columns))})
    df['Annualised Return'] = annualised_return
    df['Annualised Volatility'] = annualised_volatility
    df.index = [header.split()[0]+header.split()[1]]
    return df

def display_simulated_ef_with_random_new_data1(table, mean_returns, cov_matrix, num_portfolios, risk_free_rate, vizual):

    results, weights = random_portfolios_new_data1(
        table, num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(
        weights[max_sharpe_idx], index=table.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [
        round(i*100, 2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
    min_vol_allocation = pd.DataFrame(
        weights[min_vol_idx], index=table.columns, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i*100, 2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    if vizual == True:
        print("-"*80)
        print("Maximum Sharpe Ratio Portfolio Allocation\n")
        print("Annualised Return:", round(rp, 2))
        print("Annualised Volatility:", round(sdp, 2))
        print("\n")
        print(max_sharpe_allocation)
        print("-"*80)
        print("Minimum Volatility Portfolio Allocation\n")
        print("Annualised Return:", round(rp_min, 2))
        print("Annualised Volatility:", round(sdp_min, 2))
        print("\n")
        print(min_vol_allocation)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=results[0, :], y=results[1, :], mode='markers', marker_color=results[2, :], name='Portfolio'
        ))
        fig.add_trace(go.Scatter(
            x=np.array(sdp), y=np.array(rp), mode='markers+text', text='Maximum Sharpe ratio', name='Maximum Sharpe ratio',
            textposition='top center',
            marker=dict(size=18, symbol="star")
        ))
        fig.add_trace(go.Scatter(
            x=np.array(sdp_min), y=np.array(rp_min), mode='markers+text', text='Minimum volatility', name='Minimum volatility',
            textposition='top center',
            marker=dict(size=18, symbol="star")
        ))
        fig.update_layout(
            title='Simulated Portfolio Optimization based on Efficient Frontier',
            xaxis_title='annualised volatility',
            yaxis_title='annualised returns'
        )
        fig.show()
    elif vizual == False:
        
        max_sharpe_value = "Maximum Sharpe Ratio Portfolio Allocation\n" + \
            f"Annualised Return: { round(rp, 2)} \n" + \
            f"Annualised Volatility:  {round(sdp, 2)} \n"+ \
                f"{max_sharpe_allocation}"
        max_sharpe_data=converse_properties_to_frame(max_sharpe_value)

        min_vol_value="Minimum Volatility Portfolio Allocation\n" + \
            f"Annualised Return: {round(rp_min, 2)} \n"+\
            f"Annualised Volatility:  {round(sdp_min, 2)} \n" + \
            f"{min_vol_allocation}"
        min_vol_data=converse_properties_to_frame(min_vol_value)
        
        results_data=pd.DataFrame(columns=max_sharpe_data.columns)
        results_data=pd.concat([
            max_sharpe_data, min_vol_data
        ], axis=0)    
        return results_data
