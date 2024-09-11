import os
from pathlib import Path
from flask_apscheduler import APScheduler
from flask import Flask, jsonify, redirect, request, render_template
import numpy as np
import requests


from src.mongo_db.database import StockTransactionManager
from stock_agent.components.deployment.environment import DeploymentStockMarketEnv
from stock_agent.components.deployment.sampler import Updater
from stock_agent.components.model.environment import StockMarketEnv
from stock_agent.components.model.networks import create_actor_model_3
from stock_agent.pipeline.stage_05_model_evaluation import ModelEvaluationTrainingPipeline
from stock_agent.utils.common import setup_env

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
setup_env()
app.config.from_object(Config)
db_api = os.environ["mongo_db"]
security_key = os.environ["security_key"]
manager = StockTransactionManager(f"mongodb+srv://{db_api}@cluster0.acdf1pn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", "stock_db")
# manager = StockTransactionManager("mongodb://localhost:27017/?retryWrites=false&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000", "stock_db")
updater = Updater()
actor = create_actor_model_3((10,126))
actor.load_weights(Path("artifacts/model_trainer/actor.h5"))
env = StockMarketEnv(20,updater)
env = DeploymentStockMarketEnv(20, manager, updater, env=env)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# Route to render the HTML page with the transaction form
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get_stock_data')
def get_stock_data():
    account = manager.get_account_state()
    return jsonify(account)
# Route to fetch portfolio data
@app.route('/api/portfolio')
def get_portfolio():
    portfolio = env.portfolio_value
    return jsonify(portfolio)

# Route to fetch cash balance
@app.route('/api/profit')
def get_profit():
    cash = env.portfolio_value - env.initial_cash
    return jsonify(cash)
# Route to fetch cash balance
@app.route('/api/cash')
def get_cash():
    cash = env.cash
    return jsonify(cash)

@app.route(f'/{security_key}')
@app.route(f"/{security_key}/<address>")
def update(address):
    if address == "run":
        env.update()
        print(env.cash)
        return jsonify({"status": "success"})
    elif address == "update":
        manager.update_account_state(env)
        return jsonify({"status": "success"})
    elif address == "setenv":
        manager.set_account_state(env)
        return jsonify({"status": "success"})
    elif address == "price":
        manager.get_curr_prices()
        return jsonify({"status": "success"})
    elif address == "predict":
        update()
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "invalid"})



@app.route('/api/all_data')
def get_all_data():
    account_state = manager.get_account_state()
    portfolio = env.portfolio_value
    profit = env.portfolio_value - env.initial_cash
    cash = env.cash
    investment = env.initial_cash
    min_cash = env.min_balance
    last_prediction = account_state.get("last_pred_time_stamp", "")
    history = account_state.get("history", "")
    start_date = account_state.get("start_time_stamp", "")
    transactions = manager.get_last_10_transactions()
    stocks = account_state.get("stocks", {})

    data = {
        "portfolio": portfolio,
        "profit": profit,
        "cash": cash,
        "investment": investment,
        "lastPrediction": last_prediction,
        "startDate": start_date,
        "transactions": transactions,
        "stocks": stocks,
        "minCash": min_cash,
        "history": history
    }
    return jsonify(data)





        

@app.route('/api/new_data')
def get_curr_prices():
    data = {"data": manager.get_curr_prices()}
    return jsonify(data)



@app.route('/api/transaction', methods=['POST'])
def transaction():
    data = request.form.to_dict()
    security_key_1 = data["security_key"]
    amount = int(data["amount"])
    stock_id = int(data["stock_id"])
    transaction_type = data["transaction_type"]
    if security_key_1 == security_key:
        status = True
    else:
        status = False
    if transaction_type == "deposit":
        env.cash_deposit(amount, status)
    elif transaction_type == "withdraw":
        env.cash_withdraw(amount, status)
    elif transaction_type == "buy":
        env.buy_stocks(stock_id-1, amount, status)
    elif transaction_type == "sell":
        env.sell_stocks(stock_id-1, amount, status)
    manager.update_account_state(env)
    print(env.render())
    
    return redirect("/")


@scheduler.task('interval', id='update_stocks', seconds=(60*60*4))
def update():
    components = manager.get_curr_prices()
    if components:
        print(manager.prices)
        updater.update(np.array(components))
        action = np.squeeze(actor(np.expand_dims(env.get_observation(),0)))
        env.step(action)
        manager.update_account_state(env)
        print(env.render())

@scheduler.task('interval', id='inactive', seconds=(20))
def request_site():
    uri = "https://stocktrader-6dv1.onrender.com/api/cash"
    response = requests.get(uri)
    uri = "https://portfolio-server-vcsv.onrender.com"
    response = requests.get(uri)

def update_env(env):
    obj = ModelEvaluationTrainingPipeline()
    env = obj.main()
    env = DeploymentStockMarketEnv(20, manager, updater, env=env)
    return env


if __name__ == "__main__":
    # Initialize StockTransactionManager
    
    # manager.get_curr_prices()
    manager.set_account_state(env)
    env.update_portfolio_1()
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)

