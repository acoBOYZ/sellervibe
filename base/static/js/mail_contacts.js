const checkbox = document.getElementById("1_checkbox");

const c_1 = document.getElementById("c_1");
const n_1 = document.getElementById("n_1");
const cb_1 = document.getElementById("cb_1");

const c_2 = document.getElementById("c_2");
const n_2 = document.getElementById("n_2");
const cb_2 = document.getElementById("cb_2");
const bb_2 = document.getElementById("bb_2");
const r_2_1 = document.getElementById("r_2_1");
const r_2_2 = document.getElementById("r_2_2");

const c_3 = document.getElementById("c_3");
const n_3 = document.getElementById("n_3");
const cb_3 = document.getElementById("cb_3");
const bb_3 = document.getElementById("bb_3");
const fi_3 = document.getElementById("fi_3");
const ff_3 = document.getElementById("ff_3");

const c_4 = document.getElementById("c_4");
const n_4 = document.getElementById("n_4");
const cb_4 = document.getElementById("cb_4");
const bb_4 = document.getElementById("bb_4");
const sc_4_1 = document.getElementById("sc_4_1");
const sc_4_2 = document.getElementById("sc_4_2");
const sc_4_3 = document.getElementById("sc_4_3");

const c_5 = document.getElementById("c_5");
const n_5 = document.getElementById("n_5");
const cb_5 = document.getElementById("cb_5");
const bb_5 = document.getElementById("bb_5");
const rc_5_1 = document.getElementById("rc_5_1");
const rc_5_2 = document.getElementById("rc_5_2");
const rb_5_1 = document.getElementById("rb_5_1");
const rb_5_2 = document.getElementById("rb_5_2");
const tb_5_1 = document.getElementById("tb_5_1");
const tb_5_2 = document.getElementById("tb_5_2");


function getFileExtension(e) { 
  e.stopPropagation();
  e.preventDefault();
  e.dataTransfer.dropEffect = 'copy';
  
  for(var i = 0; i < e.dataTransfer.items.length; i++)
  {
      return e.dataTransfer.items[i].type;
  }
}

checkbox.addEventListener("change", function() {
  if (this.checked) {
    cb_1.removeAttribute("disabled");
  } else {
    cb_1.setAttribute("disabled", "disabled");
  }
});


cb_1.addEventListener("click", function(){
  const inner = '<svg width="32" height="32" viewBox="0 0 20 20"><path id="Path_11514" data-name="Path 11514" d="M10,0A10,10,0,1,1,0,10,10,10,0,0,1,10,0Z" fill="#C6F6D5"></path><path id="Path_11516" data-name="Path 11516" d="M0,0H12V12H0Z" transform="translate(4 4)" fill="none"></path><path id="Path_11517" data-name="Path 11517" d="M6.4,11.1l-1.75-1.75a.495.495,0,0,0-.7.7l2.1,2.1a.5.5,0,0,0,.7,0l5.3-5.3a.495.495,0,0,0-.7-.7Z" transform="translate(2.096 0.996)" fill="#22543D"></path></svg>';
  n_1.innerHTML = inner;

  c_1.classList.remove("collapse-open");
  c_1.classList.add("collapse-close");
  c_1.classList.remove("collapse-arrow");
  c_1.classList.add("opacity-50");

  c_2.classList.remove("opacity-50");
  c_2.classList.add("collapse-arrow");
  c_2.classList.remove("collapse-close");
  c_2.classList.add("collapse-open");
});

bb_2.addEventListener("click", function(){
  const inner = '<p class="text-base">1</p>';
  n_1.innerHTML = inner;

  c_1.classList.add("collapse-open");
  c_1.classList.remove("collapse-close");
  c_1.classList.add("collapse-arrow");
  c_1.classList.remove("opacity-50");

  c_2.classList.add("opacity-50");
  c_2.classList.remove("collapse-arrow");
  c_2.classList.add("collapse-close");
  c_2.classList.remove("collapse-open");
});

cb_2.addEventListener("click", function(){
  const inner = '<svg width="32" height="32" viewBox="0 0 20 20"><path id="Path_11514" data-name="Path 11514" d="M10,0A10,10,0,1,1,0,10,10,10,0,0,1,10,0Z" fill="#C6F6D5"></path><path id="Path_11516" data-name="Path 11516" d="M0,0H12V12H0Z" transform="translate(4 4)" fill="none"></path><path id="Path_11517" data-name="Path 11517" d="M6.4,11.1l-1.75-1.75a.495.495,0,0,0-.7.7l2.1,2.1a.5.5,0,0,0,.7,0l5.3-5.3a.495.495,0,0,0-.7-.7Z" transform="translate(2.096 0.996)" fill="#22543D"></path></svg>';
  n_2.innerHTML = inner;

  c_2.classList.remove("collapse-open");
  c_2.classList.add("collapse-close");
  c_2.classList.remove("collapse-arrow");
  c_2.classList.add("opacity-50");

  c_3.classList.remove("opacity-50");
  c_3.classList.add("collapse-arrow");
  c_3.classList.remove("collapse-close");
  c_3.classList.add("collapse-open");

  const inner_r_2_1 = '<div class="rounded-md border-2 border-dashed flex justify-center items-center flex-col bg-base-100 bg-opacity-30 cursor-pointer space-y-2 h-36" id="dd_3"><div class="rounded-full h-10 w-10 flex justify-center items-center border-none bg-base-100 border-none inline-flex shadow my-4"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="currentColor" , class="h-6 w-6 text-success opacity-75"><path cd="M0,0H20V20H0Z"></path><path d="M15.833,11.667H11.667v4.167a.833.833,0,0,1-1.667,0V11.667H5.833a.833.833,0,1,1,0-1.667H10V5.833a.833.833,0,1,1,1.667,0V10h4.167a.833.833,0,0,1,0,1.667Z" transform="translate(-0.833 -0.833)"></path></svg></div><span class="m-1 text-sm opacity-75"><a href="#" class="link link-hover link-success opacity-75">Upload a file</a>or drag and drop</span><span class="pb-4 text-xs opacity-50">.csv, .xlsx</span></div><div class="space-y-0 opacity-75"><h1 class="text-xs font-bold">İmportant note for file encoding:</h1><p class="text-xs">To ensure smooth upload process, it is recommended to use Unicode (UTF-8) encoding for your files. UTF-8 supports a wide range of characters and symbols from different languages and character sets. To select UTF-8 encoding for your file, you can find the encoding drop down list in your text editor or IDE. From the drop down list, select UTF-8 as the encoding for your file. After saving your file with UTF-8 encoding, you can proceed with the upload process. This will ensure that your file is properly recognized by our system without any syntax errors.</p></div>';
  const inner_r_2_2 = '<label class="label"><span class="label-text">Type or copy and paste contacts</span></label><textarea class="textarea textarea-bordered textarea-sm w-full h-24" placeholder="email1, email2, ..."></textarea>';
  ff_3.innerHTML = r_2_1.checked ? inner_r_2_1 : inner_r_2_2;
  if(r_2_1.checked){
    const inner_r_2_1_base = '<div class="rounded-full h-10 w-10 flex justify-center items-center border-none bg-base-100 border-none inline-flex shadow my-4"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="currentColor" , class="h-6 w-6 text-success opacity-75"><path cd="M0,0H20V20H0Z"></path><path d="M15.833,11.667H11.667v4.167a.833.833,0,0,1-1.667,0V11.667H5.833a.833.833,0,1,1,0-1.667H10V5.833a.833.833,0,1,1,1.667,0V10h4.167a.833.833,0,0,1,0,1.667Z" transform="translate(-0.833 -0.833)"></path></svg></div><span class="m-1 text-sm opacity-75"><a href="#" class="link link-hover link-success opacity-75">Upload a file</a>or drag and drop</span><span class="pb-4 text-xs opacity-50">.csv, .xlsx</span></div>';
    const inner_r_2_1_success = '<div class="w-24" id="success-lottie"></div>';
    const inner_r_2_1_error = '<div class="w-24" id="error-lottie"></div><p class="text-sm">Invalid file format</p>';
    const dropZone = document.getElementById("dd_3");
    const containerRect = dropZone.getBoundingClientRect();
    let loadLottie = false;
    let fileTypeOk = false;

    dropZone.addEventListener('dragover', function(event) {
        event.preventDefault();
        event.stopPropagation();

        if(!loadLottie)
        {
          loadLottie = true;
          fileExtension = getFileExtension(event);
          if(fileExtension === 'text/csv' || fileExtension === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
          {
            fileTypeOk = true;
            dropZone.innerHTML = inner_r_2_1_success;
            dropZone.classList.add('border-success');
            dropZone.classList.remove('border-error');
            dropZone.classList.remove('bg-error');
            dropZone.classList.remove('bg-opacity-5');
            lottie.loadAnimation({
              container: document.getElementById('success-lottie'),
              renderer: 'svg',
              loop: true,
              autoplay: true,
              path: '../../static/img/success-lottie.json',
              rendererSettings: {
              preserveAspectRatio: 'xMidYMid meet',
              progressiveLoad: false,
              scaleMode: 'noScale',
              hideOnTransparent: true
            }
            });
          }
          else
          {
            fileTypeOk = false;
            dropZone.classList.remove('border-success');
            dropZone.classList.add('border-error');
            dropZone.classList.add('bg-error');
            dropZone.classList.add('bg-opacity-5');
            
            dropZone.innerHTML = inner_r_2_1_error;
            lottie.loadAnimation({
              container: document.getElementById('error-lottie'),
              renderer: 'svg',
              loop: true,
              autoplay: true,
              path: '../../static/img/error-lottie.json',
              rendererSettings: {
              preserveAspectRatio: 'xMidYMid meet',
              progressiveLoad: false,
              scaleMode: 'noScale',
              hideOnTransparent: true
            }
            });
          }
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
          dropZone.classList.remove('border-success');
          dropZone.classList.remove('border-error');
          dropZone.classList.remove('bg-error');
          dropZone.classList.remove('bg-opacity-5');
          dropZone.innerHTML = inner_r_2_1_base;
          loadLottie = false;
        }
    });

    dropZone.addEventListener('drop', async function(event) {
      event.preventDefault();
      dropZone.classList.remove('border-success');
      dropZone.classList.remove('border-error');
      dropZone.classList.remove('bg-error');
      dropZone.classList.remove('bg-opacity-10');
      dropZone.innerHTML = inner_r_2_1_base;
      loadLottie = false;

      if(fileTypeOk)
      {
        dropZone.classList.add('border-success');
        await handleFiles(event.dataTransfer.files);
      }
    });

    fi_3.addEventListener('change', async function(event) {
      const file = event.target.files[0];
      if(file.type === 'text/csv' || file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'){
        await handleFiles(event.target.files);
      }
    });

    dropZone.addEventListener('click', function(event) {
      event.preventDefault();
      fi_3.click();
    });

    async function handleFiles(files) {
      const file = files[0]
      const fileName = file.name
      const formData = new FormData()
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        formData.append('file', file)
      }
    
      dropZone.innerHTML = '<div class="flex justify-center items-center flex-col space-y-4"><progress class="progress progress-success w-56" value="0" max="100" id="progress"></progress><h1 class="text-sm font-bold">Please wait until files upload</h1></div>'
      const progress = document.getElementById('progress')
    
      const xhr = new XMLHttpRequest()
      xhr.upload.addEventListener('progress', function(event) {
        const percentComplete = (event.loaded / event.total) * 100
        progress.value = percentComplete
      })
    
      xhr.open('POST', '/tools/upload_file/')
      xhr.send(formData)
      
      xhr.onload = function() {
        if (xhr.status == 200) {
          const result = JSON.parse(xhr.responseText)
          if (result.success) {
            const emails = result.emails.filter(email => validateEmail(email))
            console.log(emails);
            dropZone.innerHTML = `<div class="flex flex-row justify-center items-center space-x-2"><svg width="20px" height="20px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="text-warning h-6 w-6"><title/><g id="Complete"><g id="F-File"><g id="Text"><g><path d="M18,22H6a2,2,0,0,1-2-2V4A2,2,0,0,1,6,2h7.1a2,2,0,0,1,1.5.6l4.9,5.2A2,2,0,0,1,20,9.2V20A2,2,0,0,1,18,22Z" fill="none" stroke="currentColor" id="File" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="17.5" y2="17.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="13.5" y2="13.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="8" x2="13" y1="9.5" y2="9.5"/></g></g></g></g></svg><div class="text-xs text-success">Selected file: ${fileName}</div>`
            sc_4_1.innerHTML = result.emails.length;
            sc_4_2.innerHTML = emails.length;
            sc_4_3.innerHTML = result.emails.length - emails.length;
            last_touch(true);
          } else {
            console.log(result.error);
            last_touch(false);
          }
        }
        else{
          last_touch(false);
        }
      }
    }

    function validateEmail(email) {
      const regex = /\S+@\S+\.\S+/
      return regex.test(email)
    }

    function last_touch(response){
      if(!response)
      {
        dropZone.classList.remove('border-success');
        dropZone.classList.remove('border-error');
        dropZone.classList.remove('bg-error');
        dropZone.classList.remove('bg-opacity-10');
        dropZone.innerHTML = inner_r_2_1_base;
        loadLottie = false;
        cb_3.setAttribute("disabled", "disabled");
      }
      else
      {
        cb_3.removeAttribute("disabled");
      }
    }
  }
  else{

  }
});

bb_3.addEventListener("click", function(){
  const inner = '<p class="text-base">2</p>';
  n_2.innerHTML = inner;

  c_2.classList.add("collapse-open");
  c_2.classList.remove("collapse-close");
  c_2.classList.add("collapse-arrow");
  c_2.classList.remove("opacity-50");

  c_3.classList.add("opacity-50");
  c_3.classList.remove("collapse-arrow");
  c_3.classList.add("collapse-close");
  c_3.classList.remove("collapse-open");
});

cb_3.addEventListener("click", function(){
  const inner = '<svg width="32" height="32" viewBox="0 0 20 20"><path id="Path_11514" data-name="Path 11514" d="M10,0A10,10,0,1,1,0,10,10,10,0,0,1,10,0Z" fill="#C6F6D5"></path><path id="Path_11516" data-name="Path 11516" d="M0,0H12V12H0Z" transform="translate(4 4)" fill="none"></path><path id="Path_11517" data-name="Path 11517" d="M6.4,11.1l-1.75-1.75a.495.495,0,0,0-.7.7l2.1,2.1a.5.5,0,0,0,.7,0l5.3-5.3a.495.495,0,0,0-.7-.7Z" transform="translate(2.096 0.996)" fill="#22543D"></path></svg>';
  n_3.innerHTML = inner;

  c_3.classList.remove("collapse-open");
  c_3.classList.add("collapse-close");
  c_3.classList.remove("collapse-arrow");
  c_3.classList.add("opacity-50");

  c_4.classList.remove("opacity-50");
  c_4.classList.add("collapse-arrow");
  c_4.classList.remove("collapse-close");
  c_4.classList.add("collapse-open");
});

bb_4.addEventListener("click", function(){
  const inner = '<p class="text-base">3</p>';
  n_3.innerHTML = inner;

  c_3.classList.add("collapse-open");
  c_3.classList.remove("collapse-close");
  c_3.classList.add("collapse-arrow");
  c_3.classList.remove("opacity-50");

  c_4.classList.add("opacity-50");
  c_4.classList.remove("collapse-arrow");
  c_4.classList.add("collapse-close");
  c_4.classList.remove("collapse-open");
});

rc_5_1.addEventListener('click', (event) => {
  rb_5_1.checked = true;
  tb_5_2.hidden = true;
  tb_5_1.hidden = false;
});

rc_5_2.addEventListener('click', (event) => {
  rb_5_2.checked = true;
  tb_5_1.hidden = true;
  tb_5_2.hidden = false;
});

cb_4.addEventListener("click", function(){
  const inner = '<svg width="32" height="32" viewBox="0 0 20 20"><path id="Path_11514" data-name="Path 11514" d="M10,0A10,10,0,1,1,0,10,10,10,0,0,1,10,0Z" fill="#C6F6D5"></path><path id="Path_11516" data-name="Path 11516" d="M0,0H12V12H0Z" transform="translate(4 4)" fill="none"></path><path id="Path_11517" data-name="Path 11517" d="M6.4,11.1l-1.75-1.75a.495.495,0,0,0-.7.7l2.1,2.1a.5.5,0,0,0,.7,0l5.3-5.3a.495.495,0,0,0-.7-.7Z" transform="translate(2.096 0.996)" fill="#22543D"></path></svg>';
  n_4.innerHTML = inner;

  c_4.classList.remove("collapse-open");
  c_4.classList.add("collapse-close");
  c_4.classList.remove("collapse-arrow");
  c_4.classList.add("opacity-50");

  c_5.classList.remove("opacity-50");
  c_5.classList.add("collapse-arrow");
  c_5.classList.remove("collapse-close");
  c_5.classList.add("collapse-open");
});

bb_5.addEventListener("click", function(){
  const inner = '<p class="text-base">4</p>';
  n_4.innerHTML = inner;

  c_4.classList.add("collapse-open");
  c_4.classList.remove("collapse-close");
  c_4.classList.add("collapse-arrow");
  c_4.classList.remove("opacity-50");

  c_5.classList.add("opacity-50");
  c_5.classList.remove("collapse-arrow");
  c_5.classList.add("collapse-close");
  c_5.classList.remove("collapse-open");
});

