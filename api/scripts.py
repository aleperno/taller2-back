from models import Session, FoodieUser

s = Session()


def create_users():
    s.add(FoodieUser(name='John Doe', age=44))
    s.add(FoodieUser(name='San Martin', age=999))
    s.commit()


def main():
    create_users()


if __name__ == '__main__':
    main()
