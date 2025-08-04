# ÉTAPE 1: Builder - Compiler l'exécutable OCaml 'marina'
# On part d'une image OCaml/Opam complète avec un tag qui existe
FROM ocaml/opam:debian-ocaml-4.14 AS builder

# Mettre à jour les dépendances système
# 'make' est souvent déjà inclus dans ces images, mais on s'en assure.
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends make

WORKDIR /app

# Installer les dépendances OCaml listées dans le README
# 'ocamlfind' est généralement déjà là, mais on l'inclut par sécurité.
RUN opam install ocamlfind ounit2

# Copier tout le code source
COPY . .

# Construire l'exécutable en utilisant la commande du README,
# mais en l'exécutant dans l'environnement opam pour trouver les bons outils.
RUN opam exec -- make

# ---

# ÉTAPE 2: Production - Créer l'image finale avec l'API Python
# On part d'une image Python légère
FROM python:3.10-slim

WORKDIR /app

# Installer Flask, le seul prérequis de notre wrapper API
RUN pip install --no-cache-dir Flask

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
