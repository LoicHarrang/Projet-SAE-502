import gitlab
import csv

# Configuration de l'URL et du token d'authentification GitLab
gitlab_url = 'http://10.254.200.172:7575/'
gitlab_token = 'glpat-_yiVys2hzu-uXnMstmqk'

# Initialisation du client GitLab
gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)

# Fonction pour créer un nouvel utilisateur
def create_user(username, first_name, last_name, group_name):
    # Générer une adresse e-mail
    email = f'{username}@example.com'

    # Vérification de l'existence de l'utilisateur par adresse e-mail
    existing_users = gl.users.list(search=email)
    
    # Si des utilisateurs existent avec la même adresse e-mail, affiche un message et retourne
    if existing_users:
        print(f"L'utilisateur avec l'adresse e-mail {email} existe déjà.")
        return

    # Recherche du groupe existant
    groups = gl.groups.list(all=True)
    existing_group = next((group for group in groups if group.name == group_name), None)

    # Si le groupe n'existe pas, le crée
    if not existing_group:
        group = gl.groups.create({'name': group_name, 'path': group_name})
    else:
        group = existing_group

    # Création de l'utilisateur
    user_attributes = {
        'username': username,
        'name': f'{first_name} {last_name}',
        'email': email,
        'password': 'Lannion1',  # Vous pouvez définir un mot de passe plus sécurisé
        'skip_confirmation': True,
    }
    user = gl.users.create(user_attributes)

    # Ajout de l'utilisateur au groupe
    group.members.create({'user_id': user.id, 'access_level': 30})  # Access level 30 correspond à l'accès complet
    print(f"Utilisateur {username} créé avec succès dans le groupe {group_name}.")


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


def main():
    with open('utilisateurs.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Vérifier si les colonnes nécessaires sont présentes dans le fichier CSV
        required_columns = {'utilisateur', 'prenom', 'nom', 'groupe'}
        if not required_columns.issubset(reader.fieldnames):
            print("Erreur: Les colonnes nécessaires ne sont pas présentes dans le fichier CSV.")
            return

        for row in reader:
            create_user(row['utilisateur'], row['prenom'], row['nom'], row['groupe'])
            print(f"Utilisateur {row['utilisateur']} créé avec succès dans le groupe {row['groupe']}.")
        
    
    
    # Modification des droits de l'utilisateur
    #modify_user_access(new_user.id, gitlab.const.AccessLevel.MAINTAINER)


if __name__ == '__main__':
    main()