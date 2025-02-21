from flask import Flask, jsonify, request,render_template
import mysql.connector
import bcrypt
import secrets,base64
from flask_cors import CORS
import jwt
import datetime
from config import SECRET_KEY  # Assure-toi d'avoir une clé secrète pour signer le JWT


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
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
    pseudo = data.get("pseudo") #50 caracteres max
    nom = data.get("nom") #500 caracteres max
    prenom = data.get("prenom") #500 caracteres max
    email = data.get("email") #800 caracteres max
    birth = data.get("birth") #YYYY-MM-DD
    password = data.get("password")
    #password_confirm = data.get("password_confirm")
    if not pseudo or not nom or not prenom or not email or not birth or not password:# or not password_confirm:
        return jsonify({"error": "Veuillez remplir tous les champs"}), 400
    #if password != password_confirm:
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






#                                                                                       CONNEXION / DECO

#login
@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    userdata = request.json
    user = userdata.get("user")
    password = userdata.get("password")

    if not user or not password:
        return jsonify({"error": "Veuillez remplir tous les champs"}), 400
    cursor.execute("SELECT id, password, valide FROM users WHERE email = %s", (user,))
    maildata = cursor.fetchone()
    if not maildata:
        cursor.execute("SELECT id, password, valide FROM users WHERE pseudo = %s", (user,))
        pseudodata = cursor.fetchone()
    else:
        pseudodata = None
    if not maildata and not pseudodata:
        return jsonify({"error": "Identifiants incorrects"}), 400
    userdata = maildata if maildata else pseudodata
    user_id, hashed_password, valide = userdata 

    # Vérification du mot de passe
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return jsonify({"error": "Mot de passe incorrect"}), 401

    # Génération d'un token sécurisé
    session_token = secrets.token_hex(32)  # Génère un token unique sécurisé

    # Insérer le token dans la base de données
    cursor.execute("INSERT INTO tokens (token, user_id) VALUES (%s, %s)", (session_token, user_id))
    db.commit() 

    # Génération d'un token JWT pour sécuriser la session
    jwt_token = jwt.encode(
        {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Connexion réussie",
        "valide": valide,
        "session_token": session_token,
        "jwt_token": jwt_token
    }), 200



#NE PAS TOUCHER - FIN DU CODE DE TEST, retirer à la prod
if __name__ == "__main__":
    app.run(debug=True)