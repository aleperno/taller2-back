from models import Session, TallerUser

s = Session()


def create_users():
    s.add(TallerUser(name='John Doe', age=44))
    s.add(TallerUser(name='San Martin', age=999))
    s.commit()


def main():
    create_users()


if __name__ == '__main__':
    main()
