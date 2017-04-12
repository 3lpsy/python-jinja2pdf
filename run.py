import argparse
import importlib

from page import Page

if __name__ == '__main__':
    print("Pemplate: Build it Puetiful")
    parser = argparse.ArgumentParser()

    parser.add_argument("template",
        type=str,
        action='store',
        help="Template Name without .html extension (ex: document for templates/document.html)"
    )

    parser.add_argument("--context",
        type=str,
        action='store',
        help="Name of python script in current directory that contains a main function returning a dictionary of template variables",
        default=False
    )


    known, unknown = parser.parse_known_args()
    template = known.template
    context = {}

    if known.context:
        context_module = importlib.import_module(known.context)
        context = context_module.main()

    for ii in range(len(unknown)):
        if ii % 2 == 0:
            key = unknown[ii]
            value = unknown[ii + 1]
            context[key.replace('-', '')] = value

    
    page = Page(template, context)

    page.render()
    page.pdf()
