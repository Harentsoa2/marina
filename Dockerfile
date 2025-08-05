FROM ubuntu-24.04-ocaml-5.4 as Builder

RUN apt-get update 

WORKDIR /app

Copy . .

RUN opam install ocamlfind ounit2

RUN make

FROM python:3.9-slim

WORKDIR /app

COPY --from=Builder /app/marina ./marina

RUN pip install flask

COPY api_wrapper.py .

EXPOSE 8080

CMD ["python", "-u", "api_wrapper.py"]
