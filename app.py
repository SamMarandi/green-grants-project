import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
import sqlite3
import base64

app = Flask(__name__, static_folder='static')

app.config["session_permanent"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    db = sqlite3.connect('subsidies.db')
    db.row_factory = sqlite3.Row
    return db

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/subsidies', methods=['GET'])
def subsidies():
    home_type = request.args.get('homeType')
    ownership = request.args.get('ownership')
    types_selected = request.args.getlist('type')
    see_all = request.args.get('see_all')

    db = get_db_connection()

    # Build SQL with optional filters. Use parameterized queries to avoid SQL injection.
    sql = 'SELECT * FROM resources'
    clauses = []
    params = []

    if see_all == "true":
        subsidies = db.execute(sql, params).fetchall()
        db.close()
        return render_template('subsidies.html', subsidies=subsidies, see_all=see_all)

    if home_type:
        clauses.append('home_type LIKE ?')
        params.append("%" + home_type + "%")
    if ownership:
        if ownership == 'own':
            clauses.append('ownership_required LIKE ?')
            params.append("%" + "yes" + "%")
        elif ownership == 'rent':
            clauses.append('ownership_required LIKE ?')
            params.append("%" + "no" + "%")
    if types_selected:
        types = ""
        for i in range(len(types_selected)):
            if i > 0:
                types = types + " OR resource_type LIKE ?"
            else:
                types = types + "resource_type LIKE ?"
            params.append("%" + types_selected[i] + "%")
        clauses.append('(' + types + ')')

    if clauses:
        sql = sql + ' WHERE ' + ' AND '.join(clauses)

    subsidies = db.execute(sql, params).fetchall()
    db.close()

    return render_template('subsidies.html', subsidies=subsidies, see_all=see_all, filters={
        'home_type': home_type,
        'ownership': ownership,
        'types': types_selected,
    })

@app.route('/contractors', methods=['GET'])
def contractors():
    types_selected = request.args.getlist('type')

    db = get_db_connection()

    # Build SQL with optional filters. Use parameterized queries to avoid SQL injection.
    sql = 'SELECT * FROM contractors'
    params = []

    if types_selected:
        types = ""
        for i in range(len(types_selected)):
            if i > 0:
                types = types + " OR specialty LIKE ?"
            else:
                types = types + "specialty LIKE ?"
            params.append("%" + types_selected[i] + "%")

    if params:
        sql = sql + ' WHERE ' + types

    contractors = db.execute(sql, params).fetchall()    
    db.close()
    
    # Convert each row to dictionary for Jinja2
    contractor_list = [dict(c) for c in contractors]
    return render_template('contractors.html', contractors=contractors, filters={
        'types': types_selected,})

@app.route('/statistics')
def statistics():
    stats = {
        "num_signups": 7,
        "co2_per_home": 1.9,  # t/year
        "total_co2": round(7 * 1.9,1),
        "heat_pump_reduction": "Every home that upgrades to a heat pump can reduce greenhouse gas emissions by up to 2 tonnes per year that’s the equivalent of removing one car from the road.",
        "ontario_impact": "If you join thousands of Ontarians upgrading to heat pumps, we could prevent millions of tonnes of CO₂ over the next decade.",
        "heat_pump_amount": "About 6.6% of Ontario households have installed heat pumps so far.",
        "saving": "Toronto familites switiching to heat pumps can save around $550 per year on energy bills.",
        "efficient": "Heat pumps operate at 2-3x the efficiency of e;ectric furnaces in Ontario."
    }

    return render_template('statistics.html', stats=stats)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)




