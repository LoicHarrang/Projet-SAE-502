import gitlab
import csv

# Configuration de l'URL et du token d'authentification GitLab
gitlab_url = 'http://10.254.200.172:7575/'
gitlab_token = 'glpat-_yiVys2hzu-uXnMstmqk'

# Initialisation du client GitLab
gl = gitlab.GitLab(gitlab_url, private_token=gitlab_token)

# Fonction pour créer un nouvel utilisateur
def create_user(username, email, password):
    user_data = {
        'username': username,
        'email': email,
        'password': password,
        'reset_password': True
    }
    user = gl.users.create(user_data)
    return user

# Fonction pour modifier les droits d'un utilisateur
def modify_user_access(user_id, access_level):
    user = gl.users.get(user_id)
    user.access_level = access_level
    user.save()

# Fonction pour créer un projet
def create_project(name, description):
    project_data = {
        'name': name,
        'description': description,
        'visibility': 'public'
    }
    project = gl.projects.create(project_data)
    return project

# Fonction pour affecter un utilisateur à un projet en tant que membre
def assign_user_to_project(user_id, project_id, access_level):
    project = gl.projects.get(project_id)
    project.members.create({'user_id': user_id, 'access_level': access_level})

# Fonction principale
def main():
 # Création d'un nouvel utilisateur
    new_user = create_user('nouvel_utilisateur', 'nouvel_utilisateur@example.com', 'mot_de_passe')

 # Modification des droits de l'utilisateur
    modify_user_access(new_user.id, gitlab.Access.MAINTAINER)

 # Lecture d'un fichier CSV pour créer des projets et affecter des utilisateurs
 #with open('projets_utilisateurs.csv', 'r') as csvfile:
 #csvreader = csv.reader(csvfile)
 #for row in csvreader:
 #project_name, project_description, username, access_level = row
 #project = create_project(project_name, project_description)
 #user = gl.users.get(username)
 #assign_user_to_project(user.id, project.id, access_level)

if __name__ == '__main__':
 main()