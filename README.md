# staching

Compact implementation of the Mustache logic-less templating language.
This is a fork of the Stache project.
See:
    https://github.com/hyperturtle/Stache
    https://pypi.python.org/pypi/Stache/0.0.9

The biggest changes are:

- The render_js functionality has been removed making stache an even lighter
    weight implementation of Mustache

- Formatting line feeds after Mustache section tags were not being stripped properly
  staching now distinguishes between block and inline section tags and formats
  appropriately

- staching.py is a single file so can be easily embedded in another project without
  it being an external dependency

- staching.py can be run from the command line to render a template with json data

- Convenience functions

Implements everything from [Mustache.5](http://mustache.github.com/mustache.5.html)
**except for lambdas** in one small python file.

Plus five new things:
- Implied closing tags
   `{{/}}`
- Self referencer
    `{{.}}`,
- Existence check
    `{{?exists}}{{/exists}}`
- Data pusher
    `{{< blah}}{{/blah}}`
- Default
    `{{:default}}`

# Quick Start

```python
import staching

# setup the data dictionary

with open(pathtotemplatefile, "r") as fp:
    content = staching.render(fp.read(), data)

```

# Compiles all the templates and returns a template object.

```python
stacher = Stache()
# setup data dict
stacher.add_template('template_name', templatefile.read())
content = stacher.render_template('template_name', data)
```
# Overview

Fast lightweight implementation.
It consists of two main methods, `_tokenize`, and `_parse`, both python generators.
`_tokenize` creates tokens and `_parse` consumes and renders them.

# Existing Stuff

## {{tag}}

Renders the value of tag, html escaped, within the current scope

## {{{unescape}}} & {{&unescape}}

Don't html escape the value

## {{#section}}{{/section}}

Section blocks. Renders the enclosed block if

- `section` is true
- `section` exists

If `section` exists and is a(n):

- Array: It renders the enclosed block for each element in the array, placing the
current element in scope
- Dict: It renders the enclosed block once and places the Dict as the current scope

## {{^invert}}{{/invert}}

Renders the enclosed block if `invert` is an empty string, empty array, false,
or doesn't exist. The opposite the the section block.

## {{! comments - ignore me }}

Ignores the text within the tag

## {{>partial}}

Looks up the `partial` template and renders it with the current context

# New Stuff

## {{/}} Implied closing tag

Whenever you use {{/}} it implies the closing of the nearest block.

    {{#open}}stuff goes here{{/}}

Is the same as:

    {{#open}}stuff goes here{{/open}}

## {{.}} Self Referencer

This renders the current "scope". This is useful if you want to iterate over an array
and wrap them.

    {{#array}}<li>{{.}}</li>\n{{/array}}

with `array = [1,2,3,'yay']` will produce:

```html
<li>1</li>
<li>2</li>
<li>3</li>
<li>yay</li>
````

## Existence Check {{?exists}}{{/}}

Forces a check of the tag name, rather than imply that it is a section block. This
is useful for check if an array has members rather than iterate over the members

    {{?array}}
    stuff\n
    {{/}}

with `{array: [1, 2, 3, 4]}` results in:

    stuff

as opposed to

    {{#array}}
    stuff\n
    {{/}}

which would render

    stuff
    stuff
    stuff
    stuff

## {{:default}}stuff{{/}}

This is equivalent to `{{default}}{{^default}}stuff{{/}}`

It renders the enclosed section if default doesn't exist, empty or false

## {{<thing}} Pusher {{/thing}}

It renders the inner block and adds it to the global scope.

    {{<thing}}
    It takes this. You can put anything in here.
    {{tags}}, {{#blocks}}{{/blocks}}, etc.
    {{/thing}}

and it populates the global scope with a key of `thing`. Watch out, it can override
existing vars. A convention such as

    {{<namespace.thing}}{{/namespace.thing}}

or similiar will help with collisions. This is helpful if you want to use stache
templates for masterpages/inheritance.
Lets say you have these templates:

#### master =

    <div id="header">
    {{header}}
    </div>

    <div id="footer">
    {{footer}}
    </div>

#### page =

    {{<header}}
    {{name}}
    {{/header}}

    {{<footer}}
    footer
    {{/footer}}

    {{>master}}

Rendering the `page` template with `{'name': 'Stachio'}` will produce

```html
<div id="header">
Stachio
</div>

<div id="footer">
footer
</div>
```

You can also apply the inverted block or default block to supply default blocks

#### master =

    <div id="header">
    {{header}}
    {{^header}}Default Header{{/header}}
    </div>

    <div id="footer">
    {{:footer}}Default Footer{{/footer}}
    </div>

Rendering `{{<footer}}Custom Footer{{/footer}}{{>master}}` with `{}` will produce

```html
<div id="header">
Default Header
</div>

<div id="footer">
Custom Footer
</div>
```

# Install

    pip install stache

# Test

You can run `python test.py` or if you have nosetests:

    cd stache
    nosetests

# Benchmark

    python test.py

# Usage:

    >>> from Stache import Stache
    >>> Stache().render("Hello {{who}}!", dict(who="World"))
    Hello World

or

    >>> import Stache
    >>> Stache.render("Hello {{world}}!", dict(world="Stache!"))
    Hello Stache!

## To populate partials:

    >>> from Stache import Stache
    >>> stachio = Stache()
    >>> stachio.add_template('main', 'a = {{a}};')
    >>> stachio.add_template('main1', 'b = [ {{#b}}{{.}} {{/b}}];')
    >>> stachio.add_template('main2', 'stachio')
    >>> stachio.add_template('woah', '{{>main}} {{>main1}} {{>main2}}')
    >>> stachio.render_template('woah',dict(a=1, b=[1,2,3,4,5]))
    a = 1; b = [ 1 2 3 4 5 ] stachio

If you want to put in dynamic file loading of partials you can override
`Stache().templates` with a `dict()` like object and override the `__get__` and
load the template in `__get__` if it doesn't exist. Once you load up the template,
you'll need to call `self.add_template(template_name, template)` to tokenize the
template.

I don't think this is ideal though... Ideas for populating partials are welcome.

## Efficient use with async wsgi:

For wsgi apps that support async, you can yield parts of the rendered template as
they render. `render_iter` and `render_template_iter` both produce iterators that
are yield'ed as it is generated.

    >>> for part in Stache.render_iter("Hello {{world}}!", dict(world="Stache!")):
    >>>     yield part
    Hello
    Stache!


# Timeline:

