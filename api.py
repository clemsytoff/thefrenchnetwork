from flask import Flask, jsonify, request,render_template
import mysql.connector
import bcrypt
import secrets,base64

app = Flask(__name__)
# Configuration de la base de données   ----------- TOUT EST EN LOCAL HOST, IL FAUDRA ADAPTER POUR UNE DB EN LIGNE CHEZ HEXAHOST.FR
db = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 database="jbs_network"
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





#                                                           CREATIONS
# Ajouter un utilisateur
@app.route("/api/v1/public/users", methods=["POST"])
def add_user():
    data = request.json
    pseudo = data.get("pseudo")
    name = data.get("name")
    surname = data.get("surname")
    email = data.get("email")
    birth = data.get("birth")
    password = data.get("password")
    grade = data.get("grade")
    status = data.get("status")
    
    if not (pseudo and name and surname and email and birth and password and grade and status):
        return jsonify({"error": "All fields are required"}), 400

    cursor.execute("INSERT INTO users (pseudo, name, surname, email, birth, password, grade, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (pseudo, name, surname, email, birth, password, grade, status))
    db.commit()
    return jsonify({"message": "User added successfully"}), 201

# Ajouter un post
@app.route("/api/v1/public/posts", methods=["POST"])
def add_post():
    data = request.json
    user_id = data.get("user_id")
    content = data.get("content")

    if not content or not user_id:
        return jsonify({"error": "User ID and content are required"}), 400

    cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, content))
    db.commit()
    return jsonify({"message": "Post added successfully"}), 201

# Ajouter un follow
@app.route("/api/v1/public/follows", methods=["POST"])
def add_follow():
    data = request.json
    follower_id = data.get("follower_id")
    followed_id = data.get("followed_id")

    if not follower_id or not followed_id:
        return jsonify({"error": "Follower ID and Followed ID are required"}), 400

    cursor.execute("INSERT INTO follows (follower_id, followed_id) VALUES (%s, %s)", (follower_id, followed_id))
    db.commit()
    return jsonify({"message": "Follow added successfully"}), 201

# Ajouter un commentaire
@app.route("/api/v1/public/comments", methods=["POST"])
def add_comment():
    data = request.json
    post_id = data.get("post_id")
    user_id = data.get("user_id")
    content = data.get("content")

    if not post_id or not user_id or not content:
        return jsonify({"error": "Post ID, User ID, and Content are required"}), 400

    cursor.execute("INSERT INTO comments (post_id, user_id, content) VALUES (%s, %s, %s)", (post_id, user_id, content))
    db.commit()
    return jsonify({"message": "Comment added successfully"}), 201

# Ajouter un like
@app.route("/api/v1/public/likes", methods=["POST"])
def add_like():
    data = request.json
    post_id = data.get("post_id")
    user_id = data.get("user_id")

    if not post_id or not user_id:
        return jsonify({"error": "Post ID and User ID are required"}), 400

    cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (post_id, user_id))
    db.commit()
    return jsonify({"message": "Like added successfully"}), 201

# Ajouter une certification
@app.route("/api/v1/admin/certified", methods=["POST"])
def add_certification():
    data = request.json
    user_id = data.get("user_id")
    reason = data.get("reason")

    if not user_id or not reason:
        return jsonify({"error": "User ID and reason are required"}), 400

    cursor.execute("INSERT INTO certified (user_id, reason) VALUES (%s, %s)", (user_id, reason))
    db.commit()
    return jsonify({"message": "Certification added successfully"}), 201

# Ajouter un report
@app.route("/api/v1/public/reports", methods=["POST"])
def add_report():
    data = request.json
    reporter_id = data.get("reporter_id")
    reported_user_id = data.get("reported_user_id")
    reported_post_id = data.get("reported_post_id")
    reported_comment_id = data.get("reported_comment_id")
    reason = data.get("reason")

    if not reporter_id or not reason:
        return jsonify({"error": "Reporter ID and reason are required"}), 400

    cursor.execute("INSERT INTO reports (reporter_id, reported_user_id, reported_post_id, reported_comment_id, reason) VALUES (%s, %s, %s, %s, %s)", 
                   (reporter_id, reported_user_id, reported_post_id, reported_comment_id, reason))
    db.commit()
    return jsonify({"message": "Report added successfully"}), 201

# Ajouter un ban
@app.route("/api/v1/admin/bans", methods=["POST"])
def add_ban():
    data = request.json
    user_id = data.get("user_id")
    moderator_id = data.get("moderator_id")
    reason = data.get("reason")

    if not user_id or not moderator_id or not reason:
        return jsonify({"error": "User ID, Moderator ID, and reason are required"}), 400

    cursor.execute("INSERT INTO bans (user_id, moderator_id, reason) VALUES (%s, %s, %s)", (user_id, moderator_id, reason))
    db.commit()
    return jsonify({"message": "User banned successfully"}), 201

# Ajouter un avertissement (warn)
@app.route("/api/v1/admin/warns", methods=["POST"])
def add_warn():
    data = request.json
    user_id = data.get("user_id")
    moderator_id = data.get("moderator_id")
    reason = data.get("reason")

    if not user_id or not moderator_id or not reason:
        return jsonify({"error": "User ID, Moderator ID, and reason are required"}), 400

    cursor.execute("INSERT INTO warns (user_id, moderator_id, reason) VALUES (%s, %s, %s)", (user_id, moderator_id, reason))
    db.commit()
    return jsonify({"message": "Warning added successfully"}), 201





#                                               SUPPRESSION
# Suppression d'un utilisateur
@app.route("/api/v1/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Suppression d'un post
@app.route("/api/v1/admin/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    db.commit()
    return jsonify({"message": "Post deleted successfully"}), 200

# Modification d'un utilisateur
@app.route("/api/v1/admin/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = request.json
    pseudo = data.get("pseudo")
    name = data.get("name")
    surname = data.get("surname")
    email = data.get("email")
    birth = data.get("birth")
    grade = data.get("grade")
    status = data.get("status")
    
    cursor.execute("""
        UPDATE users 
        SET pseudo=%s, name=%s, surname=%s, email=%s, birth=%s, grade=%s, status=%s 
        WHERE id=%s
    """, (pseudo, name, surname, email, birth, grade, status, user_id))
    db.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Modification d'un post
@app.route("/api/v1/admin/posts/<int:post_id>", methods=["PUT"])
def edit_post(post_id):
    data = request.json
    content = data.get("content")
    
    cursor.execute("UPDATE posts SET content=%s WHERE id=%s", (content, post_id))
    db.commit()
    return jsonify({"message": "Post updated successfully"}), 200






#NE PAS TOUCHER
if __name__ == "__main__":
    app.run(debug=True)