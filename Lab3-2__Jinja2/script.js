function show_content() {
    document.getElementById('container').style.opacity = 1;
    document.getElementById('container').style.zoom = 1;
    but = document.getElementById('show_button');
    but.parentNode.removeChild(but);
}