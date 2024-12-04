from flask import Blueprint, request

import controllers

products = Blueprint("products", __name__)


@products.route("/product", methods=["POST"])
def add_product():
    return controllers.add_product(request)


@products.route('/product/category', methods=['POST'])
def create_product_category():
    return controllers.create_product_category(request)


@products.route("/products", methods=["GET"])
def get_all_products():
    return controllers.get_all_products()


@products.route("/product/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    return controllers.get_product_by_id(product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    return controllers.update_product_by_id(request, product_id)


@products.route('/product/company/<company_id>', methods=['GET'])
def get_products_by_company(company_id):
    return get_products_by_company(company_id)


@products.route("/product/<product_id>", methods=["PUT"])
def product_category_update(product_id):
    return controllers.product_category_update(product_id)


@products.route('/product/activity/<product_id>', methods=['PATCH'])
def product_activity(product_id):
    return controllers.product_activity(product_id)


@products.route("/product/delete/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    return controllers.delete_product(product_id)
