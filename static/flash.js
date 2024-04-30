// flash.js
window.onload = function() {
    var flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.display = 'block';
        setTimeout(function() {
            flashMessage.style.display = 'none';
        }, 3000);
    }
};
