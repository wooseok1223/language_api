from flask import Blueprint, request
from . import services


search_bp = Blueprint("search_bp", __name__)


@search_bp.route("", methods=["GET"])
def get_company_name_autocomplete():
    return services.get_company_name_autocomplete(request)