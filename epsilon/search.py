from flask import Flask, request, render_template
from DAO import DAO
import json

def make_keyword_list(keyword_string):
    keyword_list = []
    irrelevent = ["and", "the", "a", "an"]
    for word in keyword_string.split():
        if word.lower() not in irrelevent:
            keyword_list.append(word)
    return keyword_list


def refine_search_data(search_data):
    search_results = {}
    for item in search_data:
        if item not in search_results:
            search_results[item] = search_data.count(item)
    search_results = dict(sorted(search_results.items(), key=lambda item: item[1], reverse=True))
    print("search_result:", search_results)
    return search_results


def search(dao):
    # TODO: improve filters
    if request.method == 'POST':
        # create both queries for checking and inserting data
        sql_q = '''INSERT INTO Company (name, description) VALUES (%s, %s)'''
        # check if all form boxes are completed
        if (len(request.form['search']) == 0):
            error = 'Search box cannot be empty!'
            error_json = json.dumps({"message": error})
            return render_template('search_test.html', error=error_json)
        # if no errors
        try:
            keywords = make_keyword_list(request.form['search'])
            search_results = refine_search_data(dao.get_search_data(keywords))
            message = ""
            if search_results is None:
                message = "No results found!"
                search_results = ()
        except Exception as e:
            return render_template('search_test.html', error=e)
        return render_template('search_test.html', message=message, data=convert_search_result(search_results))
    else:
        # load if not POST
        return render_template("search_test.html")


def convert_search_result(res):
    """
    convert search result from dict (tuple->int) to json form.
    :param res: dictionary form
    :return:  json form
    """
    all_comp = []
    for d in res.keys():
        all_comp.append({"name": d[0], "description":d[1]})
    final_res = {"company_list": all_comp}
    return json.dumps(final_res)



# related to testing frontend, won't interfere with back end
def generate_error_data():
    x = {
        "message": "sample error message"
    }
    return json.dumps(x)

def generate_search_result():
    x = {
        "company_list":[
            {
                "name": "epsilon",
                "description": "sample description of epsilon"
            },

            {
                "name": "delta",
                "description": "sample description of delta"
            },
            {
                "name": "alpha",
                "description": "sample description of alpha"
            }
        ]
    }
    # return x
    return json.dumps(x)

def search_frontend_test(dao, succeed=True):
    print("search_frontend_test")
    if request.method == 'POST':
        if succeed:
            return render_template("search_test.html", data=generate_search_result())
        else:
            return render_template("search_test.html",error=generate_error_data())
    else:
        return render_template("search_test.html")
