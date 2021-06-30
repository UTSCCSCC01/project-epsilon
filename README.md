<h1 align="center">Project Epsilon</h1>

## About the project
With project epsilon we aim to enable young african entrpeneurs to build companies using a marketplace platform. Making things such as hiring talent, applying for grants, and company management easy and accessible for those wanting to take the oppurtunity to create a successful business.

## Project setup
Follow these instructions to run the project after cloning locally:
1. Install [MySQL installer](https://dev.mysql.com/downloads/installer/) and install MySQL Server 8.0.25
    1. Set the MySQL root password as: 12345
    2. Create a DB Admin user with these credentials: u: epsilon p: 12345
2. At root, create a virtual environment with these commands on your terminal [instructions]:
    1. Run `python3 -m venv venv`
    2. If your os is OS X or Linux run `source venv/bin/activate`, if your os is Windows run `venv\Scripts\activate`
    3. Run `pip3 install -r requirements.txt`
4. Run `mysql -u epsilon -p` and type in the password when prompted.
    1. Run `CREATE DATABASE epsilon_db CHARACTER SET utf8;` to create the local database.
    2. Run `exit`.
4. Run `python3 app.py` and go to the link provided in the terminal to view the webapp. (the same can be achieved by step 7)

## Additional react setup
5. in project-epsilon, run `pip install -r requirements.txt`
6. (if you have installed node please go to 7)
    download and install node from [official page](https://nodejs.org/en/), choose 14.17.1
7. verify installation by running all of `npm --version`, `npx --version`, `yarn --version`, ` node --version`.
    (windows user: if any error occurs please verify nodejs installation path is in your system env variables, tho step 5 has done this already)
8. to verify nodejs can connect to the flask application, cd into project-epsilon/epsilon, run `npm run start-flask-api`,
   expected to see our original landing page.
9. with 8 still running, to verify that backend communicates with front end, cd into project-epsilon/epsilon, run `npm start`, expected to see "I am ready from app.py".(it's an headline, not a json string) 
   (If it gives an error saying "XXX is not recognized as an internal or external command,operable program or batch file", try running `npm install`, and rerun `npm start`)

## Note
To manage the database use a third party GUI tool with the credentials above to view/edit.
(for now it is safe to put these credentials here since the repo is private to students in CSCC01)
  
For general flask inquiries and instructions follow [this](https://flask.palletsprojects.com/en/2.0.x/installation/) documentation.
For mysql connection follow [this](https://flask-mysqldb.readthedocs.io/en/latest/) documentation.

## Contributing to the project
For project epsilon we are using github as our version control. Whenever a change is made that is more than 10 lines or is not a bug fix, a pull request should be made. Branch names will be the same as their associated ticket on Jira.

All tickets will be created on Jira to assign work to any given member of the project.

Finally, members will use Figma to create all mockups

For team details, go to [doc/sprint0/team.md](doc/sprint0/team.md)
For documentation of the project, go to [SwaggerHub for project Epsilon](https://app.swaggerhub.com/apis/epsilonc01/epsilon/1.0.0)
