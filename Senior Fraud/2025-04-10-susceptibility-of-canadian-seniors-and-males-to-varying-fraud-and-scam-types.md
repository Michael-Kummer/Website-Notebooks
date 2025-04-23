---
layout: post
title: The Demographic Divide: An Analysis of Canadian Fraud Loss Patterns
date: 2025-04-10 20:36 -0600
math: True
---
Note: This was a submission for a SOA Call for Essays and was also a final paper for BUEC 420: Data Analysis in Business Economics

## Abstract

Canadians are subject to various frauds and scams, with the dollars lost per scam influenced by an individual's senior status and gender. In the face of increasing automation, exploring current vulnerabilities to undermine scam innovation is critical. Results indicate seniors tend to lose more for most scam types, especially when scammers use a more personable method. Romance scams and investment scams will cause seniors to lose more. Males and females are most vulnerable to investment scams and romance scams, respectively, while seniors will lose more per scam for most types of scams. Professionals, such as financial planners, senior association management, and insurance managers, should implement creative intervention strategies.

## 1 Introduction

An analysis of Canadian scams reveals that the category of the scam, the method of the scam, and the demographic of the victim are related to the dollars lost per scam. A complete analysis becomes even more critical as the current scam and fraud landscape undergoes rapid innovation. Scammers are more successful with specific demographics depending on the methods and type of scam committed. As machine learning and large language models become more accessible, some scams are at risk of increasing automation. Engaging with the current scam and fraud landscape is critical to ensure that guardrails are pre-emptively implemented.

Analyzing the current landscape can assist with understanding if prior American research can be applied to Canada while also giving a picture of Canada's unique vulnerabilities. The Canadian "Anti-Fraud Centre Fraud Reporting System Dataset" will be used to determine precisely what broad effects gender and senior status have on scam efficacy. Based on the correlations between dollars lost on gender and senior status, specific scams and methods targeting those demographics were found. All significant scams and methods cause individuals to lose more if the scams are more personable but vary in impact depending on gender and senior status. The effect on each demographic varies, as some scams will impact seniors drastically differently from non-seniors, with gender following a similar pattern.

## 2 Background

Seniors in Canada have experienced a vast lifestyle change due to COVID-19, as they have become more online and increasingly isolated. Seniors have become more online at an increasing rate, with a 10% jump in internet usage for those over 75 between 2020 and 2022.[^1] During COVID, many nonprofits and volunteer-run religious organizations have also vanished.[^2] Many communities that rely on volunteers and non-profits can no longer be supported by volunteering seniors, and those seniors who want to volunteer cannot, so they are left unable to and without the social network they would have otherwise had. This combination has led to an unfortunate situation where seniors have less community support and are more online.

Every scam can have varying impacts on the victim, and even though fraud might have a significant blow on the individual's life, the incident might not have led to any direct monetary loss. Specific scams require a prior successful scam on the same victim, as the scammers require preceding information to defraud a victim successfully. These grey areas make assigning dollars lost to scams difficult as the exact dollar value of stolen personal information is difficult to quantify, and multiple scams can build off another. For example, Canada's "Anti-Fraud Centre Fraud Reporting System Dataset" contains information on over 320,000 successful and unsuccessful scams within Canada. Notably, the dataset has many victims reporting a dollar loss of $0 as the losses might have been absorbed by their workplace, or the crime might have preceded another scam where there was a monetary loss.[^3]

## 3 Methodology

The analysis was done on categorical data from Canada's Anti-Fraud Centre Fraud Reporting System Dataset. As of April 2025, the dataset contains observations from January 2020 to March 2025, totalling around 324k observations. Data where information is anonymized or N/A, data where losses were 0, and non-victim data will be excluded. The rationale is that non-zero losses do not necessarily mean they are not zero and may be extremely hard to quantify. For overly anonymized data, there are inherent difficulties with analyzing NAs.

Analysis Data = Victim ∩ Non-Zero Loss ∩ Not Anonymized/Missing

Small categories with few observations were combined or removed. For the methodology used, mail, television, video call, print, and radio were combined into an "other" category as these methods ranged from 80 to 3 observations in respective order. For scam categories, those below 200 observations were combined as the number of observations becomes a limitation to understanding their representation of the greater Canadian population.

![[ScamCategories.png]]({{'/assets/postImages/post2/ScamCategories.png' | relative_url}})
*Figure 1: Comparison between the Top 6 scams in frequency and their respective dollar loss for seniors vs non-seniors.*

![[SolicitMethods.png]]({{'/assets/postImages/post2/SolicitMethods.png' | relative_url}})
*Figure 2: Comparison between the Top 5 methods in frequency and their respective dollar loss for seniors vs non-seniors.*

### 3.1 Models

Category Interaction:

$$\ln(DollarLoss_i) = \beta_0 + \sum_j \beta_j Category_{ij} + \beta_{gender}Gender_i + \beta_{senior}Senior_i + \beta_{year}Year_i + \sum_k \beta_k SolicitMethod_{ik} + \sum_j \beta_{j,s}(Category_{ij} \times Senior_i) + \sum_j \beta_{j,g}(Category_{ij} \times Gender_i) + \varepsilon_i$$

An OLS regression will determine each variable's impact, and multiple models will be used to ensure that interactions between solicitation methods, gender, location, and year will be visualizable. The natural log of the dollar loss amount was used due to the extremely wide range between the minimum and maximum scams. Non-seniors were a reference category due to the abundance of observations, and non-seniors were more evenly spread across the scams. Overall, the gender demographics were split equally except for a few scams, meaning it does not have any significance what gender the reference category is. The year was chosen as it is simply the first year of observations.

The reference categories and methods were chosen due to their size and comparability. The reference category chosen was Emergency Fraud, where the scammer pretends to be someone the victim knows and urgently requests money for bail, a hospital bill, etc. Emergency fraud has varied solicitation methods and typically requires some information about the victim but does not require the scammer to build a relationship with the victim. Direct Call/Phone was chosen as the reference category for the solicitation methods due to the ability to do various scams over the phone. Alongside the observation counts, phone and direct call scams can be automated or done manually.

Data description-wise, much of the data contained categories with an even spread. Gender was relatively evenly split between males and females. There was near-normal distribution for the ages. Scams and solicitation methods contained few categories with many observations and some categories with very few observations.

### 3.2 Robustness Check

Due to the abundance of interaction terms, multicollinearity and homoskedasticity become problematic as the interaction terms start to predict each other. As a robustness check, values under 100, 500, and 1000 and those above 25,000, 50,000, and 100,000 were dropped. Removing either bound drastically decreases the $R^2$ to the 0.15 to 0.25 range, while removing both only minorly decreases the $R^2$ to around 0.3, meaning the extremes add explanatory power to the model. Multicollinearity and heteroskedasticity also become problematic with this many interaction terms. The basic and male/senior interaction models do not suffer from the term amount issues, but these models are only capable of an extremely simplified view. Methods to penalize specific interactions could be implemented on top of a simple demographic model, creating a more technically robust but more complex model.

## 4 Data

*Figure 3: Demographics*

Variable | Basic | Male/Senior interaction | Solicit interaction | Category Interaction
---------|-------|-------------------------|-------------------|--------------------
Intercept | 7.821*** | 7.814*** | 7.823*** | 7.266***
Male | 0.084*** | 0.092*** | -0.059 | -0.044
Senior | 0.301*** | 0.314*** | 0.396*** | 0.999***
Year | 0.164*** | 0.164*** | 0.164*** | 0.164***
Adjusted R² | 0.424 | 0.424 | 0.424 | 0.431

Note: The table's reference category is Emergency Fraud, and the reference solicit method is direct call.
*p<0.1; **p<0.05; ***p<0.01

*Figure 4: Scam Category Vulnerability Profile*

Scam & Interaction Term | Basic | Male/Senior interaction | Solicit interaction | Category Interaction
------------------------|-------|-------------------------|-------------------|--------------------
Recovery Pitch | 0.771*** | 0.774*** | 0.789*** | 0.998***
Recovery Pitch X Male | | | | 0.364**
Recovery Pitch X Senior | | | | -0.468**
Investment | 1.925*** | 1.928*** | 1.935*** | 2.317***
Investment X Male | | | | 0.251**
Investment X Senior | | | | -0.735***
Extortion | 0.033 | 0.035 | 0.058 | 1.090***
Extortion X Male | | | | -0.947***
Extortion X Senior | | | | -0.439***
Romance | 1.958*** | 1.960*** | 1.968*** | 2.525***
Romance X Male | | | | -0.509***
Romance X Senior | | | | -0.303**

Note: The table's reference category is Emergency Fraud, and the reference solicit method is direct call.
*p<0.1; **p<0.05; ***p<0.01

![[GenderSeniorityComparison.png]]({{'/assets/postImages/post2/GenderSeniorityComparison.png' | relative_url}})
*Figure 5: Comparison of frequency of gender and seniority status in investment and romance scams*

For romance scams, females will lose more than males, especially females who are non-seniors. Previous American research aligns with this, but specific research has shown that educated women who score high in risk-taking are specifically the most vulnerable to this type of scam.[^4] Results here show that females were both scammed for more money and were scammed more times than males. Women who are not seniors are scammed more often, but female senior women are scammed for more per scam.

Investment and recovery scams tend to cause male victims to lose more, with senior males losing more per scam but less overall. There is detailed American research on investment scams, with the exact demographics being individuals who are not financially destitute and willing to engage in risky behaviour.[^5] The study predicts that the desire to gain wealth is driving male individuals to seek out unregulated investing areas.[^6]

*Figure 6: Method Vulnerability Profile*

Method & Interaction Term | Basic | Male/Senior interaction | Solicit interaction | Category Interaction
--------------------------|-------|-------------------------|-------------------|--------------------
Email | -0.676*** | -0.676*** | -0.799*** | -0.581***
Email X Male | | | 0.470*** | 
Email X Senior | | | -0.227*** | 
Internet | -0.592*** | -0.591*** | -0.632*** | -0.499***
Internet X Male | | | 0.205*** | 
Internet X Senior | | | -0.114** | 
Social Media | -0.722*** | -0.722*** | -0.712*** | -0.607***
Social Media X Male | | | 0.107** | 
Social Media X Senior | | | -0.108* | 
Text Message | -0.324*** | -0.325*** | -0.215*** | -0.226***
Text Message X Male | | | 0.008 | 
Text Message X Senior | | | -0.326*** | 

Note: The table's reference category is Emergency Fraud, and the reference solicitation method is direct call. Other was significant, but Other X Male and Other X Senior were not.
*p<0.1; **p<0.05; ***p<0.01

![[MethodComparison.png]]({{'/assets/postImages/post2/MethodComparison.png' | relative_url}})
*Figure 7: Comparison of gender and seniority status for email, internet, and social media scams.*

A breakdown of methodologies shows that some methods are gendered, but there are more pronounced differences between seniors and non-seniors. The seniority difference is stark in that seniors are scammed fewer times online, but they lose a substantially larger amount per scam. This suggests that these seniors are more susceptible to scams over these mediums, and non-seniors are more accessible over these mediums.

## 5 Empirical analysis and explanation

Scams being gendered in their impacts means that the types of language used within the scams should be investigated. Seeing what exactly is enticing for each gender or age category can potentially allow us to mitigate the most significant contributing factors to being scammed. Since more personable solicitation methods are more effective than those where the person on the other end is unknown, the risk from automated scams appears to be relatively low. Protecting seniors online needs to become a priority as they are losing more per scam that might be easily preventable. Still, it is only a matter of time until scammers use machine learning to augment personable scams.

The correlations between dollar loss and gendered scams or scams that focus on seniors vary. Some scams are quite successful with specific demographics, leading to the belief that there is something intrinsic about these scams and these demographics. Specific methods where the victim is unknown, such as text messages, seem indiscriminate in who they target and have no significant demographic differences. In comparison, email is also indiscriminate, yet something specific about males and non-seniors causes them to lose more money over email. This contrast might be explained by the perception of emails versus text messages. For example, a fake login portal bank notification or e-transfer may seem more legitimate over email than text, but more research is needed to conclude why this difference exists.

A significant limitation is that we cannot see further details about each occurrence. Since so many unsuccessful attempts exist, follow-up research should be conducted on attempts and observations with a dollar loss of $0. As mentioned, the category amounts in this model are cumbersome, so a more technically robust lasso regression or other penalized method could better explain the current trends seen, especially when focusing on only larger or smaller losses. The dataset is also updated frequently, so predictive analysis is possible as multiple times a year, there are more observations to test models on.

## 6 Conclusion and Recommendations

As seniors become more online and have less social support, their susceptibility to being scammed for large sums of money becomes a critical concern. Retirement organizations such as teacher associations and advocacy groups should ensure seniors understand potential scam techniques. AI scam calls could be prevented entirely if seniors were taught to call the individual requesting money to ensure it is genuinely them and not a spoofed call. Suppose the individual is calling from potentially a hospital or courthouse; in most realistic situations, the transfer of funds can wait until the senior is at the location and can verify it is true, especially as they would most likely go to that location anyway.

More research must be conducted on what exactly makes some scams gendered and more damaging to seniors. The study on romance scams shows that risk-taking behaviour is inherently intertwined with romance scam susceptibility. The investment scam study shows that, most likely, individuals scammed by fake investments were looking for grey areas to gain money. How to use this information to help prevent scams is quite complex and will most likely have to be tailor-made.

Due to the unique nature of some scams and the rapid advancements currently being made, creative measures should be implemented for each scam category, and preventing initial contact should be focused on for all scams. The landscape for scams is constantly changing, and scammers will improve in both their skills and techniques over time. The dangers of automated scams will likely have to be met with more automation. Scams requiring prolonged contact cannot be fully automated, but as automation techniques become more impressive, protecting some victims from themselves will become increasingly challenging.

## References
I'll replace the image reference for the appendix tables with actual Markdown tables:

## Appendix

### All Models:

**Model 1: Base Vulnerability Model:**

$$\ln(DollarLoss_i) = \beta_0 + \sum_j \beta_j Category_{ij} + \beta_{gender}Gender_{Male} + \beta_{senior}Senior_i + \sum_k \beta_k SolicitMethod_{ik} + \beta_{year}Year_i + \varepsilon_i$$

**Model 2: Male-Senior Interaction:**

$$\ln(DollarLoss_i) = \beta_0 + \sum_j \beta_j Category_{ij} + \beta_{gender}Gender_i + \beta_{senior}Senior_i + \beta_{g×s}(Gender_i \times Senior_i) + \sum_k \beta_k SolicitMethod_{ik} + \beta_{year}Year_i + \varepsilon_i$$

**Model 3: Solicitation Interaction:**

$$\ln(DollarLoss_i) = \beta_0 + \sum_j \beta_j Category_{ij} + \beta_{gender}Gender_i + \beta_{senior}Senior_i + \beta_{year}Year_i + \sum_k \beta_k SolicitMethod_{ik} + \sum_k \beta_{k,s}(SolicitMethod_{ik} \times Senior_i) + \sum_k \beta_{k,g}(SolicitMethod_{ik} \times Gender_i) + \varepsilon_i$$

Note: Model 4 is our main model and is represented in 3.1 Models

### Analysis Data Description:

#### Figure A.1: Solicitation Methods

| Solicitation Method | Count |
|---------------------|-------|
| Social Media        | 15991 |
| Internet            | 13184 |
| Direct call         | 7182  |
| Email               | 3275  |
| Text message        | 2270  |
| Door to door/in person | 749 |
| Other               | 168   |

#### Figure A.2: Scam/Fraud Category

| Category | Count |
|----------|-------|
| Investments | 9632 |
| Merchandise | 8012 |
| Service | 4507 |
| Vendor Fraud | 3387 |
| Job | 3264 |
| Romance | 2698 |
| Bank Investigator | 2213 |
| Counterfeit Merchandise | 1885 |
| Extortion | 1662 |
| Emergency | 1654 |
| Other | 840 |
| Spear Phishing | 814 |
| Loan | 719 |
| Prize | 648 |
| Recovery Pitch | 518 |
| Grant | 366 |

#### Figure A.3: Age Breakdown

| Age Group | Count |
|-----------|-------|
| 1 - 20    | 1360  |
| 20 - 29   | 7430  |
| 30 - 39   | 7042  |
| 40 - 49   | 6357  |
| 50 - 59   | 5945  |
| 60 - 69   | 6318  |
| 70 - 79   | 4045  |
| 80 - 89   | 1250  |
| 90+       | 164   |

#### Figure A.4: Gender Breakdown

| Gender | Count |
|--------|-------|
| Male   | 21618 |
| Female | 21201 |
