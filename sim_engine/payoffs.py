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
    M, N_plus1 = paths.shape
    N = N_plus1 - 1

    # 是否敲入
    knocked_in = np.any(paths[:, 1:] < K_in, axis=1)

    # 每期是否在敲入区间之内 => 赚票息
    in_coupon = (paths[:, 1:] >= K_in) & (paths[:, 1:] <= K_out)
    coupon_count = np.sum(in_coupon, axis=1)

    payoff = S0 * coupon * coupon_count / N  # 票息部分
    for i in range(M):
        if knocked_in[i]:
            payoff[i] += paths[i, -1]  # 本金损失
        else:
            payoff[i] += S0  # 本金返还

    return payoff


def FCN_payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100):
    M, N_plus1 = paths.shape
    N = N_plus1 - 1

    knocked_in = np.any(paths[:, 1:] < K_in, axis=1)
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
            payoff[i] = paths[i, -1]  # 本金损失
        else:
            payoff[i] = S0 * (1 + coupon)  # 本金 + 固定票息

    return payoff


def phoenix_payoff(paths, K_in=80, K_out=105, coupon=0.02, S0=100):
    M, N_plus1 = paths.shape
    N = N_plus1 - 1

    knocked_in_each_period = paths[:, 1:] < K_in
    knocked_in_any = np.any(knocked_in_each_period, axis=1)

    coupon_mask = ~knocked_in_each_period  # 每期未敲入 -> 收票息
    coupon_count = np.sum(coupon_mask, axis=1)

    payoff = S0 * coupon * coupon_count / N  # 已收票息

    for i in range(M):
        if knocked_in_any[i]:
            payoff[i] += paths[i, -1]  # 本金浮亏
        else:
            payoff[i] += S0  # 本金返还

    return payoff

