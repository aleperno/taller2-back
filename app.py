from models import Base, engine
from api.admin_resources import app, check_admin_status


Base.metadata.create_all(engine)
check_admin_status()

if __name__ == "__main__":
    app.run()
