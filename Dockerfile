
FROM ocaml/opam:ubuntu-24.04-ocaml-5.4 as builder

RUN sudo apt-get update && sudo apt-get install -y m4 build-essential

WORKDIR /app

COPY . .

RUN opam install -y ocamlfind ounit2

RUN eval $(opam env) && make

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app/marina ./marina

RUN pip install flask

COPY api_wrapper.py .

EXPOSE 8080

CMD ["python", "-u", "api_wrapper.py"]
