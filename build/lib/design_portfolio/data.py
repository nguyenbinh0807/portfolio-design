from vnstock import *
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from design_portfolio.portfolios import *


class DataLoad:
    def __init__(self, symbols, start, end):
        """ this is loader data

        Args:
            symbols (list type): list symbols
            start (date type): start tradingdate
            end (date type): end tranding date
        """
        self.symbols = symbols
        self.start = start
        self.end = end

    def download(self):
        """this is download price stock

        Returns:
            _type_: this is a dataframe price stock
        """
        price_stock = pd.DataFrame()
        price_close = []
        if type(self.symbols) is list:
            for symbol in self.symbols:
                price_close.append(stock_historical_data(symbol=symbol,  start_date=self.start,
                                   end_date=self.end).set_index('TradingDate').loc[:, 'Close'].rename(symbol))
            price_stock = pd.concat(price_close, axis=1)
            return price_stock
        else:
            return stock_historical_data(symbol=self.symbols,  start_date=self.start, end_date=self.end).set_index('TradingDate')

    def create_layout_button(self, price_stock, column):
        return dict(
            label=column, method='update',
            args=[{
                'visible': np.isin(price_stock.columns, column),
                'title': column,
                'showlegend': True
            }]
        )

    def lineplot(self, permanent=False):
        """this is a vizual pirce close

        Args:
            permanent (bool, optional): if True permanent start else . Defaults to False.
        """
        if permanent == True:
            price_stock = self.download()
            price_stock = price_stock*100/price_stock.iloc[0]
        elif permanent == False:
            price_stock = self.download()

        fig = go.Figure()
        for symbol in price_stock.columns:
            fig.add_trace(go.Scatter(
                x=price_stock.index,
                y=price_stock.loc[:, symbol],
                name=symbol,
                line=dict(
                    dash="solid",
                    width=2
                )
            ))

        symbol_dt = pd.DataFrame(price_stock.columns).rename(
            columns={0: 'symbol'})
        if type(self.symbols) is list:
            button_all = dict(
                label='All', method='update',
                args=[{
                    'visible': symbol_dt['symbol'].isin(symbol_dt['symbol']),
                    'title': 'All', 'showlegend': True
                }]
            )
            fig.update_layout(
                updatemenus=[go.layout.Updatemenu(
                    active=0,
                    buttons=([button_all]*True)+list(
                        symbol_dt['symbol'].map(lambda symbol: self.create_layout_button(
                            price_stock=price_stock, column=symbol))
                    )
                )
                ], title='Stock Price Close', xaxis_title="TradingDate",
                yaxis_title="Close")
        else:
            fig.update_layout(
                updatemenus=[go.layout.Updatemenu(
                    # active=0,
                    buttons=list(
                        symbol_dt['symbol'].map(lambda symbol: self.create_layout_button(
                            price_stock=price_stock, column=symbol))
                    )
                )
                ], title='Stock Price', xaxis_title="TradingDate",
                yaxis_title="Close")

        fig.update_xaxes(rangeslider_visible=False, rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ))
        fig.show()

    def properties(self, num_portfolios=6000, risk_free_rate=0.07, vizual=False):
        """this is a properties 

        Args:
            num_portfolios (int, optional): number portfolios. Defaults to 6000.
            risk_free_rate (float, optional): _description_. Defaults to 0.07.
            vizual (bool, optional): if True vizual camp. Defaults to False.

        Returns:
            _type_: weights, returns, vol
        """
        price_stock = self.download()
        if len(self.symbols) == 5:

            returns, mean_returns, cov_matrix = daily_returns(price_stock)
            new_data = display_ef_with_selected(
                table=price_stock, mean_returns=mean_returns, cov_matrix=cov_matrix)

            new_data = new_data.sort_values(
                by='allocation', ascending=True, axis=1)
            for column in new_data.columns:
                new_data.loc[new_data[column] >= int(30), column] = 0.3

            price_stock = price_stock.reindex(columns=new_data.columns)
            returns, mean_returns, cov_matrix = daily_returns(price_stock)
            new_data1 = display_simulated_ef_with_random(
                new_data, mean_returns, cov_matrix, num_portfolios, risk_free_rate)

            return display_simulated_ef_with_random_new_data1(table=new_data1, mean_returns=mean_returns, cov_matrix=cov_matrix, num_portfolios=num_portfolios, risk_free_rate=risk_free_rate, vizual=vizual)

        elif len(self.symbols) < 5:
            if type(self.symbols) is str:
                print('bạn chỉ nhập 1, Yêu cầu biến vào gồm 5 cổ phiếu')
            else:
                print('bạn chỉ nhập{}, Yêu cầu biến vào gồm 5 cổ phiếu'.format(
                    len(self.symbols)))
