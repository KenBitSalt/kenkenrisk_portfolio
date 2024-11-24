import scipy 
import sklearn as sk

# input 1: a list of index benchmark's percentage changr in a given period
# input 2: a matrix of pool's percentage change in the same period
# input 3: a list of pool's objective value, each for the pool's component (in order)
# input 4: a numerical target that assigns the minumum of the portfolio average objective
# input 5: a integer maximum of the maximum component of the optimized portfolio.
# output : a list of weight of the refined portfoli0

class PCA_portfolio:

    def __init__(self, index, pool, objective, target, max_comp = 2000):
        self.index = index
        self.pool = pool
        self.objectivce = objective
    
    def find_weight(self):
        pass


    def get_eigen_values(self):
        pass