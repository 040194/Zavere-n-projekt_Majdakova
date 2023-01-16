from audioop import avg
from flask import Flask, jsonify, render_template
import db_operations, cas



app = Flask(__name__)


@app.route('/main')
def domov():
	return render_template(''), 200 #zobrazenie stranky


@app.route('/cas')
def get_current_time(): 
	"""
		funkcia ktora vrati aktualny cas 	
	"""
	return cas.cas(), 200


@app.route('/room/<room_id>')
def get_room_details(room_id):
	value = db_operations.get_room_data(room_id)	

	return jsonify(value), 200


#flask sa automaticky reloadne ak zisti zmenu v kode
if __name__ == "__main__":
    app.run(debug=True, host = "localhost", port=5000)












