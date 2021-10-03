from app.exceptions import NotFoundException
from app.models.tag import Tag
from utill.handler import api_handler
from utill.datatypes import object_as_dict
from app.models.company import Company
from sqlalchemy import or_
from app.extensions import db


@api_handler
def get_company_search(request, company_name):
    language = request.headers.get('x-wanted-language')

    company = Company.query.filter(or_(
        Company.company_ko == company_name,
        Company.company_en == company_name,
        Company.company_ja == company_name
    )).first()

    if company is None:
        raise NotFoundException(error_message="없는회사")

    tag = Company.get_tag(company)

    company = object_as_dict(company)
    tag = object_as_dict(tag)

    company_name = None
    for k, v in company.items():
        if language in k:
            company_name = v

    tag_name = None
    for k, v in tag.items():
        if language in k:
            tag_name = v

    tag_name = tag_name.split('|')
    tag_name = ' '.join(tag_name).split()

    result = {
        "company_name": company_name,
        "tags": tag_name
    }

    return result


@api_handler
def post_company_new_data(request):
    language = request.headers.get('x-wanted-language')

    param = request.json.copy()
    company_name_param = param.get('company_name', '')
    tags_param = param.get('tags', '')

    company_name_param_list, tags_param_list = [], []
    for i in company_name_param.keys():
        company_name_param_list.append('company_' + i)

    tag_name_param_pretreatment = {}
    if tags_param:
        for v in tags_param[0].values():
            for k in v.keys():
                tag_name_param_pretreatment['tag_' + k] = ''
                tags_param_list.append('tag_' + k)

    company_name_param_pretreatment = {}
    for k, v in company_name_param.items():
        company_name_param_pretreatment.update({'company_' + k: v})

    for i in tags_param:
        for value in i.values():
            for k, v in value.items():
                value = tag_name_param_pretreatment.get('tag_' + k) + '|' + v
                tag_name_param_pretreatment['tag_' + k] = value

    not_exist_company_list = list(set(company_name_param_list) - set(Company.column_list()))
    not_exist_tag_list = list(set(tags_param_list) - set(Tag.column_list()))

    if not_exist_company_list or not_exist_tag_list:
        Company.add_column(db, not_exist_company_list, not_exist_tag_list)

    metadata = db.MetaData()
    company_instance = db.session.execute(
        db.Table('company', metadata, autoload=True, autoload_with=db.engine).insert(), company_name_param_pretreatment)
    row_id = company_instance.lastrowid

    tag_name_param_pretreatment.update({"company": row_id})

    db.session.execute(db.Table('tag', metadata, autoload=True, autoload_with=db.engine).insert(),
                       tag_name_param_pretreatment)

    db.session.commit()

    result = {}

    company_name, tag_set = None, None
    for k, v in company_name_param_pretreatment.items():
        if language in k:
            company_name = v

    for k, v in tag_name_param_pretreatment.items():
        if language in k:
            tag_set = v

    tag_name = tag_set.split('|')
    tag_name = ' '.join(tag_name).split()

    result.update({'company_name': company_name})
    result.update({'tags': tag_name})

    return result
