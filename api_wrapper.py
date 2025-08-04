import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Une page d'accueil simple qui explique comment utiliser l'API via le navigateur
@app.route('/')
def index():
    return """
    <h1>API du SAT Solver Marina</h1>
    <p>Cette API accepte uniquement les requêtes GET sur l'endpoint /solve.</p>
    <p><strong>Exemple d'utilisation dans votre navigateur :</strong></p>
    <p>Cliquez sur ce lien pour tester : 
       <a href="/solve?solve=(a%26b|c)-%3Ed<->~e">/solve?solve=(a&b|c)->d<->~e</a>
    </p>
    <p>Pour utiliser, ajoutez simplement <code>?solve=VOTRE_PROPOSITION</code> à la fin de l'URL /solve.</p>
    """

# On modifie l'endpoint pour qu'il n'accepte QUE la méthode GET
@app.route('/solve', methods=['GET'])
def solve_proposition():
    # On récupère directement le paramètre "solve" de l'URL.
    # Plus besoin de vérifier si la méthode est GET ou POST.
    prop = request.args.get('solve')

    # Si le paramètre est manquant, on renvoie une erreur claire.
    if not prop:
        return jsonify({"error": "Proposition non fournie. Veuillez utiliser le paramètre ?solve=... dans l'URL."}), 400

    # Le reste de la logique pour appeler l'exécutable marina est inchangé.
    marina_executable = "./marina"
    try:
        result = subprocess.run(
            [marina_executable, prop],
            capture_output=True,
            text=True,
            check=True
        )
        # On renvoie le résultat au format JSON, que le navigateur affichera.
        return jsonify({
            "status": "success",
            "output": result.stdout.strip()
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "error_message": "Erreur lors de l'exécution de marina.",
            "details": e.stderr.strip()
        }), 400
    except FileNotFoundError:
        return jsonify({"error": "L'exécutable 'marina' n'a pas été trouvé."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
