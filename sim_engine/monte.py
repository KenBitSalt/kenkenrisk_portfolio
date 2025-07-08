import numpy as np
#import payoffs as pf

#import matplotlib.pyplot as plt
#import seaborn as sns



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
        #np.random.seed(seed)
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
    

    def estimate_greeks_grid(self, epsilon=1, num_points=51):
        assert num_points % 2 == 1, "num_points should be odd to center around current value."

        result = {}

        S0_center = self.S0
        sigma_center = self.sigma
        T_center = self.T

        # === S0 GRID: for price, delta, gamma ===
        S0_array = S0_center + epsilon * np.arange(-(num_points // 2), (num_points // 2) + 1)
        price_S0 = []

        for S0 in S0_array:
            self.S0 = S0
            self.simulate_paths()
            payoff = self.payoff_fn(self.paths)
            price = np.exp(-self.r * self.T) * np.mean(payoff)
            price_S0.append(price)

        price_S0 = np.array(price_S0)
        delta_array = np.gradient(price_S0, epsilon)
        gamma_array = np.gradient(delta_array, epsilon)

        # === Sigma GRID: for vega ===
        sigma_array = sigma_center + epsilon * np.arange(-(num_points // 2), (num_points // 2) + 1)
        price_sigma = []

        self.S0 = S0_center  # reset
        for sigma in sigma_array:
            self.sigma = sigma
            self.simulate_paths()
            payoff = self.payoff_fn(self.paths)
            price = np.exp(-self.r * self.T) * np.mean(payoff)
            price_sigma.append(price)

        price_sigma = np.array(price_sigma)
        vega_array = np.gradient(price_sigma, epsilon)

        # === T GRID: for theta ===
        T_array = T_center + epsilon * np.arange(-(num_points // 2), (num_points // 2) + 1)
        price_T = []

        self.sigma = sigma_center  # reset
        for T in T_array:
            if T <= 0:
                price_T.append(np.nan)
                continue
            self.T = T
            self.dt = T / self.N
            self.simulate_paths()
            payoff = self.payoff_fn(self.paths)
            price = np.exp(-self.r * T) * np.mean(payoff)
            price_T.append(price)

        price_T = np.array(price_T)
        theta_array = -np.gradient(price_T, epsilon)

        # Restore original values
        self.S0 = S0_center
        self.sigma = sigma_center
        self.T = T_center
        self.dt = T_center / self.N

        result = {
            "S0_array": S0_array,
            "price_S0": price_S0,
            "delta_array": delta_array,
            "gamma_array": gamma_array,
            "sigma_array": sigma_array,
            "price_sigma": price_sigma,
            "vega_array": vega_array,
            "T_array": T_array,
            "price_T": price_T,
            "theta_array": theta_array
        }

        return result



    '''
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


'''
    # test
classic_snowball_payoff = pf.classic_snowball_payoff
engine = MonteCarloEngine(S0=100, r=0.03, sigma=0.2, T=1, N=12, M=10000)
engine.simulate_paths()
engine.set_payoff(lambda paths: classic_snowball_payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100))
price = engine.price()
print(f"Fair Value of Classic Snowball: {price:.4f}")

'''



