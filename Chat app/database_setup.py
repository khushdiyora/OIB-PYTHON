from app import db

# Create tables
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tables created")

if __name__ == '__main__':
    create_tables()
