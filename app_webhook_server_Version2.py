from flask import Flask, request, jsonify
from app.trade_executor import execute_trade
from app.logger import log_trade

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    action = data.get("action")
    quantity = int(data.get("quantity", 1))

    try:
        order_id = execute_trade(symbol, action, quantity)
        log_trade(symbol, action, quantity, order_id)
        return jsonify({"status": "success", "order_id": order_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)