from flask import Flask, jsonify, request,render_template
import mysql.connector
import bcrypt
import secrets,base64

app = Flask(__name__)
# Configuration de la base de données
db = mysql.connector.connect(
 host="193.22.129.72",
 user="u8_Bnz4UxnN9K",
 password="s6GBVFQ9v=23Tzh.eUaPWtT5",
 database="s8_network_social"
)
cursor = db.cursor()



#                                               LISTES
#liste utilisateurs
@app.route("/api/v1/admin/users", methods=["GET"])
def get_users_list():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    users = [{"id": row[0], "pseudo": row[1], "name": row[2], "surname": row[3], "email": row[4], "birth": row[5], "account creation": row[7], "grade": row[8], "account satus": row[9]} for row in data]
    return jsonify(users)

#liste posts
@app.route("/api/v1/admin/posts", methods=["GET"])
def get_posts_list():
    cursor.execute("SELECT * FROM posts")
    data = cursor.fetchall()
    posts = [{"id": row[0], "user": row[1], "content": row[2], "date": row[3]} for row in data]
    return jsonify(posts)

#liste follows
@app.route("/api/v1/admin/follows", methods=["GET"])
def get_follows_list():
    cursor.execute("SELECT * FROM follows")
    data = cursor.fetchall()
    follows = [{"follower": row[0], "followed": row[1], "date": row[2]} for row in data]
    return jsonify(follows)

#liste comments
@app.route("/api/v1/admin/comments", methods=["GET"])
def get_comments_list():
    cursor.execute("SELECT * FROM comments")
    data = cursor.fetchall()
    comments = [{"id": row[0], "post": row[1], "content": row[2], "date": row[3]} for row in data]
    return jsonify(comments)

#liste likes
@app.route("/api/v1/admin/likes", methods=["GET"])
def get_likes_list():
    cursor.execute("SELECT * FROM likes")
    data = cursor.fetchall()
    likes = [{"user": row[1], "post": row[2], "date": row[3]} for row in data]
    return jsonify(likes)

#liste certified
@app.route("/api/v1/admin/certified", methods=["GET"])
def get_certified_list():
    cursor.execute("SELECT * FROM certified")
    data = cursor.fetchall()
    certified = [{"user": row[0], "date": row[1], "reason": row[2]} for row in data]
    return jsonify(certified)

#liste reports
@app.route("/api/v1/admin/reports", methods=["GET"])
def get_reports_list():
    cursor.execute("SELECT * FROM reports")
    data = cursor.fetchall()
    reports = [{"id": row[0], "reporter": row[1], "reported user": row[2], "reported post": row[3], "reported comment": row[4], "reason": row[5], "date": row[6], "status": row[7]} for row in data]
    return jsonify(reports)

#liste bans
@app.route("/api/v1/admin/bans", methods=["GET"])
def get_bans_list():
    cursor.execute("SELECT * FROM bans")
    data = cursor.fetchall()
    bans = [{"id": row[0], "user": row[1], "moderator": row[2], "reason": row[3], "date": row[4]} for row in data]
    return jsonify(bans)

#liste warns
@app.route("/api/v1/admin/warns", methods=["GET"])
def get_warns_list():
    cursor.execute("SELECT * FROM warns")
    data = cursor.fetchall()
    warns = [{"id": row[0], "user": row[1], "moderator": row[2], "reason": row[3], "date": row[4]} for row in data]
    return jsonify(warns)



#                                                                                                   CREATE

#créer un utilisateur - verif good
@app.route("/api/v1/public/user", methods=["POST"])
def add_user():
    data = request.json
    pseudo = data.get("pseudo").replace(" ", "") #50 caracteres max
    nom = data.get("nom").replace(" ", "") #500 caracteres max
    prenom = data.get("prenom").replace(" ", "") #500 caracteres max
    email = data.get("email").replace(" ", "") #800 caracteres max
    birth = data.get("birth").replace(" ", "") #YYYY-MM-DD
    password = data.get("password").replace(" ", "")
    password_confirm = data.get("password_confirm").replace(" ", "")
    if not pseudo or not nom or not prenom or not email or not birth or not password or not password_confirm:
        return jsonify({"error": "Veuillez remplir tous les champs"}), 400
    if password != password_confirm:
        return jsonify({"error": "Les mots de passe ne correspondent pas."}), 400
    if not (0<=len(pseudo)<=50):
        return jsonify({"error": "Le nom d'utilisateur est trop long."}), 400
    if not (0<=len(nom)<=500):
        return jsonify({"error": "Le nom est trop long."}), 400
    if not (0<=len(prenom)<=500):
        return jsonify({"error": "Le prénom est trop long."}), 400
    if not (0<=len(email)<=800):
        return jsonify({"error": "L'email est trop long."}), 400
    # Générer un sel et hacher le mot de passe
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    cursor.execute("INSERT INTO users (pseudo,name,surname,email,birth,password,grade) VALUES (%s,%s,%s,%s,%s,%s,%s)", (pseudo,nom,prenom,email,birth,hashed_password,"0",))
    db.commit()
    return jsonify({"message": "Utilisateur créé avec succès"}), 201






#NE PAS TOUCHER - FIN DU CODE DE TEST, retirer à la prod
if __name__ == "__main__":
    app.run(debug=True)