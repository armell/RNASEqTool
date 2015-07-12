from StringIO import StringIO

from flask import Flask, make_response, g
from flask import redirect, url_for, request, render_template
from flask.ext import restful, cors
from playhouse.db_url import connect
from api import gene_expression_resources as expression_resources, content_representations
from entities import entities
from werkzeug.contrib.fixers import ProxyFix
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.peewee import ModelView
from entities.entities import database as db
import entities.entities as ent

app = Flask(__name__)
api = restful.Api(app)
cors = cors.CORS(app)
#admin = Admin(app, url="/RNASeqTool/admin")

class AdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

#admin.add_view(AdminView(name='RNASeqAdmin'))
#admin.add_view(ModelView(ent.Experiments, db))
#app.debug = True

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(data.to_json(), code)
    resp.headers.extend(headers.items().append({"Location": request.base_url}) or {"Location": request.base_url})

    return resp


@api.representation('text/csv')
def output_csv(data, code, headers=None):
    strbuffer = StringIO()
    data.to_csv(strbuffer, index=False)
    resp = make_response(strbuffer.getvalue(), code)
    resp.headers.extend(headers.items().append({"Location": request.base_url}) or {"Location": request.base_url})

    return resp


@api.representation('application/javascript')
def output_chart(data, code, headers=None):
    pass


@api.representation('text/html')
def output_html(data, code, headers=None):
    resp = make_response(data.to_html(), code)
    resp.headers.extend(headers.items().append({"Location": request.base_url}) or {"Location": request.base_url})

    return resp

@api.representation('application/pdf')
def output_pdf(data, code, headers=None):
    resp = make_response(data.to_pdf(), code)
    resp.headers.extend(headers.items().append({"Location": request.base_url}) or {"Location": request.base_url})

    return resp


api.add_resource(expression_resources.Stream, "/api/expression/stream",
                 "/api/expression/stream/<string:taskId>")
api.add_resource(expression_resources.Methods, "/api/expression/methods")
api.add_resource(expression_resources.Method, "/api/expression/method/<string:methodId>/<string:package>")
api.add_resource(expression_resources.Experiments, "/api/expression/experiments")
api.add_resource(expression_resources.Experiment, "/api/expression/experiment/<string:experimentId>")
api.add_resource(expression_resources.Charts, "/api/expression/charts")
api.add_resource(expression_resources.Chart, "/api/expression/chart/<string:chartId>")
api.add_resource(expression_resources.Datasets, "/api/expression/datasets")
api.add_resource(expression_resources.Dataset, "/api/expression/dataset/<string:datasetId>/<string:elements>")
api.add_resource(expression_resources.Tasks, "/api/expression/tasks")
api.add_resource(expression_resources.Task, "/api/expression/task/<string:taskId>")


@app.route('/')
def index():
    return redirect("http://wgs11.op.umcutrecht.nl/RNASeqTool/static/app/index.html", code="302")

@app.route('/api')
def api():
    return render_template("api.html")

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    #app.debug = True
    print("starting")
    app.run('127.0.0.1', debug=True)

