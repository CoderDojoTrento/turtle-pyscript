# Turtle with Pyscript 

## by CoderDojo Trento

Turtle graphics in the browser with [Pyscript](https://pyscript.net/)!

Since we are using Pyscript, NO server side is needed: *all* python code runs entirely in the browser 
in a real CPython environment. 

**STATUS: BETA**

**SPACE EXPLORER DEMO**: https://coderdojotrento.github.io/turtle-pyscript/demo.html?s=demo/space_rocket.py

**STORYTELLING DEMO**: https://coderdojotrento.github.io/turtle-pyscript/demo.html?s=demo/storytelling.py

**ALL TESTS**: https://coderdojotrento.github.io/turtle-pyscript/test.html?s=test/uitests_all.py


**Turtle API:** We try to be faithful to original api as much as we can. Currently we support most important things and it should work. Tested successfully in a high school classroom. 

Most noticeable problems: 

- movements are currently always immediate, [see issue about concurrency](https://github.com/CoderDojoTrento/turtle-pyscript/issues/8).
- Stamp is currently buggy ([see issue](https://github.com/CoderDojoTrento/turtle-pyscript/issues/13))
- There is noticeable lag ([see issue](https://github.com/CoderDojoTrento/turtle-pyscript/issues/18)) if you have the pen down, to prevent it keep calling `color('yellow')`


**Game engine**: We also provide an experimental `Sprite` API built on top of `Turtle` which is in flux and subject to change.

## Deploy

1. Copy all the files in any web server

2. Open `index.html` with the browser!


## Develop

If you run any http server and open `index.html` you should be able to see something actually drawn by turtle.

1. Run any http server, like python default one:

```python
python3 -m http.server -b 127.0.0.1 8000
```

2. Open browser to this link: 

http://localhost:8000/

### Test

Test page is in [test.html](test.html). You can load most tests by passing an `s` parameter like:

```
http://localhost:8000/test.html?s=test/uitest_click.py
```

Tests starting with `uitests_` are meant to be test suites.

Note: since the browser can't know which python files are on the server for security reasons, in some cases you have to explicitly write them in the pyscript config. For example, to build [pyscript-test.json](pyscript-test.json) we wrote a litte utility [test/build_test_config.py](test/build_test_config.py) that takes the template in [test/pyscript-test-template.json](test/pyscript-test-template.json) and fills it with the test file names.

## Technical stuff

### Pyscript and pyodide

To interface between the browser and Python interpreter we're using Pyscript, which in this case runs pyodide a WASM port. 

Note there is no transcompilation to Javascript, the python code runs entirely in a true CPython environment.

### Display with SVG

As graphical display we use a native `<svg>` element in the browser. This has the following benefits:

- provides a lot of primitives
- svg is easily inspectable with browser tools
- if they want, students can get to learn svg also
- can be styled with css, another occasion to learn stuff

Typically for videogames you would choose `<canvas>`, as svg is slower for videogames but 
since this lib is thought for educational purposes we think svg is sufficient.

As a downside, sometimes svg spec is not fully implemented by browsers, in particular when loading other images into an existing svg you may get weird behaviour, like Chrome not respecting transparency when clicking, in such cases we implement workarounds.

### Developer notes

- [styling svg with use, symbol, defs](https://tympanus.net/codrops/2015/07/16/styling-svg-use-content-css/)
- [Structuring, Grouping, and Referencing in SVG](https://www.sarasoueidan.com/blog/structuring-grouping-referencing-in-svg/#the-use-element)
 

## Credits and inspiration

- some code initially was taken from [Pyscript Antigravity example](https://pyscript.net/examples/antigravity.html)
- most turtle code was copyied from this transcrypt implementation:

  https://github.com/TranscryptOrg/Transcrypt/blob/master/transcrypt/modules/turtle/__init__.py
  
  which has liberal license Apache v2.0 (reported in [third-party-licences](third-party-licences)

  Note we don't use transcrypt lib at all, our project code entirely runs in a CPython environment.
