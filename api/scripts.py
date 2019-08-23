from models import Session, GlovoUser

s = Session()


def create_users():
    s.add(GlovoUser(name='John Doe', age=44))
    s.add(GlovoUser(name='San Martin', age=999))
    s.commit()


def main():
    create_users()


if __name__ == '__main__':
    main()
