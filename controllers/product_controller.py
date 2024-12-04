from flask import jsonify, request

from models.product import Products, product_schema, products_schema
from models.company import Companies
from models.category import Categories
from util.reflection import populate_object

from db import db


def add_product(request):
    post_data = request.form if request.form else request.json

    product_name = post_data.get('product_name')
    company_id = post_data.get('company_id')

    existing_product = db.session.query(Products).filter(Products.product_name == product_name).first()
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if existing_product:
        return jsonify({"message": "product already exists"}), 400

    if company_query == None:
        return jsonify({"message": "company does not exist"}), 404

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product created", "result": product_schema.dump(new_product)}), 201


def create_product_category(request):
    post_data = request.form if request.form else request.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    product_query.categories.append(category_query)
    db.session.commit()

    return jsonify({'message': 'association created', 'results': product_schema.dump(product_query)}), 201


def get_all_products():
    products_query = db.session.query(Products).all()

    return jsonify({"message": "products retrieved", "result": products_schema.dump(products_query)}), 200


def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product retrieved", "result": product_schema.dump(product_query)}), 200


def get_products_by_company(company_id):
    products_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not products_query:
        return jsonify({"message": "no products found for this company"}), 404

    return jsonify({"message": "products retrieved", "result": products_schema.dump(products_query)}), 200


def update_product_by_id(request, product_id):
    post_data = request.form if request.form else request.json
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    populate_object(product_query, post_data)
    db.session.commit()

    return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200


def product_category_update(request):
    post_data = request.form if request.form else request.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if product_query:
        if category_query:
            if category_query in product_query.categories:
                product_query.categories.remove(category_query)
            else:
                product_query.categories.append(category_query)

            db.session.commit()

    return jsonify({'message': 'product updated', 'results': product_schema.dump(product_query)}), 200


def product_activity(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    product_query.active = not product_query.active

    db.session.commit()

    return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200


def delete_product(product_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product:
        return jsonify({"message": "product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting product"}), 500

    return jsonify({"message": "product deleted"}), 200
