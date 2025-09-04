from flask import Flask, render_template
from flask import request, Response
import requests
import json

app = Flask(__name__)
# init the config
# TODO: put flask settings in config.yml
app.config.from_object("settings.Config")


@app.route("/")
def homepage():
    title = "Peertube video token demo"
    paragraph = ["The amazing videon token demo using B&G Peertube!"]

    try:
        return render_template("index.html", title=title, paragraph=paragraph)
    except Exception as e:
        return str(e)


@app.route("/search", methods=["POST"])
def search():
    """Get the string from the search box and send it to the graphql service
    return the results
    """
    zoekterm = request.form.get("searchterm")

    ## PLAATSEN
    # make a graphQL query with the search term for the right Plaatsen.
    query = (
        '{terms(match: "%s" dataset: ["gtaaplaatsen", "wikidata", "erfgeo"] ) { dataset label terms { uri prefLabel altLabel } } }'
        % zoekterm
    )
    print(query)

    # get te resulting GraphQL Data from the termennetwerk
    not_url = "http://demo.netwerkdigitaalerfgoed.nl:8080/nde/graphql"
    # not_url = 'http://zorin.beeldengeluid.nl:3023/nde/graphql'

    r = requests.post(not_url, json={"query": query}, timeout=30)
    print(r.url)
    plaatsen = json.loads(r.text)
    print("DEBUG: ", plaatsen)

    ## PERSONEN
    # make a graphQL query with the search term for the right Personen.
    querypersonen = (
        '{terms(match: "%s" dataset: ["gtaapersonen", "nta"] ) { dataset label terms { uri prefLabel altLabel } } }'
        % zoekterm
    )
    print(querypersonen)

    # get te resulting GraphQL Data from the termennetwerk
    r = requests.post(not_url, json={"query": querypersonen}, timeout=30)
    personen = json.loads(r.text)
    print("DEBUG: ", personen)

    ## PERSONEN
    # make a graphQL query with the search term for the right Onderwerpen.
    queryonderwerpen = (
        '{terms(match: "%s" dataset: ["gtaaonderwerpen", "brinkman", "wo2"] ) { dataset label terms { uri prefLabel altLabel } } }'
        % zoekterm
    )
    print(queryonderwerpen)

    # get te resulting GraphQL Data from the termennetwerk
    r = requests.post(not_url, json={"query": queryonderwerpen}, timeout=30)
    onderwerpen = json.loads(r.text)
    print("DEBUG: ", onderwerpen)
    return render_template(
        "results.html",
        plaatsen=plaatsen,
        personen=personen,
        onderwerpen=onderwerpen,
        term=zoekterm,
    )


if __name__ == "__main__":
    app.run(host=app.config.get("APP_HOST"), port=app.config.get("APP_PORT"))
