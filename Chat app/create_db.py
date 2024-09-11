from app import app, db  # Import the app and db from your main Flask file

# Create the application context
with app.app_context():
    db.create_all()
    print("Database tables created!")
