import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>API du SAT Solver Marina</h1><p>Utilisez /marina?laza=VOTRE_PROPOSITION</p>'

@app.route('/marina', methods=['GET'])
def solve():
    prop = request.args.get('laza')
    if not prop:
        return jsonify({"error": "Paramètre 'laza' manquant."}), 400

    try:
        result = subprocess.run(["./marina", prop], capture_output=True, text=True, check=True)
        return jsonify({"status": "success", "output": result.stdout.strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "details": e.stderr.strip()}), 400
    except FileNotFoundError:
        return jsonify({"error": "L'exécutable 'marina' est introuvable."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
