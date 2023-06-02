from bs4 import BeautifulSoup
from blog_flask_pkg.models import User, Post



def get_csrf_token(client, url):
    response = client.get(url)
    soup = BeautifulSoup(response.data, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
    return csrf_token


def test_register(client, app):
    response = client.get("/register")
    soup = BeautifulSoup(response.data, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    response = client.post("/register", data={
        "csrf_token": csrf_token,
        "uname": "admintest",
        "email": "admintest@gmail.com",
        "passw": "tester@123",
        "confirm_passw": "tester@123"
    })

    with app.app_context():
        user = User.query.filter_by(username="admintest").first()
        assert user.username == "admintest"
        assert user.email == "admintest@gmail.com"

def test_login_post_and_del(client, app):
    # Register a user
    response = client.post("/register", data={
        "csrf_token": get_csrf_token(client, "/register"),
        "uname": "admintest",
        "email": "admintest@gmail.com",
        "passw": "tester@123",
        "confirm_passw": "tester@123"
    })

    # Login
    response = client.post("/login", data={
        "csrf_token": get_csrf_token(client, "/login"),
        "uname": "admintest",
        "passw": "tester@123"
    })

    # Create a post
    response = client.post("/post/new", data={
        "csrf_token": get_csrf_token(client, "/post/new"),
        "title": "test post",
        "content": "Lorem ipsum dolor sit ametem aliquam ut quibusdam illo"
    }, follow_redirects=True)

    # Check if the post is created
    with app.app_context():
        user = User.query.filter_by(username="admintest").first()
        post = Post.query.filter_by(user_id=user.id).first()
        assert post.title == "test post"

    # Delete the post
    response = client.post(f"/post/{post.id}/delete", follow_redirects=True)
    with app.app_context():
        post = Post.query.filter_by(user_id=user.id).first()
        assert post is None
        assert response.status_code == 200
    #testing account route
    response = client.get('/account')
    assert response.status_code == 200
    
def test_routes(client):
    response = client.get('/home')
    assert response.status_code == 200
    response = client.get('/about')
    assert response.status_code == 200