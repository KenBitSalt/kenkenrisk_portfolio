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
    

    def estimate_greeks_grid(self, epsilon=1.0, epsilon_sigma = 0.01, num_points=51):
        assert num_points % 2 == 1, "num_points should be odd to center around current S0."

        original_S0 = self.S0
        original_sigma = self.sigma
        original_T = self.T
        original_dt = self.dt

        # === S0 GRID ===
        S0_array = original_S0 + epsilon * np.arange(-(num_points // 2), (num_points // 2) + 1)
        price_array = []
        delta_array = []
        gamma_array = []
        vega_array = []
        vanna_array = []

        for S0 in S0_array:
            # Base price at (S0, sigma)
            self.S0 = S0
            self.sigma = original_sigma
            self.simulate_paths()
            base_price = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))
            price_array.append(base_price)

        # === Delta & Gamma ===
        delta_array = np.gradient(price_array, epsilon)
        gamma_array = np.gradient(delta_array, epsilon)

        # === Vega: for each S0, perturb sigma ± ε once ===
        for S0 in S0_array:
            self.S0 = S0

            self.sigma = original_sigma + epsilon_sigma
            self.simulate_paths()
            price_up = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))

            self.sigma = original_sigma - epsilon_sigma
            self.simulate_paths()
            price_down = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))

            vega = (price_up - price_down) / (2 * epsilon_sigma)
            vega_array.append(vega)


            #vanna
        for S0 in S0_array:
            # === Delta under sigma+epsilon ===
            self.sigma = original_sigma + epsilon_sigma

            self.S0 = S0 + epsilon
            self.simulate_paths()
            price_up_up = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))

            self.S0 = S0 - epsilon
            self.simulate_paths()
            price_up_down = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))

            delta_up = (price_up_up - price_up_down) / (2 * epsilon)

            # === Delta under sigma-epsilon ===
            self.sigma = original_sigma - epsilon_sigma

            self.S0 = S0 + epsilon
            self.simulate_paths()
            price_down_up = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))

            self.S0 = S0 - epsilon
            self.simulate_paths()
            price_down_down = np.exp(-self.r * self.T) * np.mean(self.payoff_fn(self.paths))

            delta_down = (price_down_up - price_down_down) / (2 * epsilon)

            # === Vanna = diff of delta wrt sigma ===
            vanna = (delta_up - delta_down) / (2 * epsilon_sigma)
            vanna_array.append(vanna)

        # Restore
        self.S0 = original_S0
        self.sigma = original_sigma
        self.T = original_T
        self.dt = original_dt

        return {
            "S0_array": np.array(S0_array),
            "price_array": np.array(price_array),
            "delta_array": np.array(delta_array),
            "gamma_array": np.array(gamma_array),
            "vega_array": np.array(vega_array),
            "vanna_array": np.array(vanna_array)
        }




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



