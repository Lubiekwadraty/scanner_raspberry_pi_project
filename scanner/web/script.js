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
// Aspekt: Pobieranie danych z /api/parameters i wstianie do inputów
// -----------------------------------------------------------------

// TODO

// -----------------------------------------------------------------
// Aspekt: Zapięcie się na inputach i przy zmianie POST na /api/parameters
// -----------------------------------------------------------------

// TODO

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
