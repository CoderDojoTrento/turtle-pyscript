


export function vectorize(work_img, target) {
    /*  
        Traces the svg silhouette of the given work_img and puts 
        the result into target node innerHTML

        @return a canvas with the silhouette
        @since 0.9.0 
    */

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

export function getQueryVariable(variable){
    /* @since 0.9.0 */
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
            var pair = vars[i].split("=");
            if(pair[0] == variable){return pair[1];}
    }
    return false;
};


export function run(){
    let b = getQueryVariable('banner')
    if (b){
        //console.log('banner', b);
        if (b === 'false'){
            document.getElementById('banner').style.display = 'none';
        }
    }

    const loading = document.getElementById('loading');

    loading.show();

    const s = getQueryVariable('s');
    if (!s){
        loading.innerHTML = "Please select a script to run.";   
    } else {
        const re = /(test\/|demo\/)[a-zA-Z0-9_/]+\.py/;
        let arr = re.exec(s);
        //console.log(arr);
        if (!arr || ( arr.length == 0 || arr[0].length !== s.length)){
            loading.innerHTML = "ERROR: WRONG PAGE PARAMETERS! <br><br> SEE CONSOLE FOR MORE INFO.";    
            throw new Error("Got wrong script url parameter:" + s + "it must respect this regex:" + re);
        }

        let mode = s.substring(0,4);

        console.log("MODE:", mode);

        addEventListener('py:ready', () => loading.close());

        const script = document.createElement('script');
        script.setAttribute("type","py");
        script.setAttribute("src", s);
        //config is already prefetched by dumb tag in the body
        //script.setAttribute("config", "pyscript-test.json");

        const tps_pyscript = document.getElementById("tps-pyscript");
        console.log("Loading ", s);
        //console.log('script:', script);
        tps_pyscript.appendChild(script);
    }  

};


console.log("turtleps.js loaded");