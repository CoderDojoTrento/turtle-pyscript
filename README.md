# Turtle with Pyscript 

## by CoderDojo Trento


An experiment to make turtle graphics work with [Pyscript](https://pyscript.net/)

Since we are using Pyscript, NO server side is needed, and *all* python code runs entirely in the browser 
in a real CPython environment. 

**STATUS: PRE-ALPHA**

Code is very dirty and unpolished.


## Deploy

1.  Pyscript needs a way to find your python files: If you deploy to a server with a subpath you have to set PATH [template](https://docs.pyscript.net/2024.8.2/user-guide/configuration/#files) accordingly in [pyscript.json](pyscript.json)

For example, normally the `PATH` would be just `/` but in the demo https://coderdojotrento.github.io/turtle-pyscript/  

the `PATH` must be set to  `/turtle-pyscript`

2. serve the website with any static http**s** (mind the s) webserver

3. open `index.html` with the browser!


## Develop

If you run any http**s** server (mind the s) and open `index.html` you should be able to see something actually drawn by turtle.

You need http**S** because currently there is a Pyscript component (`sabayon`) which insists on calling `crypto.randomUUID()` 
which can only be executed in an http**s** environment

So to easily setup a test http**s** server run these scripts: 

1. Create `test/server.pem` file

```bash
openssl req -new -x509 -keyout test/server.pem -out test/server.pem -days 365 -nodes
```

2. Run the server:

```python
python3 test/server.py
```

3. Open browser to this link: 

https://127.0.0.1:8008/

It will warn you the certificate is not signed, just click proceed.


**NOTE**: DON'T run this test server in production, you don't need it and it would also be unsafe.


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
since lib is thought for educational purposes svg is sufficient.


### Developer notes

- [styling svg with use, symbol, defs](https://tympanus.net/codrops/2015/07/16/styling-svg-use-content-css/)
- [Structuring, Grouping, and Referencing in SVG](https://www.sarasoueidan.com/blog/structuring-grouping-referencing-in-svg/#the-use-element)
 

## Credits and inspiration

- some code initially was taken from [Pyscript Antigravity example](https://pyscript.net/examples/antigravity.html)
- most turtle code was copyied from this transcrypt implementation:

  https://github.com/TranscryptOrg/Transcrypt/blob/master/transcrypt/modules/turtle/__init__.py
  
  which has liberal license Apache v2.0 (reported in [third-party-licences](third-party-licences)

  Note we don't use transcrypt lib at all, our project code entirely runs in a CPython environment.
