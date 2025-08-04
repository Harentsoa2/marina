# ÉTAPE 1: Builder - Compiler l'exécutable OCaml 'marina'
# On part d'une image OCaml/Opam complète
FROM ocaml/opam:ocaml-4.14 AS builder

# Mettre à jour les dépendances système
RUN sudo apt-get update && sudo apt-get install -y make

WORKDIR /app

# Installer les dépendances OCaml listées dans le README
RUN opam install ocamlfind ounit2

# Copier tout le code source
COPY . .

# Construire l'exécutable en utilisant la commande du README
RUN make

# ---

# ÉTAPE 2: Production - Créer l'image finale avec l'API Python
# On part d'une image Python légère
FROM python:3.10-slim

WORKDIR /app

# Installer Flask, le seul prérequis de notre wrapper API
RUN pip install Flask

# Copier l'exécutable 'marina' compilé depuis l'étape de build
COPY --from=builder /app/marina ./marina

# Rendre l'exécutable 'marina' utilisable
RUN chmod +x ./marina

# Copier le script de notre wrapper API Python
COPY api_wrapper.py .

# Exposer le port sur lequel notre serveur Flask écoute
EXPOSE 8080

# Commande pour démarrer le serveur Python, qui à son tour appellera 'marina'
CMD ["python", "-u", "api_wrapper.py"]
