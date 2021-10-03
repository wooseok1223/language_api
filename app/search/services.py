import sys
from operator import itemgetter

from app.models.company import Company
from utill.datatypes import object_as_dict, convert_to_query_dict
from utill.handler import api_handler
from sqlalchemy import or_


@api_handler
def get_company_name_autocomplete(request):
    language = request.headers.get('x-wanted-language')

    name = request.args.get('query')

    company = Company.query.filter(or_(
        Company.company_ko.like(f'%{name}%'),
        Company.company_en.like(f'%{name}%'),
        Company.company_ja.like(f'%{name}%')
    )).all()

    company = convert_to_query_dict(company)

    company_name_list = []
    for i in company:
        for k, v in i.items():
            if language in k:
                company_name_list.append({"company_name": v})

    result = sorted(company_name_list, key=itemgetter('company_name'), reverse=True)
    return result
