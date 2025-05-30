let path = '/api';

function getFileIcon(fileExtension) {

    let IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic', 'avif'];
    if (IMAGE_EXTENSIONS.includes(fileExtension)) {
        return '/static/img/image.png';
    }else{
        return '/static/img/file.png';
    };
}

function removeSpaces(path) {
    return path.replaceAll(' ', '%20');
}

function generateDirectoriesHTML(response,pathDirectory) {

    let htmlDirectories = '';
    let directories = response['directories'];
    for (let indexDirectory = 0; indexDirectory < directories.length; indexDirectory++) {

        const folder = directories[indexDirectory];
        const folderName = folder['name'];
        const haveDirectories = folder['isEmpty'];
        const sanitizedPath = removeSpaces(pathDirectory+'/'+folderName);
        htmlDirectories +=             `<div class="col text-center">
        <img onclick=refreshFiles("${sanitizedPath}") src="/static/img/${ haveDirectories === true ? 'folder_with_files.png' : 'open-folder.png' }" alt="Logo" width="55" height="55"
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
        <img src="${getFileIcon(files[indexDirectory]['name'].split('.').at(-1))}" alt="Logo" width="55" height="55"
            style="margin-top: 10px;">
        <h5 class="text-dracula fs-6 mt-2">${files[indexDirectory]['name']}</h5>
    </div>`;
        
    };
    return htmlDirectories;
}

function backDirectory(path) {
    if (path !== '/api') {    
        path = path.split('/');
        path.pop(); 
        return path.join('/');
       
    }
}

function refreshFiles(path_api='/api') {

    let navButton = document.getElementById('back_button'); 
    let htmlDirectories = '';
    path = path_api; 

    document.querySelector('input[type="search"]').value = path.replace('/api','');
    
    if (path !== '/api'){ 
        navButton.style.visibility = 'visible';
        navButton.onclick = () => refreshFiles(backDirectory(path));

    }else{
        navButton.style.visibility = 'hidden';
    };

    $.ajax({
        url: path_api,
        method:'GET',
        dataType: 'json',
        success: function (response) {

            let filesBody = document.getElementById('files_body');
            let directories = generateDirectoriesHTML(response,path);
            let files       = generateFilesHTML(response);
            
            htmlDirectories += directories + files;
            filesBody.innerHTML = htmlDirectories;
        }
    });

};

$(document).ready(function() {


    const socketio = io();
    refreshFiles();   

    socketio.on('new_files', (data) => {
        refreshFiles(path);
    });
    
});