import numpy as np

'''
定义的结构性payoff方法
input must have a list of paths
'''


def classic_snowball_payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100):

    # for each path, generate a payoff
    M, N_plus1 = paths.shape
    N = N_plus1 - 1

    # 寻找敲入时间
    knocked_in = np.any(paths[:, 1:] < K_in, axis=1)
    
    # 翘出时间
    knocked_out = np.full(M, False)
    out_index = np.full(M, N)
    
    for t in range(1, N + 1):
        mask = (paths[:, t] > K_out) & (~knocked_out)
        knocked_out[mask] = True
        out_index[mask] = t

    payoff = np.zeros(M)
    for i in range(M):
        if knocked_out[i]:
            payoff[i] = S0 * (1 + coupon * out_index[i] / N)
        elif knocked_in[i]:
            payoff[i] = paths[i, -1]  # 本金损失，票息无
        else:
            payoff[i] = S0 * (1 + coupon)
    return payoff

def DCN_payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100):
    pass


def FCN_payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100):
    pass

