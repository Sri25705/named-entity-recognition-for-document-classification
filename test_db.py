from app import app
from models import db, User

with app.app_context():
    # Create a new user
    new_user = User(email="test@example.com", password="securepassword")
    db.session.add(new_user)
    db.session.commit()
    print("New user added!")

    # Query all users
    users = User.query.all()
    print("All Users:", users)

    # Update a user
    user_to_update = User.query.filter_by(email="test@example.com").first()
    if user_to_update:
        user_to_update.password = "newsecurepassword"
        db.session.commit()
        print("User password updated!")

    # Delete a user
    user_to_delete = User.query.filter_by(email="test@example.com").first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        print("User deleted!")
