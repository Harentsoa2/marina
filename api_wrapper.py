import subprocess
from flask import Flask, request, jsonify

# Initialiser l'application Flask
app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_proposition():
    """
    Endpoint pour résoudre une proposition logique.
    Attend une requête POST avec un JSON contenant la clé "proposition".
    Exemple: curl -X POST -H "Content-Type: application/json" -d '{"proposition": "a & ~a"}' http://localhost:8080/solve
    """
    # Récupérer le JSON de la requête
    data = request.get_json()
    if not data or 'proposition' not in data:
        return jsonify({"error": "La requête doit être un JSON avec une clé 'proposition'."}), 400

    prop = data['proposition']

    # Chemin vers l'exécutable marina dans le conteneur
    marina_executable = "./marina"

    try:
        # Exécuter la commande marina en passant la proposition comme argument
        # On capture la sortie standard (stdout) et les erreurs (stderr)
        result = subprocess.run(
            [marina_executable, prop],
            capture_output=True,
            text=True,  # Pour obtenir stdout/stderr en tant que chaîne de caractères
            check=True  # Pour lever une exception si la commande échoue (code de sortie non nul)
        )

        # Renvoyer la sortie de la commande en cas de succès
        return jsonify({
            "status": "success",
            "output": result.stdout.strip()
        })

    except subprocess.CalledProcessError as e:
        # Si marina retourne une erreur (ex: syntaxe incorrecte), on la renvoie
        return jsonify({
            "status": "error",
            "error_message": "Erreur lors de l'exécution de marina.",
            "details": e.stderr.strip()
        }), 400 # Bad Request, car la proposition était probablement mauvaise
        
    except FileNotFoundError:
        # Au cas où l'exécutable ne serait pas trouvé
        return jsonify({"error": "L'exécutable 'marina' n'a pas été trouvé."}), 500

if __name__ == '__main__':
    # Lancer le serveur sur le port 8080, accessible depuis l'extérieur du conteneur
    app.run(host='0.0.0.0', port=8080)
