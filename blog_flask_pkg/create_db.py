from blog_flask_pkg import create_app, db

# Create the Flask application
app = create_app()


with app.app_context():
    
    db.create_all()