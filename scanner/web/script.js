// const img = document.getElementById('image');
// const baseSrc = 'http://staszek-pc:8000/stream/image.jpeg';
// let preloader = new Image();
// preloader.onload = function() {
//     img.src = preloader.src;
// };
// function loadNewImage() {
//     let newSrc = `${baseSrc}?r=${Math.random()}`;
//     preloader.src = newSrc;
// }
// setInterval(loadNewImage, 100)
// loadNewImage();
   

// kod Mai
function updateImage(imgElement) {

	// create/get preloader
	let preloader = imgElement._ourPreloader;
	if (!preloader)
	{
		preloader = new Image();
		imgElement._ourPreloader = preloader;
	    preloader.onload = function() {
	        imgElement.src = preloader.src;
	    };
	}

	// replace prevoius QS and append random 
	let src = imgElement.src;
    preloader.src = src.replace(/\?.*$/, "") + "?"+Math.random();
}

function loadNewImages() {
    const images = document.querySelectorAll('.mjpg'); 
    // console.log(images);
    images.forEach(img => updateImage(img));
}

setInterval(loadNewImages, 100);
loadNewImages();


