from typing import List
from flask_mysqldb import MySQL
from databaseAccess.DAOCompanyTag import DAOCompanyTag
from exceptions.FormIncompleteError import FormIncompleteError
import json


def make_keyword_list(keyword_string: str) -> List[str]:
    """
    Returns a list of words from keyword_string removing articles.
    :param keyword_string: A sentence to obtain key word list from.
    :return List of keywords.
    """
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
    search_results = dict(sorted(search_results.items(),
                                 key=lambda item: item[1], reverse=True))
    print("search_result:", search_results)
    return search_results


def company_search(mysql: MySQL, search: str):
    """
    :param mysql: mysql db.
    :param search: user's search string
    :return json for search result and status message for search
    """
    # TODO: improve filters
    # create both queries for checking and inserting data
    dao_company_tag = DAOCompanyTag(mysql)
    # check if all form boxes are completed
    if (len(search) == 0):
        raise FormIncompleteError('Search box cannot be empty!')
    try:
        keywords = make_keyword_list(search)
        raw_search = dao_company_tag.get_search_data(keywords)
        search_results = refine_search_data(raw_search)
        message = ""
        if len(search_results) is 0:
            message = "No results found!"
        return convert_search_result(search_results), message
    except Exception as e:
        raise e


def convert_search_result(res):
    """
    convert search result from dict (tuple->int) to json form.
    :param res: dictionary form
    :return:  json form
    """
    all_comp = []
    for d in res.keys():
        all_comp.append({"tid": d[0], "name": d[1], "description": d[2], "industry": d[3]})
    final_res = {"company_list": all_comp}
    return json.dumps(final_res)
