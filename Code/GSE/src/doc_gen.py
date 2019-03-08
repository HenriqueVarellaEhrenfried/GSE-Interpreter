# ---------------------------------------------------------------------------------------------
#   Copyright (c) Henrique Varella Ehrenfried. All rights reserved.
#   Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def manage_paragraph(text):
    all_text = ""
    for tx in text:
        all_text = all_text + '<p>' + tx + '</p>\n'
    return all_text

def manage_metrics(metrics, header):
    string = "<table class='striped container'>\n<tr>\n\t<th>" + header[0] + "</th>\n\t<th>" + header[1] + "</th>\n\t<th>" + header[2] + "</th>\n\t<th>"+ header[3] + "</th></tr>\n"
    for item in metrics:
        string = string + "<tr>\n\t<td>" + str(item["acronym"]) + "</td>\n\t<td>" + str(item["name"])  + "</td>\n\t<td>" + str(item["how it works"])  + "</td>\n\t<td>" + str(item["interpretation"])  + "</td></tr>\n"
    string = string + "</table>"
    return string
def manage_requirements(files):
    string_to_return = "\n<div class='features-section'>\n"
    for file in files:
        f = open(file, "r")
        content = f.readlines()
        f.close()
        string_to_return = string_to_return + "\t<pre class=features>" + "".join(content) + "</pre>\n"

    string_to_return = string_to_return + "<div>"
    return string_to_return

def generate_html(data):
    with open('./src/Report/config.json') as handle:
        config = json.loads(handle.read())

    with open('./src/Report/metrics.json') as handle2:
        metrics = json.loads(handle2.read())

    config['Date'] = datetime.now().strftime('%B %d, %Y')

    env = Environment(loader=FileSystemLoader(SCRIPT_DIR + '/template'))
    template = env.get_template("Report.html")
    header = ['Acronym', "Name", "How it works", "Interpretation"]

    output = template.render(
        institution = config['Institution Name'],
        institution_logo = config['Institution Logo'],
        project = config['Project Name'],
        project_logo = config['Project Logo'],
        version = config['Project version'],
        date = config['Date'],
        description = manage_paragraph(config['Project description']),

        num_req = data["Num Req"],
        num_actor = data['Num Actors'],
        actors = data["Actors"],
        actor_occ = data['Num Occurences actor'],
        developers = data['Developers'],
        num_developers = data['Num Developers'],
        occ_developers = data['Num Occurences developer'],
        estimate_time = data['Estimated Time'],
        num_sprints = data['Num Sprints'],
        num_req_group = data['Num req by group'],
        pert = data["PERT"],

        metrics = manage_metrics(metrics, header),
        requirements = manage_requirements(data['FILES'])
    )
    f = open("./src/Report/Report.html", "w")
    f.write(output)
    f.close
    html = HTML('./src/Report/Report.html')
    css = CSS(string='@page { size: A4; margin: 1cm }' '* { float: none !important; };')
    html.write_pdf('./src/Report/Report.pdf', stylesheets=[css])
    # print(output)






# DOT to PNG : dot -Tpng -O .\src\PERT.dot









