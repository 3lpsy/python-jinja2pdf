# python-jinja2pdf

This project is POC for a command line util to convert jinja2 templates to pdfs. It's a rushed proof of concept so expect bugs if attempting to use it.

## Installation

1. git clone https://github.com/3lpsy/python-jinja2pdf.git
2. cd python-jinja2pdf
3. virtualenv venv
4. source venv/bin/activate
5. pip install -r requirements.txt

## Basic Usage

### Templates without Variables

Running the command.

```
$ python run.py --template example
```

The template option is always required. It must be the name of a file in the templates folder. For example, 'example' (no html extension) refers to templates/example.html


### Templates with Variables Passed In

You can pass in variables from the command line. These variables will be available in your template.

```
python run.py --title "Argument Example" --content "hello darkness my old friend" --template example2
```

Title and content will be rendered within the html template where {{title}} and {{content}} are used. Your variables can have any name (except 'template' and 'context' as those are reserved) as long as they are in the --key value format. Every key must have a value.

### Templates with Variables in a python module

You can also define more complicated variables in a python module (file) in the root directory.

For example, you could have a file 'example3_context.py' which contains:

```
def main():
    return {
        "title": "Context Example",
        "content": "Hello Darkness my old friend"
    }
```

The file must contain a main function.

You would then pass in the file module name (without the '.py' extension) as the context option:

```
$ python run.py --context 'example3_context' example
```

These variables will be available just as in example2.

## Output

The command first render's the html file from the jinja2 template. This file is output in the rendered folder for debugging. Next, the command renders a pdf using xhtml2pdf using this html file. The pdf is output in the pdf folder.

## Images and class

You can link to external images and style files (http) from your template. The tool will pull the resources and save them under assets with a unique name. Currently, only simple css and images are supported.

Relative images are not supported. However, you could use full file paths in your template.

## Contributing

It's pretty bootleg so feel free to submit a PR if you see something that can be improved.
