# Turtle with Pyscript 

## by CoderDojo Trento

Turtle graphics in the browser with [Pyscript](https://pyscript.net/)!

Since we are using Pyscript, _no_ server side is needed: _all_ python code runs entirely in the browser 
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

1. Copy all the files in any simple static web server

2. Open `index.html` with the browser!


## Develop

### Http dev server

To avoid CORS restrictions, you need to run a static http server, we tested two options:

#### Dev server option a) You choose

Run any http server of your choice, open `index.html` and paste into `main.py` some example code from [from demo/](demo/) folder,
you should be able to see something actually drawn by turtle.

1. Run any http server, like python default one:

```python
python3 -m http.server -b 127.0.0.1 8000
```

2. Open browser to this link: 

http://localhost:8000/

#### Dev server option b) Run in-browser 'pseudoserver'

This option is a little weird but it works: you can access a static web page
on our server that by will be able to properly serve html files from _your_ computer.
Thanks to HTML5 wizardy,  there is _no_ data transfer to our server, which doesn't actually read anything from your computer. 
Only _your browser_ will load and parse your files.

1. Go to [static.coderdojotrento.it/pseudoserver](https://static.coderdojotrento.it/pseudoserver)
2. Give it permission to access the folder to your own computer
3. Go to [static.coderdojotrento.it/pseudoserver/host](https://static.coderdojotrento.it/pseudoserver/host)
   and enjoy!
4. edits to files will be immediately be visible upon page or game reload.

Credits: we forked the original server [servefolder.dev](https://github.com/AshleyScirra/servefolder.dev) by Ashley Scirra, big thanks to him! 

### Edit

We evaluated three editors which we deem suitable for students with no programming background.

##### Editor option a) Chrome DevTools

This is the simplest yet quite effective, we actually developed some features of Turtleps entirely in DevTools.


Pros: 

- no installation required (Chrome or similars are very often already installed in most schools) 
- since we're doing Python in the browser, students need to learn DevTools anyway
- very fast development iterations
- syntax highlighting for Python
- no Python AI (as of May 2025)  students learn more if they  write code by themselves
 
Cons:
- no Python autocompletion (as of May 2025)
- limited navigation, in particular no Pytohn jump to symbol
- editing svgs as text in sources panel seems not possible 

##### Editor option b) Visual Studio Code App


VS Code is the editor of choice for most programmers. As a HTML server, you can either install the  [Live Preview extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server) 
or use the in-browser pseudoserver solution described above
[static.coderdojotrento.it/pseudoserver](https://static.coderdojotrento.it/pseudoserver)


Pros: 

- reasonably simple to use
- very good html, js support and also Python via official Microsoft Python extension.

Cons: 

- Students might be inclined to activate Copilot stuff (not a great way to learn stuff ...)



##### Editor option 3: Visual Studio Code Online

You can also use Visual Studio Code without installing anything, just go here: [vscode.dev](https://vscode.dev)

It can load and automatically sync files from your hard-disk on save. 
Since as of May 2025 the Live Preview Extension doesn't work in the online version, you can use the pseudoserver option [static.coderdojotrento.it/pseudoserver](https://static.coderdojotrento.it/pseudoserver)
described above, which allows for a completely install-less solution 

### Reloading and caching

The browser tends to keep old versions of files to prevent reloading stuff and save bandwith. Since when developing we are actually changing files frequently, this behaviour can give us quite a few bad surprises.

There are three mechanisms to force reloading:
 
1. **disabling browser caching altogether** in browser DevTools: Unfortunately this forces also to reload each time the whole Pyodide thing which is a big file, so it's not a viable option for us.
2. **setting special headers in the server**: since we adopted a serverless solution, we can't make any assumption about the server so we can't use this option
3. **appending parameters with progressive version to file urls** like `main.py?v=12345`:

We chose option 3: we append versions to urls to trick the browser into thinking we are requesting an entirely new file each time. We versioned `.py` files and media resources like images.

### Dev buttons


 While developing, you can reload stuff by clicking these buttons
 (to prevent confusion with the normal refresh browser button, users of the finished game shouldn't be able to see them)


![blue reload](img/refresh.svg): reload current py file

![orange reload-all](img/refresh-all.svg)  reloads the whole page, all py file and media resources 


![play](img/play.svg) : resets the game fast without reloading resources (or pyodide).


![stop](img/stop.svg): stops the game please be careful it can only interrupts `asyncio` tasks, if you get stuck with an infinite loop in your code which doesn't `await`, you can either:

a. close the page browser tab (but this also closes the DevTools), 

b. (better) hit `Shift-Esc`  to open the Chrome Process panel, in which you can kill the page without closing DevTools.  



### Test

Test page is in [test.html](test.html). You can load most tests by passing an `s` parameter like:

```
http://localhost:8000/test.html?s=test/uitest_click.py
```

Tests starting with `uitests_` are meant to be test suites.

Note: since the browser can't know which python files are on the server for security reasons, 
in some cases you have to explicitly write them in the pyscript config. For example,
to build [pyscript-test.json](pyscript-test.json) we wrote a litle utility
[test/build_test_config.py](test/build_test_config.py) that takes the template
in [test/pyscript-test-template.json](test/pyscript-test-template.json) and fills it with 
the test file names.

## Technical stuff

### Pyscript and pyodide

To interface between the browser and Python interpreter we're using Pyscript,
which in this case runs pyodide a WASM port. 

Note there is no transcompilation to Javascript, the python code runs entirely in a true CPython environment.

### Display with SVG

As graphical display we use a native `<svg>` element in the browser. This has the following benefits:

- provides a lot of primitives
- svg is easily inspectable with browser tools
- if they want, students can get to learn svg also
- can be styled with css, another occasion to learn stuff

Typically for videogames you would choose `<canvas>`, as svg is slower for videogames but 
since this lib is thought for educational purposes we think svg is sufficient.

As a downside, sometimes svg spec is not fully implemented by browsers, in particular when loading
other images into an existing svg you may get weird behaviour, like Chrome not respecting 
transparency when clicking, in such cases we implement workarounds.

### Pyscript initialization

Pyscript is initialized by [turtleps.js](js/turtleps.js) which creates a config and injects a Python `<script>` in the HTML with a custom inline Pyscript config. We chose this solution as we wanted to version loaded files according to the current timestamp. 

### Developer notes

- [styling svg with use, symbol, defs](https://tympanus.net/codrops/2015/07/16/styling-svg-use-content-css/)
- [Structuring, Grouping, and Referencing in SVG](https://www.sarasoueidan.com/blog/structuring-grouping-referencing-in-svg/#the-use-element)
 

## Credits and inspiration

- some code initially was taken from [Pyscript Antigravity example](https://pyscript.net/examples/antigravity.html)
- most turtle code was copyied from this transcrypt implementation:

  https://github.com/TranscryptOrg/Transcrypt/blob/master/transcrypt/modules/turtle/__init__.py
  
  which has liberal license Apache v2.0 (reported in [third-party-licences](third-party-licences)

  Note we don't use transcrypt lib at all, our project code entirely runs in a CPython environment.
