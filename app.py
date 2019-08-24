from models import Base, engine
from api.resources import app


Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run()
