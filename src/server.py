from flask import Flask
from flask import request
from flask import jsonify
import gsa_advantage
from jsonp import jsonp

app = Flask(__name__)
# TODO disable in prod
app.debug = True

@app.route('/carts/<cart_id>')
@jsonp
def hello(cart_id):
    gsa_adv_u = request.args.get('u')
    gsa_adv_p = request.args.get('p')
    response = gsa_advantage.getCart(gsa_adv_u,gsa_adv_p,cart_id)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
