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

const baseSrc = 'http://staszek-pc:8000/stream/image.jpeg';
function updateImage(imgElement) {
    let preloader = new Image();
    preloader.onload = function() {
        imgElement.src = preloader.src;
    };
    let newSrc = `${baseSrc}?r=${Math.random()}`;
    preloader.src = newSrc;
}

function loadNewImages() {
    const images = document.querySelectorAll('.mjpg'); // Moved inside here!
    // console.log(images)
    images.forEach(img => updateImage(img));
}

setInterval(loadNewImages, 100);
loadNewImages();


