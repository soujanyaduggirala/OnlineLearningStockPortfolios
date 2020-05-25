import pandas as pd
import numpy as np

class ConsolidatedModels:

    def __init__(self, vol='low', freq='daily', weight_init='equal'):
        self.data = pd.read_excel('{}vol_{}.xlsx'.format(vol, freq), index_col=0)
        self.open_prices = self.data.iloc[:, ::2]
        self.close_prices = self.data.iloc[:,1::2]

        self.tickers = list(set([x.split('_')[0] for x in self.data.columns]))
        self.caps = pd.read_csv('../training_data/marketcapdata.csv', index_col='Name').to_dict()['Market Cap']

        # Probabilities #
        initial_weights = self.init_weights(tickers=self.tickers, weight_init='marketcap')
        initial_weights /= sum(initial_weights)

        self.weights_rwma = initial_weights
        self.weights_mwu = initial_weights
        self.weights_hedge = initial_weights
        self.weights_expo = initial_weights

        # Total fees accrued from each alg
        self.fees_rmwa = 0
        self.fees_mwu = 0
        self.fees_hedge = 0
        self.fees_expo = 0

    def init_weights(self, tickers, weight_init='equal'):
        if weight_init is 'equal':
            w = np.ones(len(tickers))
            return w

        elif weight_init is 'marketcap':
            w = []

            for ticker in tickers:

                try:
                    w.append(self.caps[ticker])

                except:
                    w.append(0)

            return np.array(w)

        else:
            print('Invalid weight initialization method.')

    def rwma(self, timestep):
        open_now = self.open_prices.iloc[timestep].values
        close_now = self.close_prices.iloc[timestep].values

        # Calculate loss
        loss = ((close_now - open_now) < 0).astype('float64').fillna(0)


m = ConsolidatedModels()
for t in m.data.index:
    m.rwma(t)
    break