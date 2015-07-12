import StringIO
import json
import pandas as pd
import mpld3
from mpld3 import fig_to_html, plugins, fig_to_dict
from bokeh.embed import components
from bokeh.resources import CDN
from flask import Response, stream_with_context
from entities import identifier_generator as ig

# Basic api representation resource
# This is simply to ensure that we can react on each representation asked per resource
# TODO error should be thrown if representation is irrelevant
class ApiResource(object):
    def __init__(self, content, name=""):
        self.content = content
        self.name = name

    def to_json(self):
        pass

    def to_csv(self):
        pass

    def to_png(self):
        pass

    def to_html(self):
        pass

    def to_pdf(self):
        pass

    def __str__(self):
        return str(self.content)


# Input is string
# implemented representations are json and csv
class StringApiResource(ApiResource):
    def to_json(self):
        return json.dumps(self.content)

    def to_csv(self):
        return str(self.content).split(',')

    def to_pdf(self):
        return str(self.content)


# Input is pandas dataframe
# implemented representations are json and csv
class DataFrameApiResource(ApiResource):
    def to_json(self):
        return self.to_csv()

    def to_csv(self):
        str_buffer = StringIO.StringIO()
        self.content.to_csv(str_buffer, sep="\t")

        return Response(str_buffer.getvalue(), mimetype="text/csv", headers={"content-disposition":"attachment; filename=\"" + self.name + "\""})

    def to_html(self):
        print("html content")
        str_buffer = StringIO.StringIO()
        self.content.head().to_html(str_buffer)
        print("responding")
        return Response(str_buffer.getvalue())


class DataFrameJsonResource(ApiResource):
    def to_json(self):
        return json.dumps(self.content)

    def to_html(self):
        str_buffer = StringIO.StringIO()
        df = pd.read_json(json.dumps(self.content))
        df.to_html(str_buffer)

        return str_buffer.getvalue()

    #send raw csv file with counts
    def to_csv(self):
        pass


# Input is MatPlotLib
# implemented representations are html and json
class MatPlotLibResource(ApiResource):
    def to_json(self):
        str_buffer = StringIO.StringIO()
        mpld3.save_json(self.content, str_buffer)
        return str_buffer.getvalue()

    def to_html(self):
        import matplotlib.pyplot as plt
        html = fig_to_html(self.content, figid="generatedchart")
        #closes fig element (refresh)
        plt.close()

        return html

    def to_png(self):
        pass


    def to_pdf(self):
        return self.content



class BokehResource(ApiResource):
    def to_json(self):
        return json.dumps(self.content)

    def to_html(self):
        script, div = components(self.content, CDN)
        #plt.close()
        return str(script) + str(div)

    def to_png(self):
        pass


class JsonResource(ApiResource):
    def to_json(self):
        return json.dumps(self.content)

    def to_csv(self):
        return self.to_json()

    def to_html(self):
        return self.to_json()

