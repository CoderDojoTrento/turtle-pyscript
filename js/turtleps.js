
console.log("Loading turtleps.js ...");

/*
 * @since 0.10.0
 */
const DAY = 1000*60*60*24; // as milliseconds
/*
 * @since 0.10.0
 */
const PYSCRIPT_CORE_VERSION = "2025.3.1";

/*  ordered by importance first to last  
    
*/
let DEFAULT_OPTIONS = {s: '',
                       refresh_buttons: true,    
                       show_game: true,   
                       navbar: true,   // only available in run_from_params
                       sticky: false,  // puts control panel high and expands it
                       show_game: true,
                       config_url : "pyscript.json",
                       cache_expiration : DAY * 60,
                       v: 0,       //  for everything
                       v_code: 0,
                       // mode: 'dev', // allowed: 'dev' or 'demo' // not neededd for now 
}

/* @since 0.10.0

Awaits event on given target only *once*
*/
// https://www.reddit.com/r/learnjavascript/comments/19alv5n/what_would_be_bestpractice_to_wait_until_2_events/
async function when(target, event, {
  signal, capture, passive, 
} = {}) {
  const { promise, resolve } = Promise.withResolvers();
  target.addEventListener(event, resolve, { once: true, signal, capture, passive });
  return promise;
}


console.log("Patching console.error to catch TPS-STOPEX CancelledError");

/* @since 0.10.0
*/
let orig_console_error = console.error;

console.error = function(...theArgs){
    //console.log('override:', theArgs);
    if ( theArgs 
         && theArgs[0].type === 'CancelledError'
         && theArgs[0].message.includes('TPS-STOPEX')){
         console.log("(TPS: swallowed CancelledError because of regular game stop)");
         let errors = document.querySelectorAll('.py-error');
         console.log(errors);
         for (let err of errors){
             if (err.innerText.includes('TPS-STOPEX')){
                 console.log('Delete TPS-STOPEX in', err);
                 //err.innerText = '';
                 err.remove(); 
             }
         }
    } else {
        orig_console_error.apply(null, theArgs);
    }
}





/*  
    Traces the svg silhouette of the given work_img and puts 
    the result into target node innerHTML

    @return a canvas with the silhouette
    @since 0.9.0 
*/
export function vectorize(work_img, target) {
    

    //console.log('target:', target);
    //console.log('target.id:', target.id);

    //console.log('work_img:', work_img);
    

    let imageTracerOptions = {
        /*pal: [{r:0,g:0,b:255,a:255},{r:0,g:255,b:0,a:255}]*/
        colorsampling : 0,
        numberofcolors: 2  // tried 1 but seems to only create a rectangle covering everything :-/
    }
    let work_canvas = document.createElement("canvas");
    let ctx = work_canvas.getContext("2d");
    let imageData;

    
    work_canvas.width = work_img.width
    work_canvas.height = work_img.height
    
    ctx.drawImage(work_img, 0, 0, work_img.width, work_img.height);
    
    let img_width = work_img.width;
    let img_height = work_img.height;
    //console.log('work_img size:', img_width, img_height);
    

    imageData = ctx.getImageData(0, 0, img_width, img_height);
    //console.log("image data:", imageData);

    // single array, RGBA order, 0.255,  by rows from the top-left pixel to the bottom-right.
    
    let d = imageData.data;
    for (let i = 0, l = d.length; i < l; i += 4) {
        if (d[i+3] === 0){
            d[i] = 255;
            d[i+1] = 255;
            d[i+2] = 255;
        } else {
            d[i] = 0;
            d[i+1] = 0;
            d[i+2] = 0;
            d[i+3] = 255;
        }
    }
    let _ns = 'http://www.w3.org/2000/svg';

    let svgString = window.ImageTracer.imagedataToSVG(imageData, imageTracerOptions);
    //console.log("Got vectorialized svg string!", svgString)

    let ntemp = document.createElement('div');
    ntemp.innerHTML = svgString;
    let silouettes = ntemp.querySelectorAll('path[fill="rgb(0,0,0)"]');
    //console.log("silouettes", silouettes);
    if (silouettes.length === 0){
        console.error("ERROR: nothing found to trace in image:", work_img);
        target.innerHTML = "";
    } else {
        for (const s of silouettes){
            target.append(s);
        }
        //console.log('ntemp:', ntemp)
        //target.innerHTML = ntemp.innerHTML;    
    }

    return work_canvas
};


/* Runs a script given by page parameter s 

     * !!!!!!!   WARNING    !!!!!!!!
     * 
     * THIS FUNCTION ALLOWS UNTRUSTED USERS TO RUN ANY .py FILE PRESENT IN demo/ OR test/ FOLDERS
     * 
     * @since 0.10.0
*/
export function run_from_params(){
    
    let page_name = window.location.pathname.split("/").slice(-1)[0]; 
    console.log("page_name", page_name);
    if (page_name !== "demo.html" && page_name !== "test.html" ){
        throw new Error("run_param function can only be called from demo.html or test.html pages, found instead: " + window.location.href);
    }


    let the_options = Object.assign({}, DEFAULT_OPTIONS);
    const params = new URLSearchParams(window.location.search);
    
    let game_box = document.getElementById("tps-game-box");
    let msg_box = game_box ? game_box : document.body;

    let s = params.get('s');
    
    if (!s){
        msg_box.innerHTML = "<h2>PLEASE SELECT A SCRIPT TO RUN</h2>";
        console.log("TPS: Missing s parameter.")
        return;
    }
    
    const re = /(test\/|demo\/)[a-zA-Z0-9_/]+\.py/;
    let arr = re.exec(s);
    if (!arr || ( arr.length == 0 || arr[0].length !== s.length)){
        msg_box.innerHTML = "ERROR: WRONG SCRIPT! <br><br> SEE CONSOLE FOR MORE INFO.";    
        throw new Error("Got wrong script url:" + s + "it must respect this regex:" + re);
    }

    let subdir = s.substring(0,4);
    console.log("subdir:", subdir);

    if (subdir === "demo"){
        the_options.refresh_buttons = false;
    } else if (subdir === "test"){
        the_options.config_url = "pyscript-test.json";
    }
     
    for (const [pk, pv] of params){
        if (DEFAULT_OPTIONS.hasOwnProperty(pk)){
            if (typeof DEFAULT_OPTIONS[pk] === 'boolean') {
                the_options[pk] = pv === 'false' ? false : true;
            } else if (typeof DEFAULT_OPTIONS[pk] === 'number') {
                the_options[pk] = Number(pv);
            }  else {
                the_options[pk] = pv
            }
        } else {    
            the_options[pk] = pv;  
        };
                   
    }

    if (s.includes("/uitests_")){   
        console.log("Found uitests suite, making sticky.");    
        the_options.sticky = true;
        the_options.show_game = false;
    }

    let navbar = document.getElementById("tps-navbar");
    
    console.log("the_options:", the_options);
    
    console.log("tps-navbar:", navbar);
    if (navbar){
        if (the_options.navbar){    
            navbar.style.display = "block";
        } else {
            navbar.style.display = "none";
        }
    }
    run(the_options);
}

/* 
 * Updates ui game status
 * @since 0.10.0
 */
function update_ui_game_status(game_status){
    
    let play_button = document.querySelector("#tps-game-box .tps-play img");
    let stop_button = document.querySelector("#tps-game-box .tps-stop img");
    let screen  = document.querySelector("#tps-game-box .tps-screen");
    
    
    if (game_status === "PLAY"){
        if (play_button){
            play_button.classList.add('tps-ctrl-pressed');
        }
        if (stop_button){
            stop_button.classList.remove('tps-ctrl-pressed');
        }
        if (screen){
            screen.classList.remove('tps-screen-stopped');
        }
    } else if (game_status === "STOP") {
        if (play_button){
            play_button.classList.remove('tps-ctrl-pressed');
        }
        if (stop_button){
            stop_button.classList.add('tps-ctrl-pressed');
        }
        if (screen){
            screen.classList.add('tps-screen-stopped');
        }
    } else {
        throw new Error("Unrecognized game status:", game_status);
    }
    
}

/* @since 0.10.0
*/
export async function stop_game(options){
    console.log("turtleps.js:  stop_game()");

    console.log("Stopping python scripts...");

    const script = document.createElement('script');
    script.setAttribute("type","py");         
    script.textContent = "import turtleps\n"
                        + "turtleps.ge_stop()\n"
    
    const tps_pyscript = document.getElementById("tps-pyscript");
    tps_pyscript.appendChild(script);
    await when(window, "py:done");
    update_ui_game_status("STOP"); // TODO sync with module
    console.log("turtleps.js:  stop_game() is DONE.");
    
};


/* @since 0.10.0
*/
export async function play_game(options){

    console.log("turtleps.js:  play_game(", options, ")");
    
    update_ui_game_status("PLAY"); // TODO sync with module
    
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options);

    await stop_game(options);

    
    update_ui_game_status("PLAY"); // TODO sync with module
    
    console.log("Resetting python memory...");

    const script = document.createElement('script');
    script.setAttribute("type","py");         
    script.textContent = "import turtleps\n"
                        + "turtleps.ge_reset()\n"
    
    const tps_pyscript = document.getElementById("tps-pyscript");
    tps_pyscript.appendChild(script);
    await when(window, "py:done");
    console.log("Going to reload script...", the_options.s);
    run(the_options);
    console.log("turtleps.js:  play_game() is DONE.");
};



/* @since 0.10.0
*/
export async function reload (options){

    console.log("turtleps.js:  reload(", options, ")");
    
    let what = 'tps_v_code';
    try {
        console.log("Clearing ", what, " from local storage..");
        window.localStorage.removeItem(what);            
    } catch (e){
        console.info("Failed to clear " , what, " from localStorage. Reason:", e);
    }

    const current_time = new Date().getTime();  // milliseconds since 1970
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options, {v_code:current_time}) 
    
    await play_game(the_options);
    console.log("turtleps.js:  reload() is DONE.");
};


/* @since 0.10.0
*/
export function reload_all (options){
    console.log("turtleps.js:  reload_all(", options, ")");
    
    const current_time = new Date().getTime();  // milliseconds since 1970

    try {
        console.log("Clearing local storage..");
        window.localStorage.clear();            
    } catch (e){
        console.info("Failed to clear localStorage. Reason:", e);
    }

    console.log('options:', options)
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options, {v:current_time, 
                                                                   v_code: DEFAULT_OPTIONS.v_code})
    

    console.log('the_options:', the_options)
    
    let ps = '';
    let prev = '';
    for (const key of Object.keys(DEFAULT_OPTIONS)) { // insertion order, thanks to ES2015
        console.log('the_options[key]', the_options[key])
        console.log('DEFAULT_OPTIONS[key]', DEFAULT_OPTIONS[key])
        
        if (the_options[key] !== DEFAULT_OPTIONS[key]){
            ps += prev + key + '=' + the_options[key];   // not encoded and not correct, but we get pretty urls    
            prev = '&';
        }
    }
    let new_location = window.location.origin 
                       + window.location.pathname 
                       + '?' + ps 
                       + window.location.hash;
    console.log("Going to ", new_location);
    window.location.href = new_location;
}

/* @since 0.10.0
*/
function determine_timestamp(requested_v, local_v, current_time, cache_expiration){

    let v;
    if (requested_v){
        if (local_v){
            v = Math.max(requested_v, local_v);
        } else {
            v = current_time;
        }
    } else {
        if (local_v){
            v = local_v;
        } else {
            v = current_time;
        }
    }

    if (current_time > v + cache_expiration ){
        console.log("Elapsed ", (current_time - v) / DAY, "days since timestamp, updating it..");
        v = current_time;
    }

    return v;
}

/* @since 0.10.0
*/
function load_timestamp(what, current_time){
    let local_v;
    try {
        console.log("Loading ", what, " from local storage..");
        local_v = window.localStorage.getItem(what);
        if (local_v === null){
            console.log("Couldn't find ", what," in local storage");
            local_v = current_time;
        }
    } catch (e){
        console.info("Failed to load ",what,". Reason:", e);
        local_v = current_time;
    }
    return local_v
}


/* Runs a script from script_path
 * 
 * @since 0.9.0
 */
export function run(options){
    
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options);

    console.log("Requested running: ", the_options.s, "   at timestamp: ", the_options.v_code);
    
    console.log("the_options:", the_options);

    const current_time = new Date().getTime();  // milliseconds since 1970

    let local_v = load_timestamp('tps_v', current_time);
    let local_v_code = load_timestamp('tps_v_code', current_time);

    
    let html = /* html */ `
                
                <div class="tps-loading">
                    <span class="tps-loading-message">
                        <img title="Loading.." width="28px" src="img/loading.svg"/>    
                    </span>
                    
                </div>
                <div class="tps-game-ctrl-panel">
                    <a class="tps-play tps-game-ctrl" href="#"><img title="Run the current script" src="img/play.svg" width="30px"></a>
                    <a class="tps-stop tps-game-ctrl" href="#"><img title="Stop the game" src="img/stop.svg" width="30px"></a>
                    <a class="tps-reload-all tps-game-ctrl" href="#"> 
                        <img title="Try refresh all: scripts, pages, images, sounds..." 
                             src="img/refresh-all.svg" 
                             width="30px"/>
                    </a>
                    <a class="tps-reload tps-game-ctrl" 
                       href="#"> 
                       <img title="Refresh only scripts" 
                            src="img/refresh.svg"
                       width="30px">
                    </a>
                </div>
                <svg class="tps-screen">
                </svg>
    `;

    const game_area = document.getElementById("tps-game-area");
    const game_box = document.getElementById('tps-game-box');
    
    if (game_box && game_box.children.length === 0){
        console.log("TPS: Populating tps-game-box...");
        game_box.innerHTML = html;
        game_box.classList.add("tps-game-box");
    }
    
    const loading = document.querySelector('#tps-game-box .tps-loading');
    const screen = document.querySelector('#tps-game-box .tps-screen');
    screen.classList.add("tps-screen-loading");
    loading.style.visibility = 'visible';

    if (game_area){
        if (the_options.sticky){
            game_area.classList.add('tps-game-area-sticky');
        } else {
            game_area.classList.remove('tps-game-area-sticky');
        }    
    }
    
    
    if (the_options.show_game){
        screen.style.display = "block";
    } else {
        screen.style.display = "none";
    }
    
    
// ECMAScript 6 says it's evaluated only once
    addEventListener('py:ready', () => 
        {loading.style.visibility = 'hidden';
         screen.classList.remove('tps-screen-loading');
         update_ui_game_status("PLAY"); // TODO sync with module
        });


    let v = determine_timestamp(the_options.v, local_v, current_time, the_options.cache_expiration);
    console.log("Will use timestamp v=", v);

    let v_code = determine_timestamp(the_options.v_code, local_v_code, current_time, the_options.cache_expiration);
    console.log("Will use timestamp v_code=", v_code);

    try {
        console.log("Saving timestamp to local storage..");
        window.localStorage.setItem("tps_v", v);
        console.log("Saving code timestamp to local storage..");
        window.localStorage.setItem("tps_v_code", v_code);
        
    } catch (e){
        console.info("Failed to save timestamp. Reason:", e);
    }


    let reload_button = document.querySelector("#tps-game-box .tps-reload");
    reload_button.onclick = (e)=>{reload(options);}
    reload_button.style.display = the_options.refresh_buttons ? 'inline' : 'none';
    
    let reload_all_button = document.querySelector("#tps-game-box .tps-reload-all");
    reload_all_button.onclick = (e) => {reload_all(options);}
    reload_all_button.style.display = the_options.refresh_buttons ? 'inline' : 'none';
    
    
    let stop_button = document.querySelector("#tps-game-box .tps-stop");
    stop_button.onclick = (e) => {stop_game(options);}

    let play_button = document.querySelector("#tps-game-box .tps-play");
    play_button.onclick = (e) => {play_game(options);}
    
    
    const script = document.createElement('script');
    script.setAttribute("type","py");
    script.setAttribute("src", the_options.s + "?v=" + v_code);
    
    
    const xhttp = new XMLHttpRequest();

    xhttp.onload = function() {
        if (!(xhttp.readyState == 4 && xhttp.status == 200)){
            console.error(`TSP error fetching config: ${xhr.status}`);
            return;
        }
        const config_json = this.response;
        console.log("Loaded pyscript config", config_json);
        
        let target_config = {"files": {
            '{V}' : String(v),
            '{V_CODE}' : String(v_code),
            }
        };
        for (const [key1,val1] of Object.entries(config_json)){    
            if (key1 === "files"){
                for (const [keyf,valf] of Object.entries(val1)){
                    let valfp;
                    if (valf){
                        valfp = valf;
                    } else {
                        valfp = keyf.split("/").slice(-1)[0];
                    }
                    target_config["files"][keyf + '?v={V_CODE}'] = valfp;
                }
            } else {
                target_config[key1] = val1;
            }
        }
        console.log("Created target_config: ", target_config);
        script.setAttribute("config", JSON.stringify(target_config)); /// TODO
        let tps_pyscript = document.getElementById("tps-pyscript");
        if (!tps_pyscript){
            tps_pyscript = document.createElement("section");
            tps_pyscript.setAttribute("id","tps-pyscript");
            tps_pyscript.setAttribute("class", "pyscript");
            tps_pyscript.setAttribute("async","false");
            document.body.append(tps_pyscript);
            console.log('Added tps-pyscript:',tps_pyscript);
        }
        
        tps_pyscript.replaceChildren(script);
        console.log('Updated tps-pyscript:',tps_pyscript);

        import("https://pyscript.net/releases/2025.3.1/core.js").then((pscore) => {
                  
        
        // The `hooks.main` attribute defines plugins that run on the main thread.
        pscore.hooks.main.onReady.add((wrap, element) => {
            console.log("main", "onReady");
            console.debug("main", "wrap", wrap);
            //console.debug("main", "element", element);
            
        });
        
        pscore.hooks.main.onBeforeRun.add(() => {
            console.log("main", "onBeforeRun");
        });
        
        pscore.hooks.main.codeBeforeRun.add('print("main", "codeBeforeRun")');
        pscore.hooks.main.codeAfterRun.add('print("main", "codeAfterRun")');
        pscore.hooks.main.onAfterRun.add(() => {
            console.log("main", "onAfterRun");
        });


        
        let tps_pyscript_core_css = document.getElementById('tps-pyscript-core-css');
        if (!tps_pyscript_core_css){
                tps_pyscript_core_css = document.createElement('link');
                tps_pyscript_core_css.id='tps-pyscript-core-css';
                tps_pyscript_core_css.href='https://pyscript.net/releases/' + PYSCRIPT_CORE_VERSION + '/core.css';
                tps_pyscript_core_css.rel='stylesheet';
                tps_pyscript_core_css.type='text/css';
                (document.head||document.documentElement).appendChild(tps_pyscript_core_css);    
                console.log("Added Pyscript core CSS version ", PYSCRIPT_CORE_VERSION,  tps_pyscript_core_css);
         }
            });
        
    }
    xhttp.onerror = function(e){
        console.error("Couldn't fetch the config ", the_options.config_url);
        throw new Error(e);
    }

    xhttp.open("GET", the_options.config_url); 
    xhttp.responseType = "json";
    xhttp.send();
    
};


console.log("turtleps.js loaded");