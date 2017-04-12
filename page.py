from jinja2 import Template
from os.path import abspath, join, dirname
from pathlib import Path
from datetime import datetime
from xhtml2pdf import pisa
from base64 import b64encode
import requests
from mimetypes import guess_extension

def link_callback(uri, rel):
    if uri and str.startswith(uri, 'http'):
        r = requests.get(uri)
        if r.status_code == 200:
            tmp_asset_filename =  b64encode(uri.encode())
            tmp_asset_path = join(dirname(abspath(__file__)), 'assets/' + tmp_asset_filename.decode() + guess_extension(r.headers['content-type'].split()[0].rstrip(";")))
            content_type = r.headers['Content-Type']
            tmp_asset_file = Path(tmp_asset_path)

            if not tmp_asset_file.is_file():
                tmp_asset_file.touch()

            content = r.content
            with open(tmp_asset_path, 'wb') as f:
                f.write(content)

            return tmp_asset_path
        else:
            raise Exception('Failed import of <link> or <image> ' + uri)

class Page(object):
    def __init__(self, name, context = None):
        self.name = name
        self.context = context or {}
        self.rendered_path = None
        self.output_path = None
        self.pdf_path = None

    def render(self):
        template_path = self._template_path(self.name)
        with open(template_path, 'r') as f:
            text = f.read()
        template = Template(text)
        context = self.context
        html = template.render(**context)
        rendered_path = join(dirname(abspath(__file__)), 'rendered/' + self.name + "-" +datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + '.html')
        rendered_file = Path(rendered_path)
        rendered_file.touch()
        rendered_file.write_text(html)
        self.rendered_path = rendered_path
        return html

    def pdf(self):
        if not self.rendered_path:
            raise Exception("HTML not rendered")
        output_path = join(dirname(abspath(__file__)), 'pdf/' + self.name + "-" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + '.pdf')

        with open(self.rendered_path, 'r') as f:
            html = f.read()

        with open(output_path, 'w+b') as output:
            pisa_status = pisa.CreatePDF(
                html.encode(),
                dest=output,
                link_callback=link_callback
            )
            return pisa_status.err

        self.output_path = output_path

    def _template_path(self, name):
        return join(dirname(abspath(__file__)), 'templates/' + name + '.html')
