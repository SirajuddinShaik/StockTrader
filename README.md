# 📈 StockTrader
A model capable to predicting multiple buy and sell actions simultaneously.
Its 🔥LIve at https://stocktrader-6dv1.onrender.com


Welcome to the StockTrader project! This repository contains an end-to-end stock trading MLOps pipeline using a Deep Deterministic Policy Gradient (DDPG) algorithm for reinforcement learning. The project involves several key steps, from data ingestion to model training and evaluation, all aimed at creating a robust stock trading system.

## Table of Contents

- [Overview](#overview)
- [Pipeline Details](#pipeline-details)
  - [Data Ingestion](#data-ingestion)
  - [Data Evaluation](#data-evaluation)
  - [Data Transformation](#data-transformation)
  - [Model Training](#model-training)
  - [Model Evaluation](#model-evaluation)
- [Model Architecture](#model-architecture)
- [Prediction Interval](#prediction-interval)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

StockTrader leverages deep reinforcement learning to predict stock market actions such as buying, selling, or holding stocks. The project uses the DDPG algorithm to train an actor-critic model that makes decisions based on historical stock data. The app is developed using Flask and predicts stock actions every 4 hours. The model is capable of predicting multiple buy and sell actions simultaneously.

## Pipeline Details

### Data Ingestion 📥

The data ingestion pipeline uses the Twelve Data API to retrieve historical stock data for the stocks specified in `utils/stock_names.txt`. The data is then saved to CSV files for further processing.

### Data Evaluation 🔍

The data evaluation pipeline cleans the data by removing null values and stores the cleaned data in the `artifact/data_evaluation` directory.

### Data Transformation 🔄

In the data transformation pipeline, data from 20 different stocks is combined into a single pandas DataFrame. This combined data is then split into training and test datasets, which are saved in the `artifacts/data_transformation` directory.

### Model Training 🏋️‍♂️

The model training pipeline uses the cleaned and transformed data to train the DDPG model. The training process is implemented in `model_trainer.py`, where the model is optimized to make accurate stock trading decisions.

### Model Evaluation 📊

The model evaluation pipeline assesses the performance of the trained model. This involves running the model on test data and generating performance metrics, which are saved for analysis.

## Model Architecture 🧠

The actor model in the DDPG algorithm has an output shape of (3, 20) for 20 stocks. The output consists of:

1. **Action Selection (Row 1)**: Decides whether to buy, sell, or hold each stock.
2. **Buy Probability (Row 2)**: Uses softmax to allocate available money across stocks.
3. **Sell Probability (Row 3)**: Uses softmax to determine the probability of selling stocks based on the stock count in the environment.

### Output Layer Explanation 🔍

Here's a simplified explanation of the output layer in the actor model:

```python
out = Lambda(wrapped_tf_fn)(x)
out1 = Dense(3, activation='softmax')(out)
out2 = Lambda(wrapped_tf_fn)(out1)
out2 = Dense(20, activation="softmax")(out2[:,:2])
argmax = Lambda(wrapped_argmax)(out1)  # Apply argmax function
argmax = Lambda(wrapped_cast)(argmax)  # Cast to float32
expanded = Lambda(wrapped_expand_dims)(argmax)  # Expand dimensions
outputs = Concatenate(axis=1)([expanded, out2])
```

- `out1` applies a softmax activation to determine the action (buy, sell, hold).
- `out2` further processes the probabilities for buying and selling stocks.
- `argmax` selects the action with the highest probability.
- `expanded` adjusts the tensor dimensions for concatenation.
- `outputs` combines the action and probability tensors into the final output.

## Prediction Interval ⏱️

The app predicts stock actions every 4 hours, ensuring timely decision-making in the stock market.

## Usage 🚀

To run the app, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/SirajuddinShaik/StockTrader.git
   cd StockTrader
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   flask run
   ```

4. The app will start predicting stock actions every 4 hours.

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For detailed information on each pipeline stage and model implementation, refer to the respective Python scripts in the repository. Happy trading! 📊🚀