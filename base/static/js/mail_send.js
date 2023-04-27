const dropZone = document.getElementById('dropZone');
const containerRect = dropZone.getBoundingClientRect();
let loadLottie = false;
let dropZone_hasFile = false;
const dropZone_base = document.getElementById('dropZone_base');
const success_lottie = document.getElementById('success-lottie');
const dropZone_progress = document.getElementById('dropZone_progress');
const dropZone_progress_obj = document.getElementById('dropZone_progress_obj');
const dropZone_fileBase = document.getElementById('dropZone_fileBase');
const pick_list = document.getElementById('pick_list');

getEmailFileNames(pick_list);


const successToast = document.getElementById('successToast');
const errorToast = document.getElementById('errorToast');

function showSuccesToast(message=''){
    successToast.querySelector('span').innerHTML = message;
    successToast.classList.remove('hidden');
  
    setTimeout(() => {
      successToast.classList.add('hidden');
    }, 3000);
  }
  
  function showErrorToast(message=''){
    errorToast.innerHTML = message;
    errorToast.classList.remove('hidden');
  
    setTimeout(() => {
      errorToast.classList.add('hidden');
    }, 3000);
  }

dropZone.addEventListener('dragover', function(event) {
    event.preventDefault();
    event.stopPropagation();

    if(!loadLottie)
    {
        loadLottie = true;
        dropZone_fileBase.style.display = 'none';
        dropZone_base.style.display = 'none';
        success_lottie.style.removeProperty('display');
        success_lottie.innerHTML = '';
        dropZone.classList.add('border-success');
        lottie.loadAnimation({
            container: document.getElementById('success-lottie'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            path: '../../static/img/success-lottie.json',
            rendererSettings: {
            preserveAspectRatio: 'xMidYMid meet',
            progressiveLoad: true,
            scaleMode: 'noScale',
            hideOnTransparent: true
            }
        });
    }
});

dropZone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    const pointerX = event.clientX;
    const pointerY = event.clientY;
  
    if (
      pointerX >= containerRect.left &&
      pointerX <= containerRect.right &&
      pointerY >= containerRect.top &&
      pointerY <= containerRect.bottom
    ) {
      return;
    } else {
        if(dropZone_hasFile){
            dropZone_fileBase.style.removeProperty('display');
            success_lottie.style.display = 'none';
            dropZone_base.style.display = 'none';
        }
        else{
            success_lottie.style.display = 'none';
            dropZone_base.style.removeProperty('display');
        }
        dropZone.classList.remove('border-success');
        loadLottie = false;
    }
});

dropZone.addEventListener('drop', function(event) {
  event.preventDefault();
  success_lottie.style.display = 'none';
  dropZone_base.style.removeProperty('display');
  dropZone.classList.remove('border-success');
  loadLottie = false;
  handleFiles(event.dataTransfer.files);
});

let fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = '*';
fileInput.multiple = true;

fileInput.addEventListener('change', function(event) {
    event.preventDefault();
    handleFiles(event.target.files);
});

dropZone.addEventListener('click', function(event) {
    if(dropZone_hasFile){
        return;
    }
    event.preventDefault();
    fileInput.click();
});


function handleFiles(files) {
    loadLottie = false;
    if (files.length === 0) {
        showErrorToast('Files can not found!');
        return;
    }

    dropZone_base.style.display = 'none';
    success_lottie.style.display = 'none';
    dropZone_progress.style.display = 'none';
    dropZone_fileBase.innerHTML = '';
    dropZone_fileBase.style.removeProperty('display');
    dropZone.classList.add('border-success');
    let remainingFiles = files.length;
    for(let i = 0; i < files.length; i++){
        dropZone_hasFile = true;
        var fileName = files[i].name;
        dropZone_fileBase.innerHTML += `<div class="flex flex-row justify-between items-center bg-base-200 rounded-xl"><div class="flex items-center space-x-2 mx-2"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="text-warning h-4 w-4"><title/><g id="Complete"><g id="F-File"><g id="Text"><g><path d="M18,22H6a2,2,0,0,1-2-2V4A2,2,0,0,1,6,2h7.1a2,2,0,0,1,1.5.6l4.9,5.2A2,2,0,0,1,20,9.2V20A2,2,0,0,1,18,22Z" fill="none" stroke="currentColor" id="File" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="17.5" y2="17.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="13.5" y2="13.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="8" x2="13" y1="9.5" y2="9.5"/></g></g></g></g></svg><div class="text-xs text-success">${fileName}</div></div><div><button class="btn btn-xs btn-circle btn-outline" id="remove_file_btn"><svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div></div>`;
    }
    const remove_file_btns = document.querySelectorAll('#dropZone_fileBase button[id="remove_file_btn"]');
    const removeFileBtns = document.querySelectorAll('#dropZone_fileBase button[id="remove_file_btn"]');
    removeFileBtns.forEach(function (removeFileBtn) {
      removeFileBtn.addEventListener('click', function () {
        remainingFiles--;
        removeFileBtn.parentElement.parentElement.remove(); // remove the parent element of the clicked button            
        if (remainingFiles === 0) {
            success_lottie.style.display = 'none';
            dropZone_base.style.removeProperty('display');
            dropZone.classList.remove('border-success');
            setTimeout(function(){
                dropZone_hasFile = false;
            }, 10);
        }
      });
    });

    console.log('file_pattern', files.pattern);

    // Your code to handle the selected files here
}

async function getEmailFileNames(pickList) {
    try {
      const response = await fetch('/tools/get_email_names/?' + new Date().getTime());
      response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate';
      response.headers['Pragma'] = 'no-cache';
      response.headers['Expires'] = '0';
      const data = await response.json();
  
      data.names.forEach(name => {
        if(name != 'Pick one'){
          const optionEl = document.createElement('option');
          optionEl.value = name;
          optionEl.textContent = name;
          pickList.appendChild(optionEl);
        }
      });
    } catch (error) {
      showErrorToast(error.toString());
    }
  }