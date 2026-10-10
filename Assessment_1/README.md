# MapleFreight Delivery Delay Prediction

## Problem

MapleFreight Logistics moves approximately 8,000 shipments per week across Ontario, Quebec, and the Prairies. On-time performance has declined from 94% to 88%, and delays are often discovered only after customers complain.

This project predicts whether an in-transit shipment will arrive late and sends high-risk alerts to dispatch through Slack.

## Objectives

- Identify the main drivers of late delivery.
- Build a machine-learning model to predict late shipments.
- Select an operational alert threshold.
- Send high-risk shipment alerts to Slack.
- Recommend interventions that may reduce predicted risk.

## Dataset

The raw dataset contains 6,035 shipments and 23 columns. The target variable is `delivered_late`.

- `0` = delivered on time
- `1` = delivered late

Approximately 20.6% of the cleaned shipments were late.

## Data Cleaning

The following cleaning steps were completed:

- Removed fully duplicated records.
- Standardized inconsistent service-level capitalization.
- Converted 40 extreme weight values from grams to kilograms.
- Resolved one remaining conflicting duplicate shipment ID by retaining the first occurrence.
- The final cleaned dataset contains 6,000 unique shipments.
- Missing values were handled inside the modelling pipeline.
- `actual_transit_hours` was excluded from modelling because it is recorded only after delivery and would cause data leakage.

## Exploratory Data Analysis

The analysis found that late shipments generally:

- Travelled farther.
- Experienced more pickup delay.
- Faced higher traffic and route congestion.
- Had more route stops.
- Were assigned to slightly older vehicles.
- Were associated with less experienced drivers.

Storm and snow conditions had substantially higher late-delivery rates than clear weather. Contract Owner-Op had the highest observed late-delivery rate, while MapleFreight Fleet had the lowest.

## Feature Engineering

The following features were created:

- Distance per scheduled transit hour
- Pickup delay ratio
- Traffic and congestion interaction
- Route complexity
- Cyclical month features using sine and cosine transformations

## Models

A majority-class baseline and Logistic Regression were compared with CatBoost.

The final model was CatBoost with class balancing.

### Majority-Class Baseline

The majority-class baseline achieved 79.42% accuracy but detected none of the late shipments.

```text
Precision: 0.0000
Recall: 0.0000
F1 score: 0.0000
```

### Logistic Regression

At the default threshold of 0.50:

```text
Accuracy: 0.7467
Precision: 0.4317
Recall: 0.7287
F1 score: 0.5422
Average precision: 0.6050
```

### CatBoost

At the default threshold of 0.50:

```text
Accuracy: 0.7958
Precision: 0.5035
Recall: 0.5870
F1 score: 0.5421
Average precision: 0.5606
```

## Final Alert Threshold

The default classification threshold of 0.50 was replaced with a threshold of 0.31.

This threshold was selected because it provided approximately 40% precision while retaining approximately 80% recall. Missing a genuinely late shipment is more costly operationally than sending additional false alerts.

## Final Test Performance

Using CatBoost with an alert threshold of 0.31:

```text
Accuracy: 0.7183
Precision: 0.4054
Recall: 0.7895
F1 score: 0.5357
```

The model detected 195 of 247 late shipments in the test set.

Confusion matrix:

```text
[[667, 286],
 [ 52, 195]]
```

The confusion matrix shows:

- True negatives: 667
- False positives: 286
- False negatives: 52
- True positives: 195

## Model Explainability

The most important model features were:

- Weather condition
- Traffic index
- Carrier
- Scheduled transit hours
- Vehicle age
- Driver experience
- Fuel cost
- Route congestion score
- Pickup delay
- Distance relative to scheduled transit time
- Pickup delay ratio
- Distance
- Service level
- Weight
- Prior late deliveries in the previous 30 days

The feature importance results were consistent with the exploratory analysis. Weather, traffic, carrier performance, route length, and driver and vehicle characteristics were important contributors to late-delivery risk.

## Intervention Simulator

For high-risk shipments, the project tests what-if scenarios such as:

- Recovering pickup delay
- Reducing traffic exposure
- Reducing route congestion
- Removing one route stop
- Assigning a more experienced driver
- Reassigning the carrier

For the highest-risk shipment, `SHP-103230`, the predicted risk was 97.93%.

The best simulated intervention was reassigning the shipment to MapleFreight Fleet:

```text
Current predicted risk: 97.93%
Simulated risk after reassignment: 85.50%
Risk reduction: 12.43 percentage points
```

These are model-based what-if simulations and are not causal guarantees. Operational teams should validate the recommendation before taking action.

## Slack Integration

The notebook sends alerts to the `#dispatch-alerts` Slack channel.

The alert includes:

- Number of shipments above the risk threshold
- Shipment ID
- Destination
- Carrier
- Risk score
- Recommended action
- Simulated risk after the action

The test alert identified 481 shipments above the selected risk threshold and displayed the five highest-risk shipments.

The webhook URL is stored in `.env` and is not committed to the repository.

## How to Run

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Place the dataset in the project folder.

3. Create a `.env` file containing:

```text
SLACK_WEBHOOK_URL=your_webhook_url
```

4. Open the notebook:

```text
MapleFreight_Delivery_Delay_Prediction.ipynb
```

5. Run all notebook cells from top to bottom.

## Repository Contents

- `MapleFreight_Delivery_Delay_Prediction.ipynb`
- `README.md`
- `requirements.txt`
- `.gitignore`
- `.env.example`
- `screenshots/slack_alert.png`
- `maplefreight_delivery_delay_dataset.csv`
- `maplefreight_delivery_delay_dataset_cleaned.csv`

## Security

The Slack webhook is a credential.

- The real webhook URL is stored only in `.env`.
- `.env` is included in `.gitignore`.
- `.env.example` contains only a blank placeholder.
- The webhook URL is not included in the notebook, README, screenshots, or GitHub repository.

## AI Usage

An AI assistant was used to help plan the workflow, write code suggestions, troubleshoot errors, interpret model results, and improve documentation.

One incorrect early assumption was that all conflicting duplicate shipment IDs differed only in capitalization. Inspection showed that shipment `SHP-101906` had conflicting service levels: `Express` and `Standard`. The record was handled separately, the first occurrence was retained, and the cleaning decision was documented.