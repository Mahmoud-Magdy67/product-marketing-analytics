# Case study: Product & Marketing Analytics Sandbox

**Business question.** Where does seller acquisition lose leads, can a hypothetical premium onboarding flow be evaluated responsibly, and how often do customers return after a first order?

**Approach.** I joined public Olist marketing leads and closed deals to sellers' first marketplace orders. Because Olist does not record a sales-qualified lead event, I labeled a lead with populated origin and landing-page fields as an **SQL proxy**. I then randomly split sellers 50/50 (seed 42) to demonstrate an A/B analysis of existing seller-level mean review scores. For customers, I formed monthly cohorts using each unique customer's first order and measured repeat orders and payment revenue through month 12.

**Findings.** Of 8,000 MQLs, 7,940 met the SQL proxy, 828 had a closed deal, and 376 had a first order after lead contact. End-to-end conversion was **4.7%**; the largest loss was SQL proxy to closed deal (**10.4%** conversion). Median lead-to-first-order time among converters was **69 days**.

The simulated groups had almost identical review scores: **3.99887** control (n=1,545) and **3.99882** treatment (n=1,545). Welch's t-test gave **p=0.9988**; the 95% CI for the difference was **[−0.0676, 0.0675]** and Cohen's d was approximately **−0.00005**. This is neither statistically significant nor practically meaningful against an illustrative 0.2-point threshold. The observed-effect power of roughly 5% is descriptive and cannot prove no effect. No onboarding intervention occurred, so no causal claim is possible.

The **November 2017** customer cohort generated the largest observed payment revenue (**BRL 1.20 million**). Monthly repeat purchase rates are low; later cohort months are hidden where follow-up is unavailable.

**Stack.** Python, pandas, SciPy, statsmodels, Plotly, Streamlit, Parquet.

**Next.** Instrument actual SQL and onboarding events, preregister a minimum detectable effect, run a real randomized trial, and compare retention with complete equal-length follow-up.
