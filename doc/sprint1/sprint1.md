# Sprint 1
## Meeting Goal
Decide on the goals for sprint one and divide the tasks between the team members depending on their complexity and time availability. Another goal is to finish defining the technical stack for the project to start working on it.

## Sprint Goal
**Goal**:
- Complete the environment setup of the project including the basic flask project structure and mySQL local server
- Complete the backend of the team management page where teams can add, remove, promote, and see a list of their members, users can send requests to join.
- Have a functional frontend of the team management page, not necessarily yet stylized for the final delivery, that displays and reacts to the user’s request. The frontend will be done in React.

**Team Capacity** = 11 + 10 + 11 + 12 + 18 + 10 + 12 = 84 total hours

## Spikes
### Functional
Practice merging pull requests successfully with multiple branches that touch the same files.
### Technical
Test flask-mysqldb python works well for our project by using it to build the team management database.

## Stories in this sprint
### EP - 1
Title: As a team administrator, I want to create a team so that I can define who makes up the company.
Assignee: Hritik Gandhi
Sub-tasks:
Establish MySQL Database for Team Management
Create front end form to create team

### EP - 2
Title: As a team administrator, I want to be able to see a list of the members of the team, their roles, and their contact information to be able to keep track and connect with them.
Assignee: Sarah Hameed
Sub-tasks:
Create database for team members
Create front end module

### EP - 3
Title: As a team administrator, I would like to accept or decline requests of other users who want to join the team to make sure only real employees have the company in their profile.
Assignee: Kobe Louis and Artina Sin
Sub-tasks:
Push Notifications
Catch new updates to list
Add pending users to SQL
Create Accept and Deny buttons 
Create list of pending employees to front end

### EP - 4
Title: As a team administrator, I would like to remove members to only include current employees.
Assignee: Corey Fung
Sub-tasks:
Back end functionality to remove user and update database
Create front end button to remove users

### EP - 5
Title: As a team administrator, I would like to promote members (employees) from normal members to team administrators to give them access to team administrator features.
Assignee: Weiyu Li
Sub-tasks:
Backend integration to change role in database
Front end button creations

### EP - 52
Title: Transition from Django to Flask as advised by Scrum Leader
Assignee: Hritik Gandhi
Sub-tasks:
Change requirements to reflect the new venv setup.
Change README to reflect how flask works.

This ticket was done, however, after the project demo with the TA on tuesday, we realized we had to change our tech stack and not use django anymore.
### EP - 28
Title: As a developer I want to have the dev environment setup so that I can start creating the project.
Assignee: Daniela Venturo
Sub-tasks:
Django Setup
Basic frontend folder structure setup
SQL dependency setup
