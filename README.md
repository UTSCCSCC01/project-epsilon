<h1 align="center">Project Epsilon</h1>

## About the project
With project epsilon we aim to enable young african entrpeneurs to build companies using a marketplace platform. Making things such as hiring talent, applying for grants, and company management easy and accessible for those wanting to take the oppurtunity to create a successful business.

## Project setup
Follow these instructions to run the project after cloning locally:
1. Install [MySQL installer](https://dev.mysql.com/downloads/installer/) and install MySQL Server 8.0.25
    1. Set the MySQL root password as: 12345
    2. Create a DB Admin user with these credentials: u: epsilon p: 12345
2. At root, create a virtual environment with these [instructions](https://tutorial.djangogirls.org/en/django_installation/) and activate it.
3. Run `pip install -r requirements.txt` to install all requirements to your virtual environment.
4. Run `mysql -u epsilon -p` and type in the password when prompted.
    1. Run `CREATE DATABASE epsilon_db CHARACTER SET utf8;` to create the local database.
    2. Run `exit`.
5. Inside epsilon folder, run `py manage.py migrate`.
6. Inside epsilon folder, run `py manage.py runserver`.
7. Go to [localhost](http://localhost:8000/) and check you can view the landing page.

To manage the database from the django admin page, these credentials will be needed
django superuser:
- username: epsilon 
- password: BestProjectC01
(for now it is safe to put these credentials here since the repo is private to students in CSCC01)
  
For general django inquiries and instructions follow [this](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) documentation.
For mysql connection follow [this](https://dev.mysql.com/doc/connector-python/en/) documentation.

## Contributing to the project
For project epsilon we are using github as our version control. Whenever a change is made that is more than 10 lines or is not a bug fix, a pull request should be made. Branch names will be the same as their associated ticket on Jira.

All tickets will be created on Jira to assign work to any given member of the project.

Finally, members will use Figma to create all mockups

For team details, go to [doc/sprint0/team.md](doc/sprint0/team.md)
