# Business Insights Report: Reducing Telecom Customer Churn

*Based on a public sample dataset of 7,043 customers. The findings show how to approach the problem; they are not results from a real company, and patterns described here are associations in the data, not proven causes.*

## 1. The problem in numbers
- About **1 in 4 customers (26.5%)** in the data left the company.
- Winning a new customer costs more than keeping one, and retention offers cannot go to everyone, so the company needs to know **who** is at risk and **why**.

## 2. Who leaves
| Group | Churn rate | Comparison |
|---|---|---|
| Month-to-month contract | 42.8% | vs 11.1% (one year) and 2.9% (two year) |
| First year (0-12 months tenure) | 47.3% | vs 9.9% after month 48 |
| Fiber optic internet | 42.1% | vs 18.7% (DSL) and 7.2% (no internet) |
| Pays by electronic check | 45.7% | vs 14.9-19.3% for other payment methods |
| No Online Security | 31.4% | vs 14.4% with it |
| No Tech Support | 31.2% | vs 15.2% with it |

(Rates are from the training data, 5,634 customers.)

**Highest-risk segment: fiber optic customers on month-to-month contracts, at 55.1% churn.** Within every internet type, churn falls as the contract gets longer, and within every contract type fiber customers churn more than DSL customers. The two effects stack.

| Contract | DSL | Fiber optic | No internet |
|---|---|---|---|
| Month-to-month | 31.8% | 55.1% | 18.2% |
| One year | 9.5% | 18.6% | 2.1% |
| Two year | 2.0% | 7.1% | 1.0% |

**Why month-to-month matters most:** 55% of customers (3,102 of 5,634) are on month-to-month contracts, so the group with the highest churn is also the largest.

## 3. What the model adds
A model trained on this data scores each customer by churn risk, so the retention team can contact the riskiest customers first instead of everyone. On a held-out test of 1,409 customers (374 of whom left), at the default setting:
- It **caught 301 of the 374 customers who left (about 8 in 10)** and missed 73.
- It flagged 569 customers, of whom **about half (52.9%)** really would have left. The rest are false alarms.

The model's most influential signals match the findings above, in this order: month-to-month contract (by a wide margin), tenure, fiber optic internet, monthly charges, electronic check payment, and one-year contract. Support and security add-ons lower a customer's predicted risk.

The model scores are **rankings, not probabilities**. A score of 0.8 does not mean an 80% chance of leaving.

## 4. Recommendations
| # | Recommendation | Evidence |
|---|---|---|
| 1 | Offer month-to-month customers incentives to move to a one- or two-year contract. | Churn 42.8% vs 2.9% (two year); the model's strongest signal. |
| 2 | Start with fiber optic customers on month-to-month contracts. | 55.1% churn in this segment. |
| 3 | Strengthen onboarding and support in the first year. | 47.3% churn in months 0-12; short tenure raises predicted risk. |
| 4 | Encourage automatic payment, for example with a small incentive. | Electronic check users churn at 45.7% vs 14.9-16.2% for automatic payment. |
| 5 | Trial Online Security and Tech Support for at-risk customers. | Churn about 14-15% with these add-ons vs about 31% without. |
| 6 | Review fiber pricing and service quality. | Fiber churns 42.1% vs 18.7% for DSL; the data cannot say whether price, quality or something else is the cause. |
| 7 | Choose how many customers to contact from retention capacity and offer cost (section 5). | Precision and recall trade off as the cutoff moves. |

**Test before rolling out.** These findings show who leaves, not that a given offer keeps them. Customers on automatic payment or with support add-ons may simply be more settled to begin with. Run each offer as a small controlled test (offer vs no offer) and measure how many customers it actually keeps.

## 5. How many customers to contact
The model can flag more or fewer customers. Flagging more catches more churners but wastes more offers; flagging fewer wastes less but misses more churners. Example from the out-of-fold analysis (tuned models were not used for this analysis):

| Customers flagged | Precision | Recall |
|---|---|---|
| About 57% (Logistic Regression, cutoff 0.3) | 0.426 | 0.922 |
| About 41% (Logistic Regression, cutoff 0.5) | 0.516 | 0.794 |
| About 24% (Logistic Regression, cutoff 0.7) | 0.641 | 0.579 |

Precision is the share of flagged customers who really would leave; recall is the share of all churners who get flagged. **The best setting depends on numbers this dataset does not contain**, so none is recommended here. Fill in these inputs to choose:
- Number of customers the retention team can contact: [to be supplied]
- Cost of one retention offer: [to be supplied]
- Value of a customer kept (e.g. remaining revenue): [to be supplied]
- Share of contacted at-risk customers the offer actually keeps (from a controlled test): [to be supplied]

A customer is worth contacting when (chance they would leave) x (chance the offer keeps them) x (value of keeping them) exceeds the cost of the offer.

## 6. Fairness and customer experience
- Senior citizens churn more (44.1% vs 23.3% for non-seniors in the test set), and the model flags **66.2% of senior customers** vs 35.6% of non-seniors, about 1.5 times each group's real churn rate in both cases. Seniors are not under-served (the model catches 91.8% of senior churners vs 76.4% of non-senior churners), but two thirds of senior customers would receive outreach at the default setting, so contact volume and tone for that group deserve care.
- Only 222 senior customers were in the test set, so these figures are noisy.
- Gender was removed from the model because it showed no link to churn (26.6% vs 26.4%).
- Only SeniorCitizen was checked, and one check does not prove the model is fair.

## 7. Limits of this analysis
- Public sample data, a single snapshot with no time dimension.
- The models perform about equally well (ROC-AUC around 0.84), which suggests the data itself limits how well churn can be predicted.
- Costs, offer effectiveness and customer value are unknown, so no financial impact is estimated.
- Test results come from one split with 374 churners and carry sampling noise.

## 8. Suggested next steps
1. Supply the cost and value inputs in section 5 and choose the contact volume.
2. Run controlled tests of the top two or three offers on the highest-risk segments.
3. Retrain and monitor the model on current company data before using it for real decisions.
