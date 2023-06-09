import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import constants

app = Flask(__name__)

openai.api_key = constants.openai_api_key


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        english_question = request.form["english_question"]
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=generate_prompt(english_question),
          temperature=0,
          max_tokens=150,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0,
          stop=["#", ";"]
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(english_question):
    return """### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### {}\n
""".format(
        english_question
    )
