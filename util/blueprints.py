import routes


def register_blueprints(app):
    app.register_blueprint(routes.products)
    app.register_blueprint(routes.categories)
    app.register_blueprint(routes.company)
    app.register_blueprint(routes.warranties)
