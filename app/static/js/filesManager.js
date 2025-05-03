function getFileIcon(fileExtension) {

    let IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic', 'avif'];
    if (IMAGE_EXTENSIONS.includes(fileExtension)) {
        return '/static/img/image.png';
    }else{
        return '/static/img/file.png';
    };
}

function  refreshFiles() {
    
    $.ajax({
        url:'/api/',
        method:'GET',
        datatype: 'json',
        success: function (response) {

            let files_body = document.getElementById('files_body');
            let directories = response['directories'];
            let files       = response['files'];
            let html_directories = '';
            for (let index_directory = 0; index_directory < directories.length; index_directory++) {
                html_directories +=             `<div class="col text-center">
                <img src="/static/img/folder.png" alt="Logo" width="55" height="55"
                    style="margin-top: 10px;">
                <h5 class="text-dracula fs-6 mt-2">${directories[index_directory]}</h5>
            </div>`;
                
            };
            for (let index_directory = 0; index_directory < files.length; index_directory++) {
                html_directories +=             `<div class="col text-center">
                <img src="${getFileIcon(files[index_directory].split('.').at(-1))}" alt="Logo" width="55" height="55"
                    style="margin-top: 10px;">
                <h5 class="text-dracula fs-6 mt-2">${files[index_directory]}</h5>
            </div>`;
                
            };
            

            files_body.innerHTML = html_directories;
        }
    });
};

$(document).ready(function() {

    const socketio = io();
    refreshFiles();   

    socketio.on('new_files', (data) => {
        refreshFiles();    
    });
    
});