
let path = '';

function getFileIcon(fileExtension) {

    let IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic', 'avif'];
    if (IMAGE_EXTENSIONS.includes(fileExtension)) {
        return '/static/img/image.png';
    }else{
        return '/static/img/file.png';
    };
}


function generateDirectoriesHTML(response,pathDirectory) {

    let htmlDirectories = '';
    let directories = response['directories'];
    for (let indexDirectory = 0; indexDirectory < directories.length; indexDirectory++) {

        const folder = directories[indexDirectory];
        const folderName = Object.keys(folder)[0];
        const haveDirectories = Object.values(folder)[0];

        htmlDirectories +=             `<div class="col text-center">
        <img onclick=refreshFiles("/api${pathDirectory}/${folderName}") src="/static/img/${ haveDirectories === true ? 'folder_with_files.png' : 'open-folder.png' }" alt="Logo" width="55" height="55"
            style="margin-top: 10px;">
        <h5 class="text-dracula fs-6 mt-2">${folderName}</h5>
    </div>`;
        
    };
    
    return htmlDirectories;
}

function generateFilesHTML(response) {
    
    let htmlDirectories = '';
    let files       = response['files'];
    for (let indexDirectory = 0; indexDirectory < files.length; indexDirectory++) {
        htmlDirectories +=             `<div class="col text-center">
        <img src="${getFileIcon(files[indexDirectory].split('.').at(-1))}" alt="Logo" width="55" height="55"
            style="margin-top: 10px;">
        <h5 class="text-dracula fs-6 mt-2">${files[indexDirectory]}</h5>
    </div>`;
        
    };
    return htmlDirectories;
}

function  refreshFiles(path_api='/api') {
   
    if (path === ''){
        path = path_api;
    };

    $.ajax({
        url: path_api,
        method:'GET',
        dataType: 'json',
        success: function (response) {

            let filesBody = document.getElementById('files_body');
            let htmlDirectories = '';
            let pathDirectory = response['path'].includes('//') === true ? response['path'].replace('//', '/') : response['path'];
            let directories = generateDirectoriesHTML(response,pathDirectory);
            let files       = generateFilesHTML(response);
            
            htmlDirectories += directories + files;
            filesBody.innerHTML = htmlDirectories;
        }
    });

    if (path_api){
        path = path_api;
    }
};

$(document).ready(function() {


    const socketio = io();
    refreshFiles();   

    socketio.on('new_files', (data) => {
        refreshFiles(path);
        console.log("Valor de la path: " + path);
    });
    
});