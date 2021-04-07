Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-dropzone", {
    url: "upload/",
    maxFiles: 2,
    maxFilessize: 5,
    acceptedFiles: '.png, .jpg, .jpeg',
})