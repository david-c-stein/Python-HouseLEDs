var file = [], p = true;

function upload(blobOrFile) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', false);
    xhr.onload = function(e) { };
    xhr.send(blobOrFile);
}

function process() {
    for (var j = 0; j <file.length; j++) {
        var blob = file[j];

        //const BYTES_PER_CHUNK = 1024 * 1024;  // 1MB chunk sizes.
        const BYTES_PER_CHUNK = 16 * 1024;    // 16kB chunk sizes.
        const SIZE = blob.size;

        var start = 0;
        var end = BYTES_PER_CHUNK;

        while (start < SIZE) {
            var chunk = blob.slice(start,end);
            upload(chunk);
            start = end;
            end = start + BYTES_PER_CHUNK;
        }
        p = ( j = file.length - 1) ? true : false;
        self.postMessage(blob.name + " Uploaded Succesfully");
    }
}


self.onmessage = function(e) {
    for (var j = 0; j < e.data.files.length; j++)
        file.push(e.data.files[j]);

    if (p) {
        process()
    }
}
