import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
from .data_load import load

def analyze():
    items = load('items')[['order_id','seller_id']].drop_duplicates()
    reviews = load('reviews')[['order_id','review_score']].drop_duplicates('order_id')
    seller_scores = items.merge(reviews, on='order_id').groupby('seller_id')['review_score'].mean().sort_index()
    rng = np.random.default_rng(42)
    assignment = rng.permutation(len(seller_scores)) < len(seller_scores)//2
    control = seller_scores.to_numpy()[~assignment]
    treatment = seller_scores.to_numpy()[assignment]
    n0, n1 = len(control), len(treatment)
    mean0, mean1 = control.mean(), treatment.mean()
    sd0, sd1 = control.std(ddof=1), treatment.std(ddof=1)
    diff = mean1 - mean0
    test = stats.ttest_ind(treatment, control, equal_var=False)
    se = np.sqrt(sd1**2/n1 + sd0**2/n0)
    df = (sd1**2/n1 + sd0**2/n0)**2 / ((sd1**2/n1)**2/(n1-1)+(sd0**2/n0)**2/(n0-1))
    ci = stats.t.interval(.95, df, loc=diff, scale=se)
    pooled = np.sqrt(((n1-1)*sd1**2+(n0-1)*sd0**2)/(n1+n0-2))
    d = diff/pooled
    power = TTestIndPower().power(abs(d), nobs1=n1, ratio=n0/n1, alpha=.05)
    return dict(n_control=n0,n_treatment=n1,mean_control=mean0,mean_treatment=mean1,
                sd_control=sd0,sd_treatment=sd1,difference=diff,p_value=float(test.pvalue),
                t_stat=float(test.statistic),cohens_d=d,ci_low=ci[0],ci_high=ci[1],power=float(power),
                significant=bool(test.pvalue<.05),adequately_powered=bool(power>=.8),
                practically_meaningful=bool(abs(diff)>=.2))

if __name__ == '__main__': print(pd.Series(analyze()).to_string())
