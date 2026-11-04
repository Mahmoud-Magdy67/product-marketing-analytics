# Case study: Product & Marketing Analytics Sandbox

**Business question.** Where does seller acquisition lose leads, can a hypothetical premium onboarding flow be evaluated responsibly, and how often do customers return after a first order?

**Approach.** I joined public Olist marketing leads and closed deals to sellers' first marketplace orders. Because Olist does not record a sales-qualified lead event, I labeled a lead with populated origin and landing-page fields as an **SQL proxy**. For the A/B methodology demonstration, I compared sellers whose first recorded sale was after the median date with those on or before it, using seller-level mean review scores. First sale is an onboarding-date proxy, not an observed treatment assignment. For customers, I formed monthly cohorts using each unique customer's first order and measured repeat orders and payment revenue through month 12.

**Findings.** Of 8,000 MQLs, 7,940 met the SQL proxy, 828 had a closed deal, and 376 had a first order after lead contact. End-to-end conversion was **4.7%**; the largest loss was SQL proxy to closed deal (**10.4%** conversion). Median lead-to-first-order time among converters was **69 days**.

With a median first-sale cutoff of **5 November 2017**, earlier sellers averaged **3.9062** (n=1,545) and later sellers **4.0915** (n=1,545). The difference was **0.1853 points** (Welch **p≈7.03×10⁻⁸**, 95% CI **[0.1180, 0.2525]**, Cohen's d **0.194**). Observed-effect power was **99.97%**; design power for a 0.2-point difference was **99.99%**. The point estimate is below an illustrative 0.2-point practical threshold. This is an observational association: calendar time, product mix, seller volume, and review behavior may confound it. No onboarding intervention is documented, so the result does not establish a causal onboarding effect.

The **November 2017** customer cohort generated the largest observed payment revenue (**BRL 1.20 million**). Monthly repeat purchase rates are low; later cohort months are hidden where follow-up is unavailable.

**Stack.** Python, pandas, SciPy, statsmodels, Plotly, Streamlit, Parquet.

**Next.** Instrument actual SQL and onboarding events, preregister a minimum detectable effect, run a real randomized trial, and compare retention with complete equal-length follow-up.
