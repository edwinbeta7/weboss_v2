function ajustarAncho(elemento) {
    elemento.style.width = (elemento.value.length + 1) + 'ch';
}

// Llamar a la función inicialmente para ajustar el tamaño al texto por defecto
ajustarAncho(document.getElementById('rutafile'));


