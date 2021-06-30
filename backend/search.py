from flask import Flask, request, render_template
from DAO import DAO

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
    print(search_results)
    return search_results


def search(dao):
    # TODO: improve filters
    if request.method == 'POST':
        # create both queries for checking and inserting data
        sql_q = '''INSERT INTO Company (name, description) VALUES (%s, %s)'''
        # check if all form boxes are completed
        if (len(request.form['search']) == 0):
            error = 'Search box cannot be empty!'
            return render_template('search.html', error=error)
        # if no errors
        try:
            keywords = make_keyword_list(request.form['search'])
            search_results = refine_search_data(dao.get_searchdata(keywords))
            message = ""
            if search_results is None:
                message = "No results found!"
                search_results = ()
        except Exception as e:
            return render_template('search.html', error=e)
        return render_template('search.html', message=message, data=search_results)
    else:
        # load if not POST
        return render_template("search.html")