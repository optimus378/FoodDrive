function formatrawinput() {
    var $textarea = document.getElementById('rawinput');
    $textarea.addEventListener('input', function () {
       // $textarea.value = $textarea.value.replace(/[^\w\s]/gi, '');
        $textarea.value = $textarea.value
                                       .replace(/[^\w\s]/gi, '')
                                       .replace(/[\n\r]+/g, "")
                                       .replace(/(.{10})/g, "$1\n");

    });
}
formatrawinput();



function formatscrubbed() {
    var $textarea = document.getElementById('scrubbed');
    $textarea.addEventListener('input', function () {
       // $textarea.value = $textarea.value.replace(/[^\w\s]/gi, '');
        $textarea.value = $textarea.value
                                       .replace(/[^\w\s]/gi, '')
                                       .replace(/[\n\r]+/g, "")
                                       .replace(/(.{10})/g, "$1\n");

    });
}
formatscrubbed();
