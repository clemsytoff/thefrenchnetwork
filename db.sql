create table users(
    id int not null AUTO_INCREMENT primary key,
    pseudo varchar(50) not null,
    name varchar(500) not null,
    surname varchar(500) not null,
    email varchar(800) not null,
    birth date not null,
    password text not null,
    account_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    grade text not null,
    status varchar(100) not null
);

CREATE TABLE posts(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content text(2011) NOT NULL,
    date_post TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

create table follows(
    follower_id INT NOT NULL,
    followed_id INT NOT NULL,
    date_follow TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES users(id) ON DELETE CASCADE
);

create table comments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    content TEXT NOT NULL,
    date_comment TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE likes (
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    date_like TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE certified (
    user_id INT PRIMARY KEY,
    date_certification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE reports(
    id INT AUTO_INCREMENT PRIMARY KEY,
    reporter_id INT NOT NULL,  
    reported_user_id INT,      
    reported_post_id INT,      
    reported_comment_id INT,   
    reason TEXT(4000) NOT NULL,      
    date_report TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'reviewed', 'action_taken') DEFAULT 'pending',
    FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_comment_id) REFERENCES comments(id) ON DELETE CASCADE
);


CREATE TABLE bans(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    moderator_id INT NOT NULL,  
    reason TEXT(4000) NOT NULL,
    ban_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (moderator_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE warns(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    moderator_id INT NOT NULL, 
    reason TEXT(4000) NOT NULL,
    date_warn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (moderator_id) REFERENCES users(id) ON DELETE CASCADE
);
