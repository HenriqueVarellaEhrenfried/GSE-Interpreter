# ---------------------------------------------------------------------------------------------
#   Copyright (c) Henrique Varella Ehrenfried. All rights reserved.
#   Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

import json
import os
import  re
import pandas as pd
from doc_gen import generate_html

from textx import * 
from graphviz import Digraph
from pandas.io.json import json_normalize

gse_meta = metamodel_from_file('./grammar/gse.tx', skipws=False)
gse_model = gse_meta.model_from_file('./examples/example.feature')

# skipws = False : Do not skip whitespaces. By default textX skips whitespaces

Files = []

def read_files(files):
    parsed = []
    for i, f in enumerate(files):
        print(f'\n--- Reading file {i+1}: {f}')
        model = gse_meta.model_from_file(f)
        aux = extract_information(model)
        parsed.append(aux)
        Files.append(f)
    return parsed

def to_csv(parsed, file_output, sep =';', encoding = 'utf-8'):
    # Use pandas to create a dataframe
    df = pd.DataFrame.from_dict(json_normalize(parsed), orient='columns')
    # Export this dataframe as a CSV
    df.to_csv(file_output, sep=sep, encoding=encoding, index=False)

def to_json(parsed, file_output):
    f = open(file_output, "w")
    f.write(json.dumps(parsed, indent=2))
    f.close()

def extract_information(model):
    file_info = {
        "Feature":"",
        "Description":{
            "Stakeholders":[],
            "Action":"",
            "Motivation": ""
        },
        "Group":{
            "Tags":[]
        },
        "Constraints":{
            "Qualities":[],
            "Constraints":[]
        },
        "Relationship":{
            "Derived":[],
            "Contains":[],
            "Copy":[],
            "Refinament":[],
            "Dependent":[]
        },
        "Planning":{
            "Order": "",
            "Time_needed": "",
            "Num_of_developers": "",
            "Developers": [],
            "Sprint": ""
        },
        "Metrics":[],
        "Notes": [],
    }
    if (model.Feature):
        print('Feature: ' + model.Feature)
        file_info["Feature"] = model.Feature.strip()
    if (model.Description):
        print('Description Available')
        file_info['Description']['Stakeholders'] = model.Description.Stakeholder
        file_info['Description']['Action'] = model.Description.Action
        file_info['Description']['Motivation'] = model.Description.Motivation
    if (model.Group):
        print('Group Available')
        tags = []
        for g in model.Group.Groups:
            tags.append(g.Tag)
        file_info['Group']['Tags'] = flatten(tags)
    if (model.Constraints):
        print('Constraints Available')
        qualities = []
        constraints = []
        for q in model.Constraints.Qualities:
            aux = {"Item":q.Item, "Subitem": []}
            for qs in q.Subitem:
                aux["Subitem"].append(qs.Subitem)
            aux["Subitem"] = flatten(aux["Subitem"])
            qualities.append(aux)
        for c in model.Constraints.Constraints:
            aux = {"Item":c.Item, "Subitem": []}
            for cs in c.Subitem:
                aux["Subitem"].append(cs.Subitem)
            aux["Subitem"] = flatten(aux["Subitem"])
            constraints.append(aux)
        file_info['Constraints']['Qualities'] = qualities
        file_info['Constraints']['Constraints'] = constraints
    if (model.Relationship):
        print('Relationship Available')
        file_info["Relationship"]['Derived'] = model.Relationship.Derived.Requirement if model.Relationship.Derived else None
        file_info["Relationship"]['Contains'] = model.Relationship.Contains.Requirement if model.Relationship.Contains else None
        file_info["Relationship"]['Copy'] = model.Relationship.Copy.Requirement if model.Relationship.Copy else None
        file_info["Relationship"]['Refinament'] = model.Relationship.Refinament.Requirement if model.Relationship.Refinament else None
        file_info["Relationship"]['Dependent'] = model.Relationship.Dependent.Requirement if model.Relationship.Dependent else None
    if (model.Planning):
        print('Planning Available')
        file_info["Planning"]["Order"] = model.Planning.Order
        file_info["Planning"]["Time_needed"] = model.Planning.Time_needed
        file_info["Planning"]["Num_of_developers"] = model.Planning.Num_of_developers
        file_info["Planning"]["Developers"] = model.Planning.Developers
        file_info["Planning"]["Sprint"] = model.Planning.Sprint
    if (model.Metrics):
        print('Metrics Available')
        metrics = []
        for mi in model.Metrics.Metric_item:
            metrics.append({"Metric":mi.Metric, "Expected_Value": mi.Expected_Value})
        file_info["Metrics"] = metrics
    if (model.Notes):
        print('Notes Available')
        file_info["Notes"] = model.Notes.Note
    return file_info


# -------------- Helpers --------------
def num_requirements(df):
    # Return the number of lines of the dataframe. It is equal to the numebr of requirements
    return df.shape[0]

def count_developers(df):
    developers = df.loc[:, 'Planning.Developers']
    array_list = flatten(developers.values.tolist())
    array_list = [x.strip() for x in array_list]
    result = {}
    result['Developers'] = array_list
    result['All distinct developers'] = list(set(array_list))
    result['Num distinct developers'] = len(list(set(array_list)))
    result['Count appearance of developers'] = {}
    for act in list(set(array_list)):
        result['Count appearance of developers'][act] = count_appearance(act, array_list)
    return result

def count_actors(df):
    actors = df.loc[:, 'Description.Stakeholders']
    array_list = flatten(actors.values.tolist())
    array_list = [x.strip() for x in array_list]
    result = {}
    result['All actors'] = array_list
    result['All distinct actors'] = list(set(array_list))
    result['Num distinct actors'] = len(list(set(array_list)))
    result['Count appearance of actor'] = {}
    for act in list(set(array_list)):
        result['Count appearance of actor'][act] = count_appearance(act, array_list)
    return result

def get_sprint_information(df):
    sprints = df.loc[:, 'Planning.Sprint']
    array_list = flatten(sprints.values.tolist())
    array_list = [x.strip() for x in array_list]
    result = {}
    result['All Sprints'] = array_list
    result['All distinct sprints'] = list(set(array_list))
    result['Num distinct sprints'] = len(list(set(array_list)))
    result['Count appearance of sprint'] = {}
    for act in list(set(array_list)):
        result['Count appearance of sprint'][act] = count_appearance(act, array_list)
    return(result)

def count_number_of_hours_worked_in_project(df):
    time = df.loc[:, 'Planning.Time_needed']
    array_list = time.values.tolist()
    converted_time = [time_unit_converter(x, 'hours') for x in array_list]   
    # Return time in hours
    return (sum(converted_time))

def build_pert_cpm(df):
    order = df.sort_values(by=['Planning.Order'])[['Feature','Planning.Order', 'Relationship.Dependent','Planning.Time_needed']]
    array_list = order.values.tolist()
    pert = Digraph('PERT', comment='PERT-CPM Graph', format='png', node_attr={'shape': 'rectangle'}, graph_attr={'ranksep':'0.5', 'ratio':'compress'})
    MAX_ORDER = len(array_list)+1

    list_order = {}
    dependency_list = {}

    # Initialize list_order with empty arrays
    for i in range(1, MAX_ORDER):
        list_order[str(i)] = []

    # Initialize dependency_list with empty arrays
    for al in array_list:
        dependency_list[al[0]] = []

    # Create graph nodes
    for al in array_list:
        pert.node(al[0], al[0] + '\nOrder: ' + al[1] + '\nTime needed: '+ al[3])
        list_order[al[1][:-2]].append(al[0])
        if len(al[2]) > 0:
            for dep in al[2]:
                dependency_list[al[0]].append(dep)

    # Add order edges 
    for i in range(1, MAX_ORDER - 1):
        next_level = None
        # Find out the next order
        for aux_i in range(i+1, MAX_ORDER):
            if len(list_order[str(aux_i)]) > 0:
                next_level = aux_i
                break
        # Add order edge if next level is not None
        if next_level != None:
            for source_node in (list_order[str(i)]):
                for destination_node in (list_order[str(next_level)]):
                    pert.edge(source_node, destination_node, constraint='true')
            
    # Add dependency edges
    for i in range(0,len(array_list)):
        for dep in dependency_list[array_list[i][0]]:
            pert.edge(dep, array_list[i][0], constraint='true', color="red")       
    
    pert.edge_attr.update(arrowhead='vee')
    pert.render()
    return("../../PERT.gv.png")

def count_req_by_group(df):
    groups = df.loc[:, 'Group.Tags']
    array_list = flatten(groups.values.tolist())
    array_list = [x.strip() for x in array_list]
    result = {}
    result['All groups'] = array_list
    result['All distinct groups'] = list(set(array_list))
    result['Num distinct groups'] = len(list(set(array_list)))
    result['Count appearance of group'] = {}
    for act in list(set(array_list)):
        result['Count appearance of group'][act] = count_appearance(act, array_list)
    return(result)

def count_appearance(item, array):
    counter = 0
    for a in array:
        if a == item:
            counter = counter + 1
    return counter

def flatten(my_list):
    flat_list = [item for sublist in my_list for item in sublist]
    return flat_list

def time_unit_converter(time, desired_unit):
    FACTOR ={
        "seconds": 1.0,
        "second" : 1.0,
        "minutes" : 60.0,
        "minute" : 60.0,
        "hours" : 3600.0,
        "hour" : 3600.0,
        "days" : 86400.0,
        "day" : 86400.0,
        "weeks" : 604800.0,
        "week" : 604800.0,
        "months" : 2592000.0,
        "month" : 2592000.0,
        "years" : 31536000.0,
        "year" : 31536000.0,

    }
    splitted = time.strip().split(' ')
    value = float(splitted[0])
    unit = splitted[1].lower()

    time_in_seconnds = FACTOR[unit] * value

    return (time_in_seconnds / FACTOR[desired_unit])


def hash_to_html_count(array, hash, header=["Item", "Number of occurences"]):
    string = "<table class='striped container'>\n<tr>\n\t<th>"+ header[0] +"</th>\n\t<th>" + header[1] + "</th></tr>\n"
    for item in array:
        string = string + "<tr>\n\t<td>" + str(item) + "</td>\n\t<td>" + str(hash[item]) + "</td></tr>\n"
    string = string + "</table>"
    return string

def string_to_html(string):
    return ("<p>" + str(string) + "</p>\n")

def get_files_from_dir(dir):
    start_dir = os.getcwd()
    os.chdir(dir)
    current_dir = os.getcwd()

    # print(f"Verificando diretório: {current_dir}")

    regex = re.compile('[\w]*\.feature$', re.IGNORECASE)
    
    files_in_dir = os.listdir()

    files = []
    num_match = 0
    num_not_match = 0
    # print('--------- FILES ---------\n')
    # print(files_in_dir)
    # print('\n')
    for f in files_in_dir:
        if regex.match(f):
            # print(f" + Deu Match de :: {f}")
            num_match = num_match + 1
            files.append(current_dir + '/' + f)
        else:
            # print(f" - Não deu Match de :: {f}")
            num_not_match = num_not_match +1
    # print('\n')
    # print('--------- STATISTICS ----------\n')
    # print(f'Number of match: {num_match}\nNumber of not match: {num_not_match}\n')

    os.chdir(start_dir)
    return (files)




def generate_docs(parsed):
    # All df columns
    # ['Constraints.Constraints', 'Constraints.Qualities', 'Description.Action', 'Description.Motivation', 
    # 'Description.Stakeholders', 'Feature', 'Group.Tags', 'Metrics', 'Notes', 'Planning.Developers', 
    # 'Planning.Num_of_developers', 'Planning.Order', 'Planning.Sprint', 'Planning.Time_needed', 
    # 'Relationship.Contains', 'Relationship.Copy', 'Relationship.Dependent', 'Relationship.Derived', 
    # 'Relationship.Refinament']

    df = pd.DataFrame.from_dict(json_normalize(parsed), orient='columns')
    num_req = num_requirements(df)
    count_actor = count_actors(df)
    count_developer= count_developers(df)
    get_sprint_info = get_sprint_information(df)
    count_number_of_hours_worked = count_number_of_hours_worked_in_project(df)
    build_pert = build_pert_cpm(df)
    c_req_by_group = count_req_by_group(df)

    data={
        "Num Req": string_to_html(num_req),
        "Num Actors": string_to_html(count_actor["Num distinct actors"]),
        "Actors": string_to_html(", ".join(count_actor["All distinct actors"])),
        "Num Occurences actor": hash_to_html_count(count_actor["All distinct actors"],count_actor["Count appearance of actor"],["Actor", "Number of occurences"]),
        "Num Developers": string_to_html(count_developer["Num distinct developers"]),
        "Developers": string_to_html(", ".join(count_developer["All distinct developers"])),
        "Num Occurences developer": hash_to_html_count(count_developer["All distinct developers"],count_developer["Count appearance of developers"], ["Developer", "Number of occurences"]),
        "Estimated Time": string_to_html(str(count_number_of_hours_worked) + ' hours'),
        "Num Sprints": string_to_html(get_sprint_info['Num distinct sprints']),
        "Num req by group": hash_to_html_count(c_req_by_group['All distinct groups'],c_req_by_group['Count appearance of group'], ["Group", "Number of occurences"]),
        "PERT": build_pert,
        "FILES": Files
    }
    generate_html(data)

    

# Create an array of Dictionaries. Each item of the array is a file parsed
# parsed = read_files(['./examples/example.feature', './examples/example2.feature'])
# parsed = read_files(get_files_from_dir('./examples'))

# get_files_from_dir('./examples')

# generate_docs(parsed)


# print(time_unit_converter('365 days', 'year'))

# To generate editable files

# to_json(parsed, './Teste1.json')
# to_csv(parsed, './Teste2.csv')
