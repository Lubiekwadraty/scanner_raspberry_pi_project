// -----------------------------------------------------------------
// Aspekt: semi mjpeg
// -----------------------------------------------------------------

// kod Mai
function updateImage(imgElement) {
  // create/get preloader
  let preloader = imgElement._ourPreloader;
  if (!preloader) {
    preloader = new Image();
    imgElement._ourPreloader = preloader;
    preloader.onload = function () {
      imgElement.src = preloader.src;
    };
  }

  // replace prevoius QS and append random
  let src = imgElement.src;
  preloader.src = src.replace(/\?.*$/, "") + "?" + Math.random();
}

function loadNewImages() {
  const images = document.querySelectorAll(".mjpg");
  // console.log(images);
  images.forEach((img) => updateImage(img));
}

setInterval(loadNewImages, 250);
loadNewImages();

// -----------------------------------------------------------------
// Aspekt: Pobieranie danych z /api/parameters i wstawianie do inputów
// -----------------------------------------------------------------

let input = document.querySelectorAll('input')
let appParams = {}
async function getAppParams() {
	try {
    	const response = await fetch("/api/parameters");
    	if (!response.ok) throw new Error(`Response status: ${response.status}`);
    	appParams = await response.json();
		params()
		inInput()
	} catch (error) {
    console.error(error.message);
  }
}
getAppParams()
function params(){
	let label = document.querySelectorAll('.appParams li label')
	let span = document.querySelectorAll('.appParams li span')
	let keys = Object.keys(appParams)
	let values = Object.values(appParams)
	for(let i = 0; i < 5; i++){
		label[i].innerHTML =keys[i]
		span[i].innerHTML = ": " + values[i]
	}
}

function inInput(){
	input.forEach(element => {
		if(element.type == 'checkbox'){
			element.checked = appParams[element.name]
      return
		}
		if(element.type =='submit') return
		if(appParams[element.name] == null) return
		if(element.type == 'hidden') return;
		element.value = appParams[element.name]
	});
}

// function checkbox(){
//   let checkboxes = document.querySelectorAll('input[type="checkbox"]')
//   checkboxes.forEach(checkbox => {
//     if(checkbox.checked){
//       checkbox.value = 'True'
//     }  
//     else{
//       checkbox.value = 'False'
//     }
//   });
// }


// function updateParams() {
// 	console.log(document.querySelectorAll("[app-params]"))
//   	document.querySelectorAll("[app-params]").forEach((e) => {
//     let s = e.getAttribute("app-params");
// 	console.log("s: ", s)
//     s = eval(s);
//     e.innerHTML = s;
//   });
// }
// getAppParams()
// setInterval(getAppParams, 500);


// -----------------------------------------------------------------
// Aspekt: Zapięcie się na inputach i przy zmianie POST na /api/parameters
// -----------------------------------------------------------------

async function send(form){

  // collect form -> JSON
  let appConfig = {}
  let inputs = form.querySelectorAll('input')
  inputs.forEach(input => {

	// protect agains property overwrites 
	if (input.name in appConfig) return;
	  
    if (input.type == 'checkbox')
    {
    	if (input.checked) appConfig[input.name] = input.value;
		return;
	}
    
    appConfig[input.name] = input.value
  });

  try{
    const response = await fetch("/api/parameters", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(appConfig)
    });
    const result = await response.json()
    console.log(result)
  }catch (e){
    console.error(e)
  }
}

const form = document.querySelector('form');

form.addEventListener('submit', function(event) { send(this); event.preventDefault(); })
form.addEventListener('change', function(event) { send(this); });
form.addEventListener('keyup', function(event) { send(this); });

// -----------------------------------------------------------------
// Aspekt: Pobieranie danych z /api/info i wstianie na stronę
// -----------------------------------------------------------------

let appInfo = {};

async function getAppInfo() {
  try {
    const response = await fetch("/api/info");
    if (!response.ok) throw new Error(`Response status: ${response.status}`);
    appInfo = await response.json();
    updateView();
  } catch (error) {
    console.error(error.message);
  }
}

function updateView() {
  document.querySelectorAll("[data-app-info]").forEach((e) => {
    let s = e.getAttribute("data-app-info");
    s = eval(s);
    e.innerHTML = s;
  });
}

getAppInfo();
setInterval(getAppInfo, 500);
