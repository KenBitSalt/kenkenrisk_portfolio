
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import seaborn as sns
import numpy as np
from scipy.stats import norm
from tqdm import tqdm
import requests

import akshare as ak

class PortfolioStressTester:
    def __init__(self, config_path="config.json", portfolio_path=None):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # 基础配置
        #self.token = self.config["TUSHARE_TOKEN"]
        #ts.set_token(self.token)
        #self.pro = ts.pro_api()


        self.lookback_years = self.config["DEFAULT_LOOKBACK_YEARS"]
        self.days = self.config["DEFAULT_VAR_DAYS"]
        self.stress_level = self.config["DEFAULT_STRESS_LEVEL"]


        self.us_sub = self.config["US_INDEX"] # 也就是SPY
        self.hk_sub = self.config["HK_INDEX"] # 也就是HSI
        self.cn_sub = self.config["CN_INDEX"] # 也就是csi500
        self.hk_industry_index_map = self.config["HK_SECTOR_TO_INDEX"] 

        # 美元兑人民币
        self.usd_rates = self.init_fx("USD", ["CNY"])['CNY']
        print(f"1 USD = {self.usd_rates} CNY")

        # 港币兑人民币（方法1：直接HKD为base）
        self.hkd_rates = self.init_fx("HKD", ["CNY"])['CNY']
        print(f"1 HKD = {self.hkd_rates} CNY")
        
        # 读取持仓表
        self.portfolio_df = None
        if portfolio_path:
            df1= pd.read_excel(portfolio_path)
            df1["标的代码"] = df1["标的代码"].astype(str).str.upper()
            #print(df1["行业信息"].unique())
            self.portfolio_df =  df1
            #print(self.portfolio_df["行业信息"].unique())
            date_col = "交易日" if "交易日" in df1.columns else "date"
            self.last_trade_date = datetime.strptime(str(df1[date_col].max()),"%Y%m%d") #最后交易日
            self.start_date = (self.last_trade_date - timedelta(days=(365 * self.lookback_years-2)))
            print("分析日期：")
            print(self.start_date,self.last_trade_date)

            # 如 industry 运维一份hk_ind_df
            if self.hk_sub == "industry":
                self.hk_industry_df = self.init_hk_ind()

            #self.start_date = (self.last_trade_date - timedelta(days=365 * self.lookback_years))
            print(self.last_trade_date)
            
            self.initialize_market_and_sector_returns()

    def init_fx(self,base="USD", symbols=["CNY", "HKD"]):
            url = f"https://open.er-api.com/v6/latest/{base}"
            resp = requests.get(url)
            data = resp.json()
            if data["result"] != "success":
                raise Exception("API error: " + data.get("error-type", "unknown"))

            rates = {sym: data["rates"][sym] for sym in symbols}
            return rates


    def init_hk_ind(self):
        all_dfs = []
        print("获取hk行业走势中")
        for sector, sym in tqdm(self.hk_industry_index_map.items()):
            #print("获取%s行业数据"%sector)
            try:
                df = ak.stock_hk_index_daily_em(symbol=sym)
                if df is None or df.empty:
                    print(f"[警告] {sector} ({sym}) 无数据")
                    continue
                # 统一列名或保留原样
                df = df.copy()
                df["sector"] = sector
                df["symbol"] = sym
                df["return"] = df["latest"].pct_change()
                all_dfs.append(df)
                print(df['date'].min())
            except Exception as e:
                print(f"[错误] 拉取 {sector} ({sym}) 失败: {e}")

        if all_dfs:
            big_df = pd.concat(all_dfs, ignore_index=True)
            big_df['trade_date'] = big_df['date'].astype(str).str.replace("-","")
            big_df = big_df[big_df['trade_date']>=(self.start_date.strftime("%Y%m%d"))]
            big_df = big_df[big_df['trade_date']<=(self.last_trade_date.strftime("%Y%m%d"))]
            big_df = big_df.set_index("trade_date")[["return","sector"]]
            
            print(big_df)
        else:
            big_df = pd.DataFrame()

        return big_df
            


    def initialize_market_and_sector_returns(self):
        """
        在 __init__ 中调用：
        - 获取 US_INDEX、HK_INDEX、CN_INDEX 的日收益率
        - 但是如果self.hk_sub == “industry”，那么self.hk_return就是init阶段所有 港股持仓的行业（l2_code）对应的指数收益率
        存储到：
            - self.us_return
            - self.hk_return
            - self.cn_return
        """
        if self.portfolio_df is None or self.last_trade_date is None:
            return

        # 参数
        last_date_str = self.last_trade_date.strftime("%Y%m%d")
        start_date_str = self.start_date.strftime("%Y%m%d")
        print(start_date_str,last_date_str )

        # 获取 config 中的替代指数
        self.us_index_code = self.us_sub
        self.hk_index_code = self.hk_sub
        self.cn_index_code = self.cn_sub

        def get_index_return(ts_code):
            #index_global_spot_em_df = ak.index_global_spot_em()
            #print(index_global_spot_em_df)          
            try:
                #df = self.pro.index_global(ts_code=ts_code, start_date=start_date_str, end_date=last_date_str)
                df = ak.index_global_hist_em(symbol=ts_code)
            #print(df)
                df["trade_date"] = df["日期"]
                df["trade_date"] = pd.to_datetime(df["trade_date"])
                df["trade_date"] = df["trade_date"].dt.strftime("%Y%m%d")
                df["close"] = df["最新价"]
                df = df.sort_values("trade_date")
                df["return"] = df["close"].pct_change()
                print(df)
                return df.set_index("trade_date")["return"]
            except Exception as e:
                print(f"❌ 获取指数 {ts_code} 失败: {e}")
                return pd.Series()
            
        # 美股与港股基准收益
        self.us_return = get_index_return(self.us_index_code)

        if self.hk_index_code != "industry":
            self.hk_return = get_index_return(self.hk_index_code)
        else:
            print("using industry performance for hk missing returns")
            self.hk_hsi = get_index_return("恒生指数") #save for replacement
            self.hk_return = self.hk_industry_df


        #cn_df = self.pro.index_daily(ts_code=self.cn_index_code, start_date=start_date_str, end_date=last_date_str)
        cn_df = ak.index_zh_a_hist(symbol=self.cn_index_code, start_date=start_date_str, end_date=last_date_str, period = "daily")
        #print(cn_df)
        cn_df["trade_date"] = cn_df["日期"]
        cn_df["trade_date"] = pd.to_datetime(cn_df["trade_date"])
        cn_df["trade_date"] = cn_df["trade_date"].dt.strftime("%Y%m%d")
        cn_df["close"] = cn_df["收盘"]
        cn_df  = cn_df.sort_values("trade_date")
        cn_df["return"] = cn_df["close"].pct_change()
        print(cn_df)
        self.cn_return = cn_df.set_index("trade_date")["return"]
        

        self.init_md()
        #print(self.us_return)
        #print(self.hk_return)

    def identify_market(self,ticker: str) -> str:
        """
        根据标的代码后缀识别市场：A股、港股、美股。默认使用 config fallback。
        """
        ticker = ticker.upper()
        if ticker.endswith(".SH") or ticker.endswith(".SZ"):
            return "CN"
        elif ticker.endswith(".SZHK") or ticker.endswith(".HK"):
            return "HK"
        elif ticker.endswith(".US"):
            return "US"
        else:
            return "UNKNOWN"
        

    from datetime import datetime, timedelta

    def fetch_price_series(self, tickers: list[str]):
        """
        获取 A股（Tushare）+ 港股/美股（AkShare）历史前复权收盘价，并保存为 CSV
        返回：{ticker: pd.Series of close prices}
        """
        import akshare as ak
        import pandas as pd
        import os
        from datetime import datetime, timedelta

        start_date = self.start_date.strftime("%Y%m%d")
        end_date = self.last_trade_date.strftime("%Y%m%d")
        today_str = datetime.today().strftime("%Y%m%d")
        
        # dict[tickers] = dataframe series of prices
        price_data = {}
        printed = 0
        for ticker in tqdm(tickers):
            market = self.identify_market(ticker)
            print(ticker,market)


            try:
                if market == "CN":
                    ticker_now = ticker.split(".")[0]
                    print(ticker_now)
                    df = ak.stock_zh_a_hist(symbol=ticker_now, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
                #df = self.pro.daily(ts_code = ticker,start_date=start_date, end_date = end_date)
                    print(df)
                    if df is not None and not df.empty:
                        print(f'good: length {len(df)}')
                        df["date"] = pd.to_datetime(df["日期"])
                        df["date"] = df["date"].dt.strftime("%Y%m%d")
                        df = df.sort_values("date")

                        # append to dict
                        series = df.set_index("date")["收盘"]
                        price_data[ticker] = series.astype(float)
                    else:
                        print("empty ", ticker)

                elif market == "HK":
                    code = ticker.replace(".SZHK", "").replace(".HK", "")#.zfill(4)
                    print(code)
                    df = ak.stock_hk_hist(symbol=code, start_date=start_date, end_date=end_date)
                    if not df.empty:
                        print(f'good: length {len(df)}')
                        df = df.rename(columns={"日期": "date", "收盘": "close"})
                        df["date"] = pd.to_datetime(df["date"])
                        df["date"] = df["date"].dt.strftime("%Y%m%d")

                        # append to dict
                        price_data[ticker] = df.set_index("date")["close"].astype(float)*self.hkd_rates
                    else:
                        print("empty ", ticker)

                elif market == "US":
                    symbol = ticker.replace(".US", "")
                    print(symbol)
                    df = ak.stock_us_daily(symbol=symbol, adjust="qfq")
                    if not df.empty:
                        print(f'good: length {len(df)}')
                        df = df.rename(columns={"日期": "date", "收盘": "close"})
                        df["date"] = pd.to_datetime(df["date"])
                        df["date"] = df["date"].dt.strftime("%Y%m%d")
                        df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]


                        #  append to dict
                        price_data[ticker] = df.set_index("date")["close"].astype(float)*self.usd_rates
                    else:
                        print("empty ", ticker)

                else:
                    print(f"⚠️ 不支持的市场或格式：{ticker}")
                printed = printed+1
                print(printed)

            except Exception as e:
                print(f"获取 {ticker} 数据失败：{e}")

        # 合并为 DataFrame 并保存
        if price_data:
            print(len(price_data))
            df_merged = pd.concat(price_data, axis=1).sort_index()
            print(df_merged.shape[1])
            df_merged["date"] = df_merged.index.astype(str)
            df_merged = df_merged.reset_index(drop=True)
            os.makedirs("data", exist_ok=True)
            save_path = f"data/prices_{self.last_trade_date.strftime("%Y%m%d")}.csv"
            #df_merged.to_csv(save_path)
            #print(f"价格数据已保存至 {save_path}")
        else:
            #print("⚠️ 无价格数据可保存")
            pass

        return price_data,df_merged

    def init_md(self):
        if self.portfolio_df is None:
            raise ValueError("未加载持仓数据")
        if self.hk_index_code == "industry":
            df = self.portfolio_df.rename(columns={
                "交易日": "date",
                "标的代码": "ticker",
                #"名义本金": "notional",
                "标的数量": "vol",
                "行业信息": "sector"
            }).copy()
        else:
            df = self.portfolio_df.rename(columns={
                "交易日": "date",
                "标的代码": "ticker",
                #"标的名称": "name",
                "标的数量": "vol",
                #"名义本金": "notional",
                #"行业信息": "sector"
            })

        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

        latest_date = df["date"].max()
        if self.hk_index_code == "industry":
            df_latest = df[df["date"] == latest_date].groupby('ticker').agg({
                #"notional": "sum",
                "vol":"sum",
                "sector": "first"   # 或者 lambda x: x.iloc[0]
            })
        else:
            df_latest = df[df["date"] == latest_date].groupby('ticker').agg({
                #"notional": "sum",
                "vol":"sum",
                #"sector": "first"   # 或者 lambda x: x.iloc[0]
            })

        if self.hk_index_code == "industry":
            ticker_to_sector = dict(zip(df_latest.index, df_latest["sector"]))
       # print(ticker_to_sector)


        df_latest["ticker"] = df_latest.index

        self.weights = df_latest.set_index("ticker")["vol"]
        self.total_size = self.weights.sum()
        self.weights = self.weights / self.weights.sum()
        tickers = self.weights.index.tolist()


        price_data,price_df = self.fetch_price_series(tickers)
        latest_price_data = price_df[price_df['date']==self.last_trade_date.strftime("%Y%m%d")].T
        latest_price_data.columns = ['price']
        df_latest = df_latest.merge(latest_price_data,how="left",right_index = True, left_index = True)
        df_latest['size'] = df_latest['vol']*df_latest['price']

        self.weights = df_latest.set_index("ticker")["size"]
        print(len(self.weights))
        self.total_size = self.weights.sum()
        print('total size is: %s' % self.total_size)
        self.weights = self.weights / self.weights.abs().sum()
        tickers = self.weights.index.tolist()

        
        print(df_latest)
        print(f"\n📌 最新持仓日期：{latest_date.date()}，共 {len(tickers)} 个标的")
        

        # 整合价格序列，计算收益
        aligned = pd.concat(price_data, axis=1).sort_index()#.dropna()
        aligned.to_excel("aligned.xlsx")
        returns = aligned.pct_change()
        #returns.to_excel("result.xlsx")
        # 遍历每列，根据 ticker 判断市场后，用相应指数 return 替换 NaN
        for col in returns.columns:
            if col.endswith((".SH", ".SZ")):
                sub_ret = self.cn_return
                print(sub_ret)
            elif col.endswith((".SZHK", ".HK")):
                if self.hk_index_code != "industry":
                    sub_ret = self.hk_return
                    print(sub_ret)
                else:
                    #TODO
                    now_indus = ticker_to_sector[col]
                    #print(f"replacing {col} with {self.hk_industry_index_map[now_indus]}")
                    sub_ret = self.hk_industry_df[self.hk_industry_df['sector'] == now_indus]["return"] #此乃对应industry的return
                    sub_ret = sub_ret.fillna(self.hk_hsi)
                    #print(sub_ret)
                    #print("hk subret")
                    #print(sub_ret)
                    #sub_ret = sub_ret[sub_ret.index]
                    #使用col判断这个hk股票数据哪个行业，并在self.hk_return中截取对应行业的returns
                    #print("使用行业数据替代hk个股缺失值")
            elif col.endswith(".US"):
                #print("us subret")
                #print(sub_ret)
                sub_ret = self.us_return
                print(sub_ret)
            else:
                continue
            returns[col] = returns[col].fillna(sub_ret).fillna(0)

        self.returns = returns.fillna(0) #考虑到三个市场存在不一样的交易日，nan日确认已为别的市场交易时候，该市场的休息日因此收益为0
        returns.to_excel(f"data/returns_{self.last_trade_date.strftime("%Y%m%d")}.xlsx")
        #print(f"returns数据整合完毕现在保存至：data/returns_{self.last_trade_date.strftime("%Y%m%d")}.xlsx")

    def run_stress_test(self, level = None, days = None,method = "parametric"):
        """
        执行一次压力测试，包括：
        - 读取最近日期的持仓数据
        - 根据标的识别市场，调用 fetch_price_series 获取历史价格
        - 计算组合收益序列、VaR、最大回撤
        - 输出行业集中度和个股集中度
        返回：dict 格式结果
        """

        if level is not None:
            y = level
        else:
            y = self.stress_level

        if days is not None:
            n = days
        else:
            n = self.days

        self.portfolio_returns = self.returns @ self.weights

        def calculate_var_maxloss(returns_df=self.returns, weights=self.weights, y=0.99, n=5, method=method):
            portfolio_returns = returns_df @ weights
            print(f"\n[VaR/ES计算] 方法={method}, 置信度={y}, 时长(日)={n}")

            if method == "empirical":
                # 历史模拟
                n_day_returns = portfolio_returns.rolling(window=n).sum().dropna()
                
                var_y = np.quantile(n_day_returns, (1-y))
                es_y = n_day_returns[n_day_returns <= var_y].mean()  # ES: 超过VaR部分的平均损失
                max_loss = n_day_returns.min()
                
                print(f"经验法: VaR(%)={var_y:.4%}, ES(%)={es_y:.4%}, MaxLoss%={max_loss:.4%}")
                return var_y, es_y, max_loss

            elif method == "parametric":
                # 正态近似
                mu = portfolio_returns.mean()
                sigma = portfolio_returns.std()
                z = norm.ppf(1 - y)
                var_1d = z * sigma - mu
                var_nd = var_1d * np.sqrt(n)

                # parametric ES (正态分布公式)
                es_1d = - (mu - sigma * norm.pdf(z) / (1 - y))
                es_nd = es_1d * np.sqrt(n)

                print(f"正态法: VaR(%)={var_nd:.4%}, ES(%)={es_nd:.4%}")
                return var_nd, es_nd, np.nan
        
        portfolio_value = self.total_size
        #portfolio_returns = returns @ weights.loc[returns.columns]
        var_perc, es_perc, max_loss_perc = calculate_var_maxloss(y=y, n=n)
        var_amt = var_perc * portfolio_value
        es_amt = es_perc * portfolio_value
        max_loss_amt = max_loss_perc * portfolio_value if not np.isnan(max_loss_perc) else np.nan

        return var_perc, var_amt, es_perc, es_amt, max_loss_perc, max_loss_amt
    

    def gen_report(self):
        self.days_range = self.config["VAR_DAYS"]
        self.levels_range = self.config["VAR_LEVELS"]
        self.methods_range = self.config["METHODS"]

        print("Generating report using: ")
        print(self.days_range,self.levels_range,self.methods_range)


        results = []
        # 迭代不同组合
        for method in self.methods_range:
            for level in self.levels_range:
                for days in self.days_range:
                    print(f"Running stress test: method={method}, level={level}, days={days}")
                    var_perc, var_amt, es_perc, es_amt, max_loss_perc, max_loss_amt = self.run_stress_test(
                        level=level,
                        days=days,
                        method=method
                    )
                    results.append({
                        "method": method,
                        "level": level,
                        "days": days,
                        "var_perc": var_perc,
                        "var_amt": var_amt,
                        "es_perc": es_perc,
                        "es_amt": es_amt,
                        "max_loss_perc": max_loss_perc,
                        "max_loss_amt": max_loss_amt
                    })


                # 转为 DataFrame 并输出 Excel
        df_result = pd.DataFrame(results)
        df_result.to_excel("stress_test_results.xlsx", index=False)
        print("✅ 已保存至 stress_test_results.xlsx")

        # 只绘制一种 method 的热力图（如 "empirical"）
        df_plot = df_result[df_result["method"] == "empirical"]

        # 构造透视表：index=days, columns=level, values=VaR%
        pivot_table = df_plot.pivot(index="days", columns="level", values="var_perc")

        # 绘制热力图
        plt.figure(figsize=(8, 5))
        sns.heatmap(pivot_table, annot=True, fmt=".2%", cmap="YlOrRd_r", cbar_kws={"label": "VaR (%)"})
        plt.title("VaR percentage heat map (empirical)")
        plt.xlabel("level of trust")
        plt.ylabel("days of holding")
        plt.tight_layout()
        plt.savefig("1.png")

        # 只绘制一种 method 的热力图（如 "empirical"）
        df_plot = df_result[df_result["method"] == "parametric"]

        # 构造透视表：index=days, columns=level, values=VaR%
        pivot_table = df_plot.pivot(index="days", columns="level", values="var_perc")

        # 绘制热力图
        plt.figure(figsize=(8, 5))
        sns.heatmap(pivot_table, annot=True, fmt=".2%", cmap="YlOrRd_r", cbar_kws={"label": "VaR (%)"})
        plt.title("VaR percentage heat map (parametric)")
        plt.xlabel("level of trust")
        plt.ylabel("days of holding")
        plt.tight_layout()
        plt.savefig("2.png")



        pass



#st = PortfolioStressTester(config_path="config.json", portfolio_path="姚泾河持仓.xlsx")
#st.gen_report()






