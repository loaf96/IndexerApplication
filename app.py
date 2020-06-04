from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
    
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/deats.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class AllInfo(db.Model):
    __tablename__ = 'detailed_placesInfo'
    __table_args__ = { 'extend_existing': True }
    placeID = db.Column(db.String, primary_key=True)   
    name = db.Column(db.String)
    website = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.String)
    rating = db.Column(db.String)
    user_ratings_total = db.Column(db.String)
    
@app.route("/")
def homepage():
    totalnumber = f'{AllInfo.query.count():,}'
    print(totalnumber)
    return render_template("index.html", info=totalnumber)

@app.route('/output', methods= ['POST', 'GET'])
def selectstate():
    totalnumber = f'{AllInfo.query.count():,}'
    dsrd_state = AllInfo.query.all()
    choiceids = ['STATE', 'STATE AND CITY', 'STATE AND ZIPCODE', 'BUSINESS NAME']
    datag = request.form.get('type1')
    if datag == 'und':
        return render_template('srchby.html', info = totalnumber, dachoice=choiceids[3]\
            , woState='Y', srch='Y')
    elif bool(datag=='und') == False:
        clncln = list(set([x.state for x in dsrd_state]))
        sofrsh = []
        for x in clncln:
            try:
                if len(x) == 2:
                    sofrsh.append(x)
            except:
                'TypeError'
        if datag == 'una':
            return render_template('srchby.html', info = totalnumber\
            , dsrdstate = sorted(sofrsh), onlystate=[{'Make selection to view data'}], stateoutput=True\
                , dachoice=choiceids[0], srch='Y')
        elif datag == 'unb':
            return render_template('srchby.html', info = totalnumber\
            , dsrdstate = sorted(sofrsh), withcity='Y', dachoice=choiceids[1].split(' ')[-1], withState='Y', srch='Y')
        elif datag == 'unc':
            return render_template('srchby.html', info = totalnumber\
            , dsrdstate = sorted(sofrsh), zapazip='Y', dachoice=choiceids[2].split(' ')[-1]\
                , withState='Y', srch='Y')
                
@app.route('/search', methods=['GET', 'POST'])
def srchbystate():
    type11 = request.form.get('pikachu')
    type13 = request.form.get('daName')
    if bool(type13) == True:
        lookitup = AllInfo.query.filter_by(name=type13).all()
        quien = ['NAME :', 'ADDRESS :' , 'CITY :', 'ZIPCODE :', 'AVERAGE RATING :', 'USER RATING TOTAL :'\
        , 'STATE :  ', 'WEBSITE :  ']
        que = [[f' #{lookitup.index(x)+1}', f'{quien[0]}  {x.name}', f'{quien[7]} {x.website}', f'{quien[1]}  {x.street_addr}'\
        , f'{quien[2]} {x.city}', f'{quien[6]} {x.state}', f'{quien[3]}  {x.zipcode}', f'{quien[4]}  {x.rating}'\
            , f'{quien[5]}  {x.user_ratings_total}'] for x in lookitup]
        if type(que[0]) != type(list()):
            que = list(que)
            return render_template('rowsults.html', datinfo=que, dachoice=type13\
            , numba=range(1, len(que)), info=len(que))
        else:
            return render_template('rowsults.html', datinfo=que, dachoice=type13\
            , numba=range(1, len(que)), info=len(que))
    type12 = request.form.get('whtelse')
    if bool(type12) == True:
        try:
            int(type12)
            lookitup = AllInfo.query.filter_by(state=type11, zipcode=type12).all()    
            quien = ['NAME :', 'ADDRESS :' , 'CITY :', 'ZIPCODE :', 'AVERAGE RATING :', 'USER RATING TOTAL :'\
            , 'STATE :  ', 'WEBSITE :  ']
            que = [[f' #{lookitup.index(x)+1}', f'{quien[0]}  {x.name}', f'{quien[7]} {x.website}', f'{quien[1]}  {x.street_addr}'\
            , f'{quien[2]} {x.city}', f'{quien[6]} {x.state}', f'{quien[3]}  {x.zipcode}', f'{quien[4]}  {x.rating}'\
                , f'{quien[5]}  {x.user_ratings_total}'] for x in lookitup]
            return render_template('rowsults.html', datinfo=que, dachoice=type12+', '+type11\
            , numba=range(1, len(que)), info=len(que))
        except:
            'ValueError'
            lookitup = AllInfo.query.filter_by(state=type11, city=type12).all()    
            quien = ['NAME :', 'ADDRESS :' , 'CITY :', 'ZIPCODE :', 'AVERAGE RATING :', 'USER RATING TOTAL :'\
                , 'STATE :  ', 'WEBSITE :  ']
            que = [[f' #{lookitup.index(x)+1}', f'{quien[0]}  {x.name}', f'{quien[7]} {x.website}', f'{quien[1]}  {x.street_addr}'\
                , f'{quien[2]} {x.city}', f'{quien[6]} {x.state}', f'{quien[3]}  {x.zipcode}', f'{quien[4]}  {x.rating}'\
                    , f'{quien[5]}  {x.user_ratings_total}'] for x in lookitup]
            return render_template('rowsults.html', datinfo=que, dachoice=type12+', '+type11\
                , numba=range(1, len(que)), info=len(que))
    elif type12 == None:
        lookitup = AllInfo.query.filter_by(state=type11).all()
        quien = ['NAME :', 'ADDRESS :' , 'CITY :', 'ZIPCODE :', 'AVERAGE RATING :', 'USER RATING TOTAL :'\
            , 'STATE :  ', 'WEBSITE :  ']
        que = [[f' #{lookitup.index(x)+1}', f'{quien[0]}  {x.name}', f'{quien[7]} {x.website}', f'{quien[1]}  {x.street_addr}'\
            , f'{quien[2]} {x.city}', f'{quien[6]} {x.state}', f'{quien[3]}  {x.zipcode}', f'{quien[4]}  {x.rating}'\
                , f'{quien[5]}  {x.user_ratings_total}'] for x in lookitup]
        return render_template('rowsults.html', datinfo=que, dachoice=type11\
            , numba=range(1, len(que)), info=len(que))
    

if __name__ == '__main__':
    app.run(debug=True)
