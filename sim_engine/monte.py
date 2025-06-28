import numpy as np
import payoffs as pf

import matplotlib.pyplot as plt
import seaborn as sns



class MonteCarloEngine:
    def __init__(self, S0, r, sigma, T, N, M):
        self.S0 = S0
        self.r = r
        self.sigma = sigma
        self.T = T
        self.N = N
        self.M = M
        self.dt = T / N
        self.paths = None
        self.payoff_fn = None
    
    def simulate_paths(self, seed=420):
        np.random.seed(seed)
        paths = np.zeros((self.M, self.N + 1))
        paths[:, 0] = self.S0
        for t in range(1, self.N + 1):
            Z = np.random.normal(0, 1, self.M)
            paths[:, t] = paths[:, t - 1] * np.exp(
                (self.r - 0.5 * self.sigma**2) * self.dt + self.sigma * np.sqrt(self.dt) * Z
            )
        self.paths = paths
        return paths
    
    def set_payoff(self, payoff_fn):
        self.payoff_fn = payoff_fn
    
    def price(self):
        #given payoffs list, find mean..... and return
        if self.paths is None:
            raise RuntimeError("Paths not simulated yet.")
        if self.payoff_fn is None:
            raise RuntimeError("Payoff function not set.")
        payoffs = self.payoff_fn(self.paths)
        discounted = np.exp(-self.r * self.T) * payoffs
        return np.mean(discounted)
    
    def draw(self,save=False, type = "plot"):
        if type == "plot":
            for path in self.paths:
                plt.plot(path)
            
            if save:
                plt.savefig()
            plt.show()

        elif type == "end_dist":
            last_elements = [path[-1] for path in self.paths]
            # Plot distribution
            sns.histplot(last_elements, kde=True)
            plt.title("Distribution of last date")
            plt.xlabel("Last Element")
            plt.ylabel("Frequency")
            plt.show()


'''
    # test
classic_snowball_payoff = pf.classic_snowball_payoff
engine = MonteCarloEngine(S0=100, r=0.03, sigma=0.2, T=1, N=12, M=10000)
engine.simulate_paths()
engine.set_payoff(lambda paths: classic_snowball_payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100))
price = engine.price()
print(f"Fair Value of Classic Snowball: {price:.4f}")

'''



