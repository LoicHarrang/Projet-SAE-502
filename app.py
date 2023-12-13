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

def create_projects_from_csv(csv_file, assign_users_if_exist=False):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Vérifier si les colonnes nécessaires sont présentes dans le fichier CSV
        required_columns = {'name', 'description'}
        if not required_columns.issubset(reader.fieldnames):
            print("Erreur: Les colonnes nécessaires ne sont pas présentes dans le fichier CSV.")
            return

        for row in reader:
            project_name = row['name']
            project_description = row['description']

            # Créer le projet avec la possibilité d'affecter les utilisateurs s'il existe déjà
            create_project(project_name, project_description, assign_users_if_exist)


def create_project(project_name, project_description, assign_users_if_exists=False):
    # Récupération de la liste de tous les projets
    all_projects = gl.projects.list(all=True)

    # Vérification de l'existence du projet par nom
    existing_project = next((project for project in all_projects if project.name == project_name), None)

    # Si le projet existe déjà
    if existing_project:
        print(f"Le projet {project_name} existe déjà.")

        # Affectation de tous les utilisateurs au projet si l'option est activée
        if assign_users_if_exists:
            assign_all_users_to_projects()

        return

    # Création du projet
    project_attributes = {
        'name': project_name,
        'description': project_description,
        'visibility': 'public',  # Vous pouvez ajuster la visibilité selon vos besoins (public, internal, private)
    }
    project = gl.projects.create(project_attributes)
    print(f"Projet {project_name} créé avec succès.")

    # Affectation de tous les utilisateurs au projet
    assign_all_users_to_projects()

def assign_all_users_to_projects():
    # Mapping des groupes aux projets
    group_project_mapping = {
        'A1': 'projet1',
        'A2': 'projet1',
        'B1': 'projet2',
        'B2': 'projet2',
        'C1': 'projet3',
        'C2': 'projet3',
    }

    # Récupération de la liste de tous les utilisateurs GitLab
    all_users = gl.users.list(all=True)

    for group_name, project_name in group_project_mapping.items():
        # Récupération ou création du groupe
        group = get_or_create_group(group_name)

        if group:
            # Récupération du projet
            project = get_or_create_project(project_name)

            # Vérification si le projet existe
            if project:
                # Récupération des membres du groupe
                group_members = set(member.username for member in group.members.list())

                # Affectation des membres au projet avec l'accès approprié
                for user in all_users:
                    if user.username in group_members:
                        access_level = 30  # Access level 30 correspond à l'accès complet, ajustez selon vos besoins

                        # Affectation de l'utilisateur au projet
                        try:
                            project.members.create({'user_id': user.id, 'access_level': access_level})
                            print(f"Utilisateur {user.username} ajouté au groupe {group_name} et au projet {project_name} avec succès.")
                        except Exception as e:
                            if '409 Member already exists' in str(e):
                                print(f"Utilisateur {user.username} est déjà membre du projet {project_name}.")
                            else:
                                print(f"Erreur lors de l'ajout de l'utilisateur {user.username} au projet {project_name}: {str(e)}")
            else:
                print(f"Le projet {project_name} n'existe pas.")
        else:
            print(f"Le groupe {group_name} n'existe pas.")

def get_or_create_group(group_name):
    try:
        # Tentative de récupération du groupe
        group = gl.groups.get(group_name)
    except Exception as e:
        # Le groupe n'existe pas, le crée
        group = gl.groups.create({'name': group_name, 'path': group_name})

    return group

def get_or_create_project(project_name):
    project_name = "root/"+ project_name
    try:
        # Tentative de récupération du projet
        project = gl.projects.get(project_name)
        return project
    except Exception as e:
        # Le projet n'existe pas
        print(f"Erreur lors de la récupération du projet {project_name}: {str(e)}")
        return None



def main():
    # with open('utilisateurs.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
        
    #     # Vérifier si les colonnes nécessaires sont présentes dans le fichier CSV
    #     required_columns = {'utilisateur', 'prenom', 'nom', 'groupe'}
    #     if not required_columns.issubset(reader.fieldnames):
    #         print("Erreur: Les colonnes nécessaires ne sont pas présentes dans le fichier CSV.")
    #         return

    #     for row in reader:
    #         create_user(row['utilisateur'], row['prenom'], row['nom'], row['groupe'])
    #         print(f"Utilisateur {row['utilisateur']} créé avec succès dans le groupe {row['groupe']}.")
        
    
    create_projects_from_csv("projects.csv", assign_users_if_exist=True)
    
    # Modification des droits de l'utilisateur
    #modify_user_access(new_user.id, gitlab.const.AccessLevel.MAINTAINER)


if __name__ == '__main__':
    main()