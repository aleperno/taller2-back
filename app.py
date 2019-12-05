import logging
from models import Base, engine
from api.admin_resources import app, check_admin_status


Base.metadata.create_all(engine)
check_admin_status()


@app.before_first_request
def setup_logging():
    # Borro los handlers iniciales
    app.logger.removeHandler(app.logger.handlers[0])
    # Agrego handler re gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)

    # Seteo el mismo level que gunicorn
    app.logger.setLevel(gunicorn_logger.level)

    #app.logger.setLevel(logging.INFO)
    app.logger.info("Esto es un info")
    app.logger.warning("Esto es un warning")
    app.logger.debug("Esto es un debug")


if __name__ == "__main__":
    app.run()
