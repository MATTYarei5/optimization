from flask import jsonify, request

from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object

from db import db


def add_company(request):
    post_data = request.form if request.form else request.json

    company_name = post_data.get('company_name')

    company_query = db.session.query(Companies).filter(Companies.company_name == company_name).first()

    if company_query:
        return jsonify({"message": "company already exists"}), 400

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201


def get_all_companies():
    companies_query = db.session.query(Companies).all()

    return jsonify({"message": "companies retrieved", "result": companies_schema.dump(companies_query)}), 200


def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    return jsonify({"message": "company retrieved", "result": company_schema.dump(company_query)}), 200


def update_company_by_id(request, company_id):
    post_data = request.form if request.form else request.json
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    populate_object(company_query, post_data)
    db.session.commit()

    return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200


def delete_company(company_id):
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company:
        return jsonify({"message": "company not found"}), 404

    try:
        db.session.delete(company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting company"}), 500

    return jsonify({"message": "company deleted"}), 200
