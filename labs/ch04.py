"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt, isclose, isfinite
from random import Random
from statistics import mean, stdev, variance, NormalDist

def mean_variance_ar1(n, sigma, rho):
    if not isinstance(n,int) or n<1 or not isfinite(sigma) or not isfinite(rho) or sigma<=0 or not -1<rho<1:
        raise ValueError('需要n>=1、sigma>0与平稳rho')
    return sigma**2/n*(1+2*sum((1-h/n)*rho**h for h in range(1,n)))

def stationary_ar1(rng, n, mu, sigma, rho):
    mean_variance_ar1(n,sigma,rho)
    values=[mu+sigma*rng.gauss(0,1)]
    innovation=sigma*sqrt(1-rho*rho)
    for _ in range(n-1):
        values.append(mu+rho*(values[-1]-mu)+innovation*rng.gauss(0,1))
    return values

def circular_block_means(values, length, repeats, seed):
    if not isinstance(length,int) or not isinstance(repeats,int) or not 1<=length<=len(values) or repeats<2:
        raise ValueError('区块长及重复次数非法')
    if any(not isfinite(v) for v in values):
        raise ValueError('重抽样输入必须有限')
    rng=Random(seed); n=len(values); estimates=[]
    for _ in range(repeats):
        sample=[]
        while len(sample)<n:
            start=rng.randrange(n)
            sample.extend(values[(start+j)%n] for j in range(length))
        estimates.append(mean(sample[:n]))
    return estimates

# %% 四期样本：均值区间与下一期预测区间
x=[.02,.04,-.01,.03]; n=len(x); s=stdev(x); m=mean(x); critical=3.182
mean_ci=(m-critical*s/sqrt(n),m+critical*s/sqrt(n))
prediction=(m-critical*s*sqrt(1+1/n),m+critical*s*sqrt(1+1/n))
assert isclose(variance(x),.00046666666666666666)
assert prediction[0]<mean_ci[0]<mean_ci[1]<prediction[1]
print({'均值区间':mean_ci,'单次预测区间':prediction})

# %% 已知高斯AR(1)：覆盖率是模拟估计，不是固定常数
n=40; mu=.01; sigma=.2; rho=.6; repeats=2000
exact_var=mean_variance_ar1(n,sigma,rho); exact_se=sqrt(exact_var)
naive_se=sigma/sqrt(n); z=NormalDist().inv_cdf(.975)
rng=Random(104); naive_hits=0; exact_hits=0; means=[]
for _ in range(repeats):
    sample=stationary_ar1(rng,n,mu,sigma,rho)
    sample_mean=mean(sample); means.append(sample_mean)
    naive_hits+=abs(sample_mean-mu)<=z*naive_se
    exact_hits+=abs(sample_mean-mu)<=z*exact_se
assert isclose(mean_variance_ar1(n,sigma,0),sigma**2/n)
assert exact_se>naive_se
print({'独立标准误':naive_se,'已知协方差标准误':exact_se,
       '有限样本有效量':sigma**2/exact_var,'模拟均值标准差':stdev(means),
       '独立错误区间覆盖率':naive_hits/repeats,'已知协方差覆盖率':exact_hits/repeats,
       '95%覆盖率的MC标准误':sqrt(.95*.05/repeats)})

# %% 环形区块：只做一条样本的重抽比较
sample=stationary_ar1(Random(204),120,mu,sigma,rho)
bootstrap_se={length:stdev(circular_block_means(sample,length,800,304+length)) for length in (1,5,10)}
assert all(v>0 for v in bootstrap_se.values())
print({'不同区块长度的均值标准误估计':bootstrap_se,'功效规划近似样本量':((1.96+.84)*.05/.005)**2})
