from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from forms.person_form import PersonForm
from forms.function_form import FunctionForm
from forms.tectcase_form import TestCaseForm
from forms.login import Login
from sqlalchemy.sql import func
import plotly
import json
import plotly.graph_objs as go
from werkzeug import secure_filename

# from dao.orm.model import *


app = Flask(__name__)
app.secret_key = 'key'

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Lab_4'

# ENV = 'prod'
#
# if ENV == 'dev':
#
# else:
#     app.debug = False
#     app.config[
#         'SQLALCHEMY_DATABASE_URI'] = 'postgres://wlfvowjgamjvxx:1549af6931d922ddad8a64e5bb806ae1b55cb34007771bb0bfdebaa901fd665d@ec2-174-129-255-39.compute-1.amazonaws.com:5432/d4jll9sk7spe1p'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormPersons(db.Model):
    __tablename__ = 'orm_person'

    person_login = db.Column(db.String(50), primary_key=True)
    person_password = db.Column(db.String(32), nullable=False)
    person_name = db.Column(db.String(50), nullable=False)
    person_surname = db.Column(db.String(50), nullable=False)
    person_email = db.Column(db.String(50), nullable=True)
    person_birthday = db.Column(db.Date, nullable=False)
    person_status = db.Column(db.String(50), nullable=False)
    person_photo = db.Column(db.String(200), nullable=False)

    Persons_Function = db.relationship("ormFunction")


class ormFunction(db.Model):
    __tablename__ = 'orm_function'

    function_name = db.Column(db.String(100), primary_key=True)
    function_text = db.Column(db.String(1000), nullable=False)
    counter_of_tests = db.Column(db.Integer, nullable=False)

    person_login_fk = db.Column(db.String(50), db.ForeignKey('orm_person.person_login'))

    Function_TescCase = db.relationship("ormTestCase")


class ormTestCase(db.Model):
    __tablename__ = 'orm_testcase'

    testcase_id = db.Column(db.Integer, primary_key=True)

    function_name_fk = db.Column(db.String(100), db.ForeignKey('orm_function.function_name'))

    TestCase_Parameters = db.relationship("ormParameters")
    TestCase_Result = db.relationship("ormResult")


class ormParameters(db.Model):
    __tablename__ = 'orm_parameters'

    parameters_index = db.Column(db.Integer, primary_key=True)
    testcase_iteration = db.Column(db.Integer, primary_key=True)
    parameters_value = db.Column(db.String(100), nullable=False)
    testcase_type = db.Column(db.String(20), primary_key=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('orm_testcase.testcase_id'), primary_key=True)


class ormResult(db.Model):
    __tablename__ = 'orm_result'

    result_value = db.Column(db.Integer, nullable=False)
    testcase_iteration = db.Column(db.Integer, primary_key=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('orm_testcase.testcase_id'), primary_key=True)


# db.session.query(ormResult).delete()
# db.session.query(ormParameters).delete()
# db.session.query(ormTestCase).delete()
# db.session.query(ormFunction).delete()
# db.session.query(ormPersons).delete()

@app.route('/new', methods=['GET', 'POST'])
def new():
    Dima = ormPersons(person_login="Dima",
                      person_password="0000",
                      person_name="Dima",
                      person_surname="Koltsov",
                      person_email="dik19994@gmail.com",
                      person_birthday="1999-01-01")

    Vlad = ormPersons(person_login="Vlad",
                      person_password="0000",
                      person_name="Vlad",
                      person_surname="Kanevckyi",
                      person_email="vladkaneve@gmail.com",
                      person_birthday="1999-02-04")

    Vadim = ormPersons(person_login="Vadim",
                       person_password="0000",
                       person_name="Vadim",
                       person_surname="Pits",
                       person_email=None,
                       person_birthday="1998-10-29")

    Yarik = ormPersons(person_login="Yarik",
                       person_password="0000",
                       person_name="Yarik",
                       person_surname="Artemenko",
                       person_email=None,
                       person_birthday="1999-08-11")

    Srhey = ormPersons(person_login="Srhey",
                       person_password="0000",
                       person_name="Srhey",
                       person_surname="Gorodnuk",
                       person_email=None,
                       person_birthday="1999-10-02")

    add = ormFunction(function_name="add",
                      function_text="def add(a, b):\n\treturn a+b",
                      counter_of_tests=10)

    sub = ormFunction(function_name="sub",
                      function_text="def sub(a, b):\n\treturn a-b",
                      counter_of_tests=10)

    mult = ormFunction(function_name="mult",
                       function_text="def mult(a, b):\n\treturn a*b",
                       counter_of_tests=10)

    div = ormFunction(function_name="div",
                      function_text="def div(a, b):\n\treturn a/b",
                      counter_of_tests=10)

    abs = ormFunction(function_name="abs",
                      function_text="def abs(a):\n\treturn abs(a)",
                      counter_of_tests=10)

    Dima.Persons_Function.append(add)
    Vlad.Persons_Function.append(sub)
    Vadim.Persons_Function.append(mult)
    Yarik.Persons_Function.append(div)
    Srhey.Persons_Function.append(abs)

    i_1 = ormTestCase(testcase_id=1)
    i_2 = ormTestCase(testcase_id=2)
    i_3 = ormTestCase(testcase_id=3)
    i_4 = ormTestCase(testcase_id=4)
    i_5 = ormTestCase(testcase_id=5)

    add.Function_TescCase.append(i_1)
    sub.Function_TescCase.append(i_2)
    mult.Function_TescCase.append(i_3)
    div.Function_TescCase.append(i_4)
    abs.Function_TescCase.append(i_5)

    p_0i_1_1 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=2)

    p_1i_1_1 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=3)

    p_0i_2_1 = ormParameters(parameters_index=0,
                             testcase_iteration=2,
                             testcase_type='int',
                             parameters_value=4)

    p_1i_2_1 = ormParameters(parameters_index=1,
                             testcase_iteration=2,
                             testcase_type='int',
                             parameters_value=5)

    p_0i_3_1 = ormParameters(parameters_index=0,
                             testcase_iteration=3,
                             testcase_type='int',
                             parameters_value=10)

    p_1i_3_1 = ormParameters(parameters_index=1,
                             testcase_iteration=3,
                             testcase_type='int',
                             parameters_value=31)

    p_0i_4_1 = ormParameters(parameters_index=0,
                             testcase_iteration=4,
                             testcase_type='int',
                             parameters_value=44)

    p_1i_4_1 = ormParameters(parameters_index=1,
                             testcase_iteration=4,
                             testcase_type='int',
                             parameters_value=-5)

    p_0i_5_1 = ormParameters(parameters_index=0,
                             testcase_iteration=5,
                             testcase_type='int',
                             parameters_value=8)

    p_1i_5_1 = ormParameters(parameters_index=1,
                             testcase_iteration=5,
                             testcase_type='int',
                             parameters_value=12)

    p_0i_1_2 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=4)

    p_1i_1_2 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=5)

    p_0i_1_3 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=2)

    p_1i_1_3 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=5)

    p_0i_1_4 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=100)

    p_1i_1_4 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=50)

    p_0i_1_5 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=-7)

    i_1.TestCase_Parameters.append(p_0i_1_1)
    i_1.TestCase_Parameters.append(p_1i_1_1)
    i_1.TestCase_Parameters.append(p_0i_2_1)
    i_1.TestCase_Parameters.append(p_1i_2_1)
    i_1.TestCase_Parameters.append(p_0i_3_1)
    i_1.TestCase_Parameters.append(p_1i_3_1)
    i_1.TestCase_Parameters.append(p_0i_4_1)
    i_1.TestCase_Parameters.append(p_1i_4_1)
    i_1.TestCase_Parameters.append(p_0i_5_1)
    i_1.TestCase_Parameters.append(p_1i_5_1)

    i_2.TestCase_Parameters.append(p_0i_1_2)
    i_2.TestCase_Parameters.append(p_1i_1_2)

    i_3.TestCase_Parameters.append(p_0i_1_3)
    i_3.TestCase_Parameters.append(p_1i_1_3)

    i_4.TestCase_Parameters.append(p_0i_1_4)
    i_4.TestCase_Parameters.append(p_1i_1_4)

    i_5.TestCase_Parameters.append(p_0i_1_5)

    iter_1_1 = ormResult(result_value=5,
                         testcase_iteration=1)

    iter_1_2 = ormResult(result_value=9,
                         testcase_iteration=2)

    iter_1_3 = ormResult(result_value=41,
                         testcase_iteration=3)

    iter_1_4 = ormResult(result_value=49,
                         testcase_iteration=4)

    iter_1_5 = ormResult(result_value=20,
                         testcase_iteration=5)

    iter_2_1 = ormResult(result_value=-1,
                         testcase_iteration=-1)

    iter_3_1 = ormResult(result_value=4,
                         testcase_iteration=1)

    iter_4_1 = ormResult(result_value=2,
                         testcase_iteration=1)

    iter_5_1 = ormResult(result_value=7,
                         testcase_iteration=1)

    i_1.TestCase_Result.append(iter_1_1)
    i_1.TestCase_Result.append(iter_1_2)
    i_1.TestCase_Result.append(iter_1_3)
    i_1.TestCase_Result.append(iter_1_4)
    i_1.TestCase_Result.append(iter_1_5)
    i_2.TestCase_Result.append(iter_2_1)
    i_3.TestCase_Result.append(iter_3_1)
    i_4.TestCase_Result.append(iter_4_1)
    i_5.TestCase_Result.append(iter_5_1)

    db.session.add_all([Dima, Vlad, Vadim, Yarik, Srhey, add, sub, mult, div, abs, i_1, i_2, i_3, i_4, i_5,
                        p_0i_1_1, p_1i_1_1, p_0i_2_1, p_1i_2_1, p_0i_3_1, p_1i_3_1, p_0i_4_1, p_1i_4_1, p_0i_5_1,
                        p_1i_5_1,
                        p_0i_1_2, p_1i_1_2, p_0i_1_3, p_1i_1_3, p_0i_1_4, p_1i_1_4, p_0i_1_5, iter_1_1, iter_1_2,
                        iter_1_3, iter_1_4, iter_1_5, iter_2_1, iter_3_1, iter_4_1, iter_5_1])

    db.session.commit()

    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    db.create_all()

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/person', methods=['GET'])
def person():
    result = db.session.query(ormPersons).all()

    return render_template('person.html', persons=result)


@app.route('/new_person', methods=['GET', 'POST'])
def new_person():
    form = PersonForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('person_form.html', form=form, form_name="New person", action="new_person")
        else:
            filename = ""
            if form.person_photo.data:

                filename = secure_filename(form.person_photo.data.filename)
                form.person_photo.data.save('photos/' + form.person_login.data + "." + filename.split(".")[1])


            new_person = ormPersons(
                person_login=form.person_login.data,
                person_password=form.person_password.data,
                person_name=form.person_name.data,
                person_surname=form.person_surname.data,
                person_email=form.person_email.data,
                person_birthday=form.person_birthday.data.strftime("%d-%b-%y"),
                person_status="user",
                person_photo='photos/' + form.person_login.data + "." + filename.split(".")[1]
            )

            db.session.add(new_person)
            db.session.commit()

            return redirect(url_for('person'))

    return render_template('person_form.html', form=form, form_name="New person", action="new_person")


@app.route('/edit_person', methods=['GET', 'POST'])
def edit_person():
    form = PersonForm()

    if request.method == 'GET':

        person_login = request.args.get('person_login')
        person = db.session.query(ormPersons).filter(ormPersons.person_login == person_login).one()

        # fill form and send to user
        form.person_login.data = person.person_login
        form.person_password.data = person.person_password
        form.person_name.data = person.person_name
        form.person_surname.data = person.person_surname
        form.person_email.data = person.person_email
        form.person_birthday.data = person.person_birthday

        return render_template('person_form.html', form=form, form_name="Edit person", action="edit_person")


    else:

        if not form.validate():
            return render_template('person_form.html', form=form, form_name="Edit person", action="edit_person")
        else:
            # find user
            person = db.session.query(ormPersons).filter(ormPersons.person_login == form.person_login.data).one()

            # update fields from form data
            person.person_login = form.person_login.data
            person.person_password = form.person_password.data
            person.person_name = form.person_name.data
            person.person_surname = form.person_surname.data
            person.person_email = form.person_email.data
            person.person_birthday = form.person_birthday.data.strftime("%d-%b-%y")

            db.session.commit()

            return redirect(url_for('person'))


@app.route('/delete_person', methods=['POST'])
def delete_person():
    person_login = request.form['person_login']

    result = db.session.query(ormPersons).filter(ormPersons.person_login == person_login).one()

    db.session.delete(result)
    db.session.commit()

    return person_login


@app.route('/function', methods=['GET'])
def function():
    result = db.session.query(ormFunction).all()

    return render_template('function.html', functions=result)


@app.route('/new_function/<person_login>', methods=['GET', 'POST'])
def new_function(person_login):
    form = FunctionForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('function_form.html', form=form, form_name="New function", action="new_function")
        else:
            new_function = ormFunction(
                function_name=form.function_name.data,
                function_text=form.function_text.data,
                counter_of_tests=form.counter_of_tests.data,
                person_login_fk=person_login
            )

            db.session.add(new_function)
            db.session.commit()

            return redirect(url_for('function'))

    return render_template('function_form.html', form=form, form_name="New function",
                           action="new_function/" + person_login)


@app.route('/edit_function', methods=['GET', 'POST'])
def edit_function():
    form = FunctionForm()

    if request.method == 'GET':

        function_name = request.args.get('function_name')
        function = db.session.query(ormFunction).filter(ormFunction.function_name == function_name).one()

        # fill form and send to user
        form.function_name.data = function.function_name
        form.function_text.data = function.function_text
        form.counter_of_tests.data = function.counter_of_tests
        form.person_login_fk.data = function.person_login_fk

        return render_template('function_form.html', form=form, form_name="Edit function", action="edit_function")


    else:

        if not form.validate():
            return render_template('function_form.html', form=form, form_name="Edit function", action="edit_function")
        else:
            # find user
            function = db.session.query(ormFunction).filter(ormFunction.function_name == form.function_name.data).one()

            # update fields from form data
            function.function_name = form.function_name.data
            function.function_text = form.function_text.data
            function.counter_of_tests = form.counter_of_tests.data
            function.person_login_fk = form.person_login_fk.data

            db.session.commit()

            return redirect(url_for('function'))


@app.route('/delete_function', methods=['POST'])
def delete_function():
    function_name = request.form['function_name']

    result = db.session.query(ormFunction).filter(ormFunction.function_name == function_name).one()

    db.session.delete(result)
    db.session.commit()

    return function_name


@app.route('/testcase', methods=['GET'])
def testcase():
    result = db.session.query(ormTestCase).all()

    return render_template('testcase.html', testcases=result)


@app.route('/new_testcase/<function_name>', methods=['GET', 'POST'])
def new_testcase(function_name):
    form = TestCaseForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('testcase_form.html', form=form, form_name="New testcase", action="new_testcase")
        else:
            new_testcase = ormTestCase(
                testcase_id=form.testcase_id.data,
                function_name_fk=function_name,
            )

            db.session.add(new_testcase)
            db.session.commit()

            return redirect(url_for('testcase'))

    return render_template('testcase_form.html', form=form, form_name="New testcase",
                           action="new_testcase/" + function_name)


@app.route('/edit_testcase', methods=['GET', 'POST'])
def edit_testcase():
    form = TestCaseForm()

    if request.method == 'GET':

        testcase_id = request.args.get('testcase_id')
        testcase = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == testcase_id).one()

        # fill form and send to user
        form.testcase_id.data = testcase.testcase_id
        form.function_name_fk.data = testcase.function_name_fk

        return render_template('testcase_form.html', form=form, form_name="Edit testcase", action="edit_testcase")


    else:

        if not form.validate():
            return render_template('testcase_form.html', form=form, form_name="Edit testcase", action="edit_testcase")
        else:
            # find user
            testcase = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == form.testcase_id.data).one()

            # update fields from form data
            testcase.testcase_id = form.testcase_id.data
            testcase.function_name_fk = form.function_name_fk.data

            db.session.commit()

            return redirect(url_for('testcase'))


@app.route('/delete_testcase', methods=['POST'])
def delete_testcase():
    testcase_id = request.form['testcase_id']

    result = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == testcase_id).one()

    db.session.delete(result)
    db.session.commit()

    return testcase_id


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = (
        db.session.query(
            ormPersons.person_login,
            func.count(ormFunction.function_name).label('function_count')
        ).
            outerjoin(ormFunction).
            group_by(ormPersons.person_login)
    ).all()

    query2 = (
        db.session.query(
            ormFunction.function_name,
            func.count(ormTestCase.testcase_id).label('testcase_count')
        ).
            outerjoin(ormTestCase).
            group_by(ormFunction.function_name)
    ).all()

    login, function_count = zip(*query1)
    bar = go.Bar(
        x=login,
        y=function_count
    )

    name, testcase_count = zip(*query2)
    pie = go.Pie(
        labels=name,
        values=testcase_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form, form_name="Sign up", action="login")

        else:
            try:
                result = db.session.query(ormPersons).filter(ormPersons.person_login == form.person_login.data).one()
            except:
                return render_template('login.html', form=form, form_name="Sign up", action="login",
                                       login="Неправельный логин или пароль")

            if result.person_password == form.person_password.data:
                session["login"] = form.person_login.data
                return render_template("index.html")
            else:
                return render_template('login.html', form=form, form_name="Sign up", action="login", login="Неправельный логин или пароль")

    return render_template('login.html', form=form, form_name="Sign up", action="login")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    form = Login()
    session.clear()

    return render_template('login.html', form=form, form_name="Sign up", action="login")


@app.route('/correlation', methods=['GET', 'POST'])
def correlation():
    db.create_all()

    return render_template('index.html')


@app.route('/clustering', methods=['GET', 'POST'])
def clustering():
    db.create_all()

    return render_template('index.html')


@app.route('/artificial_intelligence', methods=['GET', 'POST'])
def artificial_intelligence():
    db.create_all()

    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
