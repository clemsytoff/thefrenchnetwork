# The Social Network

## Description

The Social Network est une plateforme sociale développée avec Flask, Python, SQL, HTML, CSS et JavaScript. Ce projet permet aux utilisateurs de se connecter, de publier du contenu, d'interagir avec les autres membres et de gérer leur profil.

## Technologies utilisées

Backend : Flask (Python)

Base de données : SQL (SQLite/MySQL/PostgreSQL selon configuration)

Frontend : HTML, CSS, JavaScript

Authentification : Flask-Login, Flask-WTF

## Fonctionnalités principales

Inscription et connexion des utilisateurs

Création et modification de profils

Publication de posts et interaction avec les publications (like, commentaire)

Système de suivi entre utilisateurs (follow/unfollow)

Fil d'actualité personnalisé

Notifications en temps réel

## Installation

### Prérequis

Python 3.x installé

Un environnement virtuel (recommandé)

Un gestionnaire de base de données compatible (SQLite, MySQL, PostgreSQL...)

Clonez le dépôt :

git clone https://github.com/clemsytoff/thesocialnetwork

Créez un environnement virtuel et activez-le :

python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

Configurez la base de données :

flask db init
flask db migrate
flask db upgrade

Lancez l'application :

flask run

Accédez à l'application dans votre navigateur :
http://127.0.0.1:5000

## Contribution
Les contributions sont les bienvenues !

Forkez le projet

Créez une branche (git checkout -b feature-nouvelle-fonction)

Commitez vos changements (git commit -m 'Ajout d'une nouvelle fonctionnalité')

Poussez votre branche (git push origin feature-nouvelle-fonction)

Ouvrez une Pull Request

N'oubliez pas de mettre une étoile !

## Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## Contact
Pour toute question ou suggestion, contactez-moi par email : clement@hexahost.fr

## Remerciements
Un grand merci à DeletedUser et Alo_59 de m'avoir aidé sur ce projet, sans eux il ne serait jamais arrivé là où il en est aujourd'hui.
