from flask import Blueprint, request
from . import services

language_bp = Blueprint("language_bp", __name__)


@language_bp.route("/<company_name>", methods=["GET"])
def get_company_search(company_name):
    return services.get_company_search(request, company_name)


@language_bp.route("", methods=["POST"])
def post_company_new_data():
    return services.post_company_new_data(request)