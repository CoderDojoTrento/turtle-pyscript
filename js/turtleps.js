import { marked } from "./marked.esm.js";

console.log("Loading turtleps.js ...");


/**
 * A global mutable config to be shared with python - 
 * Don't like having global stuff but unfortunately as of 2025.3.1 pyscript
 * doesn't allow proper config reload.  
 * @since 0.12.0 
 */
export let tps_config = {
    tps : {
        
    }
};
/**
 * @since 0.10.0
 */
export const DAY = 1000*60*60*24; // as milliseconds
/**
 * @since 0.10.0
 */
export const PYSCRIPT_CORE_VERSION = "2025.3.1";

/**  ordered by importance first to last  
    
*/
export let DEFAULT_OPTIONS = {  s: '',
                                /**  py: pyodide  mpy: micropython */
                                t: 'py',  
                                /** version for everything */
                                v: 0,       
                                /** version for code */
                                vc: 0,
                                /** run number 
                                 * @since 0.12.0 */                              
                                r : 1,
                                refresh_buttons: true,
                                /** Suspends execution and shows a big play banner:
                                 * 
                                 *   -1: never
                                 *    0: right before executing python
                                 *    1: at the end of first ge_init call
                                 *
                                 *  ignored when r > 1
                                 *
                                 *  @since 0.12.0
                                */    
                                play_banner: -1,
                                show_game: true,
                                /** only available in run_from_params */   
                                navbar: true,   
                                /** puts control panel high and expands it */
                                sticky: false,  
                                show_desc: true,
                                /** @since 0.12.0 */
                                show_options: true,
                                config_url : "pyscript.json",
                                cache_expiration : DAY * 60
                                // mode: 'dev', // allowed: 'dev' or 'demo' // not neededd for now 
}

/** @since 0.10.0

Awaits event on given target only *once*
*/
// https://www.reddit.com/r/learnjavascript/comments/19alv5n/what_would_be_bestpractice_to_wait_until_2_events/
export async function when(target, event, {
  signal, capture, passive, 
} = {}) {
  const { promise, resolve } = Promise.withResolvers();
  target.addEventListener(event, resolve, { once: true, signal, capture, passive });
  return promise;
}


console.log("Patching console.error to catch TPS-STOPEX CancelledError");

/** @since 0.10.0
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





/**  
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


/** 
    s: script relative path,  must NOT have parameters

   @since 0.11.0
*/
export function sep_title_desc(s, raw_string){
    const sname = s.substring("test/".length, s.length - ".py".length);
    const rsp = raw_string.trim();
    const i = rsp.indexOf('\n'); 
    let title = '';
    let descr = '';
    
    if (i == -1){
        title = rsp.trim();
        descr = '';
    } else {
        title = rsp.substring(0,i).trim();
        descr = rsp.substring(i+1).trim();
    }
    if (title.trim().length === 0){
        title = sname;
    }
    
    return [title, descr];    
}

/**
    @since 0.12.0
*/
export async function fetch_title_desc(s){
    
    const response = await fetch(s);  // TODO would need version, but I guess it's still good enough
    
    let d = '';
    if (!response.ok) {
        console.error("Couldn't fetch test:" + s, response);
    } else {
        const t = await response.text();
        const re = /^\s*"""(.*?)"""/gs;
        let arr = re.exec(t);
        
        if (!arr || arr.length < 2) {
            console.log("Couldn't find test description");    
        } else {
            d = arr[1];
        }
        
    }
    return sep_title_desc(s, d);
}



/**
    @since 0.11.0
*/
async function show_desc(s){

    const [title, desc] = await fetch_title_desc(s);
            
    const st = document.querySelector(".tps-script-title");
    if (st){
        st.innerHTML = `<a href="${s}" target="_blank">${title}</a>`
    }
    const sd = document.querySelector(".tps-script-description");
    if (sd){    
        sd.innerHTML = marked.parse(desc);
    }

}

/** 
 * r: the run number
 * @since 0.12.0
 */
export async function show_play_banner(play_banner, r){
    if (play_banner === -1){
        console.debug("play_banner flag is", play_banner, "not showing it");
        return;
    }
    if ((play_banner >= 0) && (r > 1)){
        console.debug("r is", r, "not showing play_banner");
        return;
    }

    const loading         = document.querySelector('#tps-game-box .tps-loading');
    const play_banner_button = document.querySelector('#tps-game-box .tps-play-banner');
    const play_button     = document.querySelector("#tps-game-box .tps-play");
    
    // TODO reload_button for now is just disabled, it would be more logical to actually interrupt this funciton and refresh
    const reload_button     = document.querySelector("#tps-game-box .tps-reload");
    
    console.log("Waiting player click on play panel / play / reload...")

    loading.style.visibility = 'hidden';
    play_banner_button.style.visibility = 'visible';
    
    let old_play_click = play_button.onclick;     
    play_button.onclick = null;

    let old_reload_click = reload_button.onclick;     
    reload_button.onclick = null;

    await Promise.any([when(play_banner_button, "click"), 
                       when(play_button, "click"),
                       when(reload_button, "click"),
]);

    console.debug("Restoring play onclicks...")

    play_button.onclick   = old_play_click;
    reload_button.onclick   = old_reload_click;

    if (play_banner === 0){
        loading.style.visibility = 'visible';
    } else if (play_banner === 1){
        loading.style.visibility = 'hidden';
    } else {
        console.error("Found invalid play_banner value:", play_banner);
    }
    play_banner_button.style.visibility = 'hidden';

}

/** Runs a script given by page parameter s 

     * !!!!!!!   WARNING    !!!!!!!!
     * 
     * THIS FUNCTION ALLOWS UNTRUSTED USERS TO RUN ANY .py FILE PRESENT IN demo/ OR test/ FOLDERS
     * 
     * @since 0.10.0
*/
export async function run_from_params(){
    
    let page_name = window.location.pathname.split("/").slice(-1)[0]; 
    console.log("page_name", page_name);
    if (page_name !== "demo.html" && page_name !== "test.html" ){
        throw new Error("run_param function can only be called from demo.html or test.html pages, found instead: " + window.location.href);
    }


    let the_options = Object.assign({}, DEFAULT_OPTIONS);
    const params = new URLSearchParams(window.location.search);
    
    let game_box = document.getElementById("tps-game-box");
    let msg_box = game_box ? game_box : document.body;
    let options_box = document.getElementById("tps-options-box");

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
        the_options.play_banner = 1;  // show play_banner at the end of ge_init
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

    if (s.includes("/uitests_")){   
        console.log("Found uitests suite, making sticky.");    
        the_options.sticky = true;
        the_options.show_game = false;
    } else if (s.includes("/uitest_") || s.includes("/stresstest_") ||subdir == "demo") {
        if (!the_options.show_desc){
            console.debug("show_desc is false, skipping description.");    
        } else {
            let script_doc = null;
            let script_title = null;
            let script_description = null;
            const game_area = document.getElementById('tps-game-area');
            if (game_area){
                script_doc = game_area.querySelector('.tps-script-doc');
                script_title = game_area.querySelector('.tps-script-title');
                script_description = game_area.querySelector('.tps-script-description');
            }
            if (!script_doc){
                script_doc = document.createElement('div');
                script_doc.classList.add("tps-script-doc");
                game_area.prepend(script_doc);
            }

            if (!script_title){
                script_title = document.createElement('h1');
                script_title.classList.add("tps-script-title");
                script_doc.appendChild(script_title);
            }
            if (!script_description){
                script_description = document.createElement('div');
                script_description.classList.add("tps-script-description");
                script_doc.appendChild(script_description);
            }
            
            await show_desc(s);
        }
    }

    const bold_span = 'style="font-weight:bold"';

    options_box.innerHTML = `
        <div class="tps-intepreter">
            <input type="radio" name="tps-interpreter" value="py" ${the_options.t==="py"? "checked" : ""}>
            <label for="py"><a href="#">pyodide</a></label><span ${the_options.t==="py"? bold_span : ""}><a href="#">slow loading, supports almost all Python features</a></span>
            <input type="radio" name="tps-interpreter" value="mpy" ${the_options.t==="mpy"? "checked" : ""}>
            <label for="mpy"><a href="#">micropython</a></label><span ${the_options.t==="mpy"? bold_span : ""}><a href="#">fast loading but supports few Python features (may give weird errors)</a></span>
        </div>
    `
    options_box.style.display = the_options.show_options ? "block" : "none";

    const what = the_options.t === "py" ? "mpy" : "py";  
    let options_box_input = document.querySelector(`#tps-options-box input[value="${what}"]`);
    let options_box_label = document.querySelector(`#tps-options-box label[for="${what}"]`);
    let options_box_span = document.querySelector(`#tps-options-box label[for="${what}"] + span`);

    const frel = (e) => {reload_page(Object.assign({}, the_options, {t:what}));}    // fresh restart
    
    options_box_input.onclick = frel;   
    options_box_label.onclick = frel;
    options_box_span.onclick = frel;
    

        
    await run(the_options);
}
/** 
 * Updates ui game status
 * @since 0.10.0
 */
function update_ui_game_status(game_status){
    
    let play_button_img = document.querySelector("#tps-game-box .tps-play img");
    let stop_button = document.querySelector("#tps-game-box .tps-stop img");
    let screen  = document.querySelector("#tps-game-box .tps-screen");
    
    
    if (game_status === "PLAY"){
        if (play_button_img){
            play_button_img.classList.add('tps-ctrl-pressed');
        }
        if (stop_button){
            stop_button.classList.remove('tps-ctrl-pressed');
        }
        if (screen){
            screen.classList.remove('tps-screen-stopped');
        }
    } else if (game_status === "STOP") {
        if (play_button_img){
            play_button_img.classList.remove('tps-ctrl-pressed');
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

/** @since 0.10.0
*/
export async function stop_game(options){
    console.log("turtleps.js:  stop_game()");

    console.log("Stopping python scripts...");

    let the_options = Object.assign({}, DEFAULT_OPTIONS, options);

    const script = document.createElement('script');
    script.setAttribute("type",the_options.t);         
    script.textContent = "import turtleps\n"
                        + "turtleps.ge_stop()\n"
    
    const tps_pyscript = document.getElementById("tps-pyscript");
    tps_pyscript.appendChild(script);
    await when(window, the_options.t + ":done");
    update_ui_game_status("STOP"); // TODO sync with module
    console.log("turtleps.js:  stop_game() is DONE.");
    
};


/** @since 0.10.0
*/
export async function play_game(options){

    console.log("turtleps.js:  play_game(", options, ")");
    
    update_ui_game_status("PLAY"); // TODO sync with module
    
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options);

    await stop_game(options);

    
    update_ui_game_status("PLAY"); // TODO sync with module
    
    console.log("Resetting python memory...");

    const script = document.createElement('script');
    script.setAttribute("type",the_options.t);         
    script.textContent = "import turtleps\n"
                        + "turtleps.ge_reset()\n"
    
    const tps_pyscript = document.getElementById("tps-pyscript");
    tps_pyscript.appendChild(script);
    await when(window, the_options.t + ":done");
    console.log("Going to reload script...", the_options.s);
    the_options.r += 1;
    await run(the_options);
    console.log("turtleps.js:  play_game() is DONE.");
};



/** @since 0.10.0
*/
export async function reload (options){

    console.log("turtleps.js:  reload(", options, ")");
    
    let what = 'tps_vc';
    try {
        console.log("Clearing ", what, " from local storage..");
        window.localStorage.removeItem(what);            
    } catch (e){
        console.info("Failed to clear " , what, " from localStorage. Reason:", e);
    }

    const current_time = new Date().getTime();  // milliseconds since 1970
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options, {vc:current_time});    
    await play_game(the_options);
    console.log("turtleps.js:  reload() is DONE.");
};


/** @since 0.10.0
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
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options, {v : current_time, 
                                                                   vc: DEFAULT_OPTIONS.vc})
    the_options.r += 1;

    console.log('the_options:', the_options)

    reload_page(the_options);
}

/**
 * @since 0.12.0 
 */
export function reload_page(options){
    console.log("turtleps.js:  reload_page(", options, ")");

    let the_options = Object.assign({}, DEFAULT_OPTIONS, options);

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

/** @since 0.10.0
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

/** @since 0.10.0
*/
function load_timestamp(what, current_time){
    let local_v;
    try {
        console.log("Loading ", what, " from local storage..");
        const local_v_raw = window.localStorage.getItem(what);
        if (local_v_raw === null){
            console.log("Couldn't find ", what," in local storage");
            local_v = current_time;
        } else {
            local_v = Number(local_v_raw);
        }
    } catch (e){
        console.info("Failed to load ",what,". Reason:", e);
        local_v = current_time;
    }
    return local_v
}

/** failed attempt at config rewriting

   note to myself: attempted to run a Python script to update files,
   approach seemed to work  but apparently it was generating too many concurrent events
*/
async function config_overwrite_TODO(wrap, target_config, the_options){

    console.log("!!!!! PROVA BEGIN");
`
    //console.debug("main", "element", element);
    const loc = window.location.pathname.split('?')[0];
    const cur_path = loc.substring(0, loc.lastIndexOf("/")+1);



    console.log("!!!! updated_urls:")
    
    for (const [url, modname] of Object.entries(target_config["files"])){
    
    with open(modname, "w") as targetf:
        if ".py" in url:
            
            nurl = "${cur_path}" + url
            print("OVERWRITING...", modname, "with", nurl)
            
            response = await js.fetch(nurl)
            if not response.ok:
                print("ERROR! response.status:", response.status)
            else:
                targetf.write(await response.text())

            print("DONE OVERWRITING", modname)
`       
    console.log("!!!!! PROVA END");
}

/**
    @since 0.12.0
*/
function on_py_ready(){ 
    _on_python_ready('py');
}

/**
    @since 0.12.0
*/
function on_mpy_ready(){ 
    _on_python_ready('mpy');
}

/**
    @since 0.12.0
*/
function _on_python_ready(script_type){ 
    console.log(script_type + ':ready, updating ui game status...')

    const loading  = document.querySelector('#tps-game-box .tps-loading');
    const screen   = document.querySelector('#tps-game-box .tps-screen');
    
    loading.style.visibility = 'hidden';
    screen.classList.remove('tps-screen-loading');
    update_ui_game_status("PLAY"); // TODO sync with module
}


/** Runs a script from script_path
 * 
 * @since 0.9.0
 */
export async function run(options){
    
    let the_options = Object.assign({}, DEFAULT_OPTIONS, options);
    
    console.log( "Requested running: ", the_options.s, 
                "\n- at timestamp: ",   the_options.vc,
                "\n- r:",            the_options.r);
    
    console.log("the_options:", the_options);

    const current_time = new Date().getTime();  // milliseconds since 1970

    let local_v      = load_timestamp('tps_v',      current_time);
    let local_vc = load_timestamp('tps_vc', current_time);
    
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
                <div class="tps-play-banner">
                    <img title="Play!" width="200px" src="img/play.svg"/>
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
    
    const loading  = document.querySelector('#tps-game-box .tps-loading');
    const screen   = document.querySelector('#tps-game-box .tps-screen');
    const play_banner_button = document.querySelector('#tps-game-box .tps-play-banner');
    
    screen.classList.add("tps-screen-loading");
    loading.style.visibility = 'visible';
    play_banner_button.style.visibility = 'hidden';

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
    if (the_options.t === "py"){
        addEventListener('py:ready', on_py_ready);
    } else if (the_options.t === "mpy"){
        addEventListener('mpy:ready', on_mpy_ready);
    } else {
        throw new Error("Unrecognized script type:", the_options.t);
    }


    the_options.v = determine_timestamp(the_options.v, local_v, current_time, the_options.cache_expiration);
    console.log("Will use timestamp v=", the_options.v);

    the_options.vc = determine_timestamp(the_options.vc, local_vc, current_time, the_options.cache_expiration);
    console.log("Will use timestamp vc=", the_options.vc);

    try {
        console.log("Saving timestamp to local storage..");
        window.localStorage.setItem("tps_v", the_options.v);
        console.log("Saving code timestamp to local storage..");
        window.localStorage.setItem("tps_vc", the_options.vc);
        
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
    script.setAttribute("type", the_options.t);
    script.setAttribute("src", the_options.s + "?v=" + the_options.vc);
    

    const xhttp = new XMLHttpRequest();

    xhttp.onload = async function() {
        if (!(xhttp.readyState == 4 && xhttp.status == 200)){
            console.error(`TSP error fetching config: ${xhr.status}`);
            return;
        }
        const config_json = this.response;
        console.log("Loaded pyscript config", config_json);
        
        for (const prop of Object.getOwnPropertyNames(tps_config)) {
            delete tps_config[prop];
        }

        tps_config["tps"] = {};
        tps_config["files"] = {};

        for (const [key1,val1] of Object.entries(config_json)){    
            if (key1 === "files"){
                for (const [keyf,valf] of Object.entries(val1)){
                    let valfp;
                    if (valf){
                        valfp = valf;
                    } else {
                        valfp = keyf.split("/").slice(-1)[0];
                    }
                    tps_config["files"][keyf + '?v=' + String(the_options.vc)] = valfp;
                }
            } else {
                tps_config[key1] = val1;
            }
        }

        for (const [key,val] of Object.entries(the_options)){
            tps_config["tps"][key] = val;
        }

        console.log("Created tps_config: ", tps_config);
        script.setAttribute("config", JSON.stringify(tps_config)); /// TODO
        let tps_pyscript = document.getElementById("tps-pyscript");
        if (!tps_pyscript){
            tps_pyscript = document.createElement("section");
            tps_pyscript.setAttribute("id","tps-pyscript");
            tps_pyscript.setAttribute("class", "pyscript");
            tps_pyscript.setAttribute("async","false");
            document.body.append(tps_pyscript);
            console.log('Added tps-pyscript:',tps_pyscript);
        }
        
        if (the_options.play_banner === 0){
            await show_play_banner(the_options.play_banner, the_options.r);
            tps_pyscript.replaceChildren(script);

        } else {
            tps_pyscript.replaceChildren(script);

        }

    
        console.log('Updated tps-pyscript:',tps_pyscript);

        
        import(`https://pyscript.net/releases/${PYSCRIPT_CORE_VERSION}/core.js`)
        .then((pscore) => {
            console.log("pscore:", pscore);
            if (the_options.r === 1){
                // The `hooks.main` attribute defines plugins that run on the main thread.
                pscore.hooks.main.onReady.add(async (wrap, element) => {
                    console.log("main", "onReady");
                    console.debug("main", "wrap", wrap);
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
                        tps_pyscript_core_css.href=`https://pyscript.net/releases/${PYSCRIPT_CORE_VERSION}/core.css`;
                        tps_pyscript_core_css.rel='stylesheet';
                        tps_pyscript_core_css.type='text/css';
                        (document.head||document.documentElement).appendChild(tps_pyscript_core_css);    
                        console.log("Added Pyscript core CSS version ", PYSCRIPT_CORE_VERSION,  tps_pyscript_core_css);
                }
            };
        });
    }
    
    xhttp.onerror = function(e){
        console.error("Couldn't fetch the config ", the_options.config_url);
        throw new Error(e);
    }

    xhttp.open("GET", the_options.config_url); 
    xhttp.responseType = "json";
    xhttp.send();
    await when(window, the_options.t + ":ready");
    console.log("turtleps.js run(): py:ready()");
    await when(window, the_options.t + ":done");                                                
    console.log("turtleps.js run() is DONE: script=", the_options.s, "\n - asyncio tasks can still be running...")
};


console.log("turtleps.js loaded");