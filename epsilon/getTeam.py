from flask import Flask, request, render_template
from DAO import DAO

# EP-2: Display Team
def getTeam(tid, dao):
    q = "With temp as (Select Users.uid, Users.name, Users.contact,Users.rid, Roles.type from Users inner join Roles on Users.rid=Roles.rid) Select temp.name, temp.type, temp.contact, temp.uid, Teams.tid,temp.rid from temp, Teams where Teams.uid=temp.uid and Teams.tid="+str(tid)
    # q = "With temp as (Select Users.uid, Users.name,Roles.type from Users inner join Roles on Users.rid=Roles.rid) Select temp.name, temp.type from temp, Teams where Teams.uid=temp.uid and Teams.tid="+str(tid)
    team = dao.get_data(q, None)
    if team:  # there are values in the database
        userDetails = team
        return render_template('displayteam.html', userDetails=userDetails)
    else:
        message = "Your team does not exist"
        return render_template('displayteam.html', message=message)
