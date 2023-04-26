
lottie.loadAnimation({
  container: document.getElementById('loading-files-lottie'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: '../../static/img/loading-files-lottie.json',
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
    progressiveLoad: false,
    scaleMode: 'noScale',
    hideOnTransparent: true,
  }
});

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
const p_5 = document.getElementById("p_5");
const cpr_5 = document.getElementById("cpr_5");
const pr_5 = document.getElementById("pr_5");


const successToast = document.getElementById('successToast');
const errorToast = document.getElementById('errorToast');

function showSuccesToast(message=''){
  successToast.innerHTML = message;
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

let em_d;


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

  const inner_r_2_1 = '<div class="rounded-md border-2 border-dashed flex justify-center items-center flex-col bg-base-100 bg-opacity-30 cursor-pointer space-y-2 h-36" id="dd_3"><div class="rounded-full h-10 w-10 justify-center items-center bg-base-100 border-none inline-flex shadow my-4"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="currentColor" , class="h-6 w-6 text-success opacity-75"><path cd="M0,0H20V20H0Z"></path><path d="M15.833,11.667H11.667v4.167a.833.833,0,0,1-1.667,0V11.667H5.833a.833.833,0,1,1,0-1.667H10V5.833a.833.833,0,1,1,1.667,0V10h4.167a.833.833,0,0,1,0,1.667Z" transform="translate(-0.833 -0.833)"></path></svg></div><span class="m-1 text-sm opacity-75"><a href="#" class="link link-hover link-success opacity-75">Upload a file</a>or drag and drop</span><span class="pb-4 text-xs opacity-50">.xlsx</span></div><div class="space-y-0 opacity-75"><h1 class="text-xs font-bold">İmportant note for file encoding:</h1><p class="text-xs">To ensure smooth upload process, it is recommended to use Unicode (UTF-8) encoding for your files. UTF-8 supports a wide range of characters and symbols from different languages and character sets. To select UTF-8 encoding for your file, you can find the encoding drop down list in your text editor or IDE. From the drop down list, select UTF-8 as the encoding for your file. After saving your file with UTF-8 encoding, you can proceed with the upload process. This will ensure that your file is properly recognized by our system without any syntax errors.</p></div>';
  const inner_r_2_2 = '<label class="label"><span class="label-text">Type or copy and paste contacts</span></label><textarea id="emailList" class="textarea textarea-bordered textarea-sm w-full h-24" placeholder="email1, email2, ..."></textarea>';
  ff_3.innerHTML = r_2_1.checked ? inner_r_2_1 : inner_r_2_2;
  if(r_2_1.checked){
    const inner_r_2_1_base = '<div class="rounded-full h-10 w-10 justify-center items-center bg-base-100 border-none inline-flex shadow my-4"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="currentColor" , class="h-6 w-6 text-success opacity-75"><path cd="M0,0H20V20H0Z"></path><path d="M15.833,11.667H11.667v4.167a.833.833,0,0,1-1.667,0V11.667H5.833a.833.833,0,1,1,0-1.667H10V5.833a.833.833,0,1,1,1.667,0V10h4.167a.833.833,0,0,1,0,1.667Z" transform="translate(-0.833 -0.833)"></path></svg></div><span class="m-1 text-sm opacity-75"><a href="#" class="link link-hover link-success opacity-75">Upload a file</a>or drag and drop</span><span class="pb-4 text-xs opacity-50">.xlsx</span></div>';
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
          if(fileExtension === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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
        const percentComplete = (event.loaded / event.total) * 100;
        progress.value = percentComplete;
      })
    
      xhr.open('POST', '/tools/upload_file/')
      xhr.send(formData)
      
      xhr.onload = function() {
        if (xhr.status == 200) {
          const result = JSON.parse(xhr.responseText);
          if (result.success) {
            em_d = result.emails;
            dropZone.innerHTML = `<div class="flex flex-row justify-center items-center space-x-2"><svg width="20px" height="20px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="text-warning h-6 w-6"><title/><g id="Complete"><g id="F-File"><g id="Text"><g><path d="M18,22H6a2,2,0,0,1-2-2V4A2,2,0,0,1,6,2h7.1a2,2,0,0,1,1.5.6l4.9,5.2A2,2,0,0,1,20,9.2V20A2,2,0,0,1,18,22Z" fill="none" stroke="currentColor" id="File" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="17.5" y2="17.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="13.5" y2="13.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="8" x2="13" y1="9.5" y2="9.5"/></g></g></g></g></svg><div class="text-xs text-success">Selected file: ${fileName}</div>`
            sc_4_1.innerHTML = result.total_count;
            sc_4_2.innerHTML = result.validate_count;
            sc_4_3.innerHTML = result.unknown_count;
            last_touch(true);
          } else {
            showErrorToast(result.error.toString());
            last_touch(false);
          }
        }
        else{
          showErrorToast('In handleFiles went something wrong!');
          last_touch(false);
        }
      }
    }

    function last_touch(response){
      if(!response)
      {
        dropZone.classList.remove('border-success');
        dropZone.classList.remove('border-error');
        dropZone.classList.remove('bg-error');
        dropZone.classList.remove('bg-opacity-10');
        dropZone.innerHTML = inner_r_2_1_base;
        cb_3.setAttribute("disabled", "disabled");
      }
      else
      {
        cb_3.removeAttribute("disabled");
      }
      loadLottie = false;
    }
  }
  else{
    cb_3.removeAttribute("disabled");
  }
});

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

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
  cb_3.setAttribute("disabled", "disabled");
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

  if (r_2_2.checked) {
    const emailList = document.getElementById('emailList').value;
    if (emailList) {
      const emails = emailList.split(',').map(email => email.trim());
  
      em_d = [];
      let total_count = 0;
      let valid_count = 0;
      for (let email of emails) {
        total_count++;
        if (isValidEmail(email)) {
          const emailObj = {
            'name': '',
            'title': '',
            'email': email,
            'status': true
          };
          em_d.push(emailObj);
          valid_count++;
        }
      }
  
      console.log(em_d);
      sc_4_1.innerHTML = total_count;
      sc_4_2.innerHTML = valid_count;
      sc_4_3.innerHTML = total_count - valid_count;
    }
  }
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
  getEmailFileNames(tb_5_1);
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

async function getEmailFileNames(pick_list, selected_name='') {
  try {
    const response = await fetch('/tools/get_email_names/?' + new Date().getTime());
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate';
    response.headers['Pragma'] = 'no-cache';
    response.headers['Expires'] = '0';
    const data = await response.json();
    pick_list.innerHTML = '<option disabled selected>Pick one</option>';

    console.log('data:', data.names);
    data.names.forEach(name => {
      if(name != 'Pick one'){
        const optionEl = document.createElement('option')
        optionEl.value = name
        optionEl.textContent = name
        if(selected_name != '' && selected_name == name){
          optionEl.selected = true;
        }
        pick_list.appendChild(optionEl)
      }
    });
    create_table();
  } catch (error) {
    showErrorToast(error.toString());
  }
}

cb_5.addEventListener("click", function(){
  save_form();
});

function save_form(){
  const formData = new FormData();
  formData.append('emails', JSON.stringify(em_d));
  const name = rb_5_1.checked ? tb_5_1.options[tb_5_1.selectedIndex].value : tb_5_2.value;
  if(name == 'Pick one'){
    showErrorToast('Please select a correct name!');
    return;
  }
  formData.append('name', name);
  const xhr = new XMLHttpRequest();

  p_5.style.display = 'none';
  cpr_5.style.removeProperty('display');

  xhr.upload.addEventListener('progress', function(event) {
    const percentComplete = (event.loaded / event.total) * 100;
    pr_5.style.setProperty('--value', `${percentComplete}`);
    pr_5.innerHTML = `${percentComplete}%`;
  })

  xhr.open('POST', '/tools/save_emails/')
  xhr.send(formData)
  xhr.onload = function() {

    cpr_5.style.display = 'none';
    p_5.style.removeProperty('display');

    if (xhr.status == 200) {
      const response = JSON.parse(xhr.responseText);
      if (response.success) {
        showSuccesToast('Task complate successfully.');
        setTimeout(tab_2_func, 200, name);
      } else {
        showSuccesToast('Error! Task failed.');
      }
    }
    else{
      showSuccesToast('Error! Task failed for unsported reason! ERR_003');
    }
  }
}

const tab_1 = document.getElementById('tab_1');
const tab_2 = document.getElementById('tab_2');
const tab_1_panel = document.getElementById('tab_1_panel');
const tab_2_panel = document.getElementById('tab_2_panel');
const ms_1 = document.getElementById('ms_1');
const mf_1 = document.getElementById('mf_1');
const mfp_1 = document.getElementById('mfp_1');

tab_1.addEventListener('click', function(){
  tab_2.classList.remove('tab-active');
  tab_2.classList.remove('[--tab-bg:hsl(var(--b2))]');
  tab_2_panel.style.display = 'none';
  tab_1.classList.add('tab-active');
  tab_1.classList.add('[--tab-bg:hsl(var(--b2))]');
  tab_1_panel.style.removeProperty('display');
});

tab_2.addEventListener('click', tab_2_func);

function tab_2_func(name=''){
  tab_1.classList.remove('tab-active');
  tab_1.classList.remove('[--tab-bg:hsl(var(--b2))]');
  tab_1_panel.style.display = 'none';
  tab_2.classList.add('tab-active');
  tab_2.classList.add('[--tab-bg:hsl(var(--b2))]');
  tab_2_panel.style.removeProperty('display');
  getEmailFileNames(ms_1, name);
}

ms_1.onchange = create_table;

async function create_table() {
  const selectedOption = ms_1.options[ms_1.selectedIndex].value;

  if(selectedOption != 'Pick one'){
    const itemsPerPage = 50;
    let currentPage = 1;
    let emails = await getEmails(selectedOption);

    async function renderTable(){
      mf_1.style.display = 'none';
      mfp_1.style.removeProperty('display');
      mf_1.innerHTML = '<div class="overflow-x-auto bg-base-200 rounded-lg"><table class="min-w-full" id="mt_table"><thead class="bg-base-300 rounded-t-lg"><tr><th scope="col" class="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider"><label class="inline-flex items-center"><input type="checkbox" class="checkbox checkbox-xs" id="checkbox_all"></label></th><th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Name</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Title</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Email</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Status</th></tr></thead><tbody class="divide-y divide-gray-700" id="mtb_1"></tbody><tfoot><tr><td colspan="5" class="bg-base-300 px-6 py-4 rounded-b-lg text-sm" id="mtf_1">Showing _ to _ of _ entries</td></tr></tfoot></table></div><div class="flex items-center justify-end gap-x-4 pr-2"><button class="btn btn-sm btn-outline text-xs btn-error" id="mdelb_1" disabled="disabled">Delete</button><button class="btn btn-sm btn-outline text-xs" id="msaveb_1">Save</button></div>';

      const mt_table = document.getElementById('mt_table');
      const mtb_1 = document.getElementById('mtb_1');
      const selectAllCheckbox = document.getElementById('checkbox_all');
      const deleteButton = document.getElementById('mdelb_1');
      const saveButton = document.getElementById('msaveb_1');


      if (emails != []) {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        const rows = emails.slice(startIndex, endIndex);
        rows.forEach((email, index) => {
          // Create the table row
          const tr = document.createElement('tr');
          tr.id = 'mt_tr';
          tr.classList.add('transition-all', 'duration-200', 'hover:bg-base-100');
      
          // Create the checkbox cell
          const tdCheckbox = document.createElement('td');
          tdCheckbox.classList.add('px-6', 'py-3', 'whitespace-nowrap', 'text-sm');
          const label = document.createElement('label');
          label.classList.add('inline-flex', 'items-center');
          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.id = 'emailCheckboxes';
          checkbox.classList.add('checkbox', 'checkbox-xs');
          label.appendChild(checkbox);
          tdCheckbox.appendChild(label);
          tr.appendChild(tdCheckbox);
      
          // Create the name cell
          const tdName = document.createElement('td');
          tdName.classList.add('px-6', 'py-3', 'whitespace-nowrap', 'text-sm');
          tdName.textContent = email.name;
          tr.appendChild(tdName);
      
          // Create the title cell
          const tdTitle = document.createElement('td');
          tdTitle.classList.add('px-6', 'py-3', 'whitespace-nowrap', 'text-sm');
          tdTitle.textContent = email.title;
          tr.appendChild(tdTitle);
      
          // Create the email cell
          const tdEmail = document.createElement('td');
          tdEmail.classList.add('px-6', 'py-3', 'whitespace-nowrap', 'text-sm');
          tdEmail.textContent = email.email;
          tr.appendChild(tdEmail);
      
          // Create the status cell
          const tdStatus = document.createElement('td');
          tdStatus.classList.add('px-6', 'py-3', 'whitespace-nowrap', 'text-sm');
          const labelStatus = document.createElement('label');
          labelStatus.classList.add('swap', 'swap-rotate');
          const checkboxStatus = document.createElement('input');
          checkboxStatus.type = 'checkbox';
          checkboxStatus.id = 'statusCheckboxes';
          checkboxStatus.checked = email.status;
          const divOn = document.createElement('div');
          divOn.classList.add('swap-on', 'text-success', 'text-xs', 'font-bold');
          divOn.textContent = 'ACTIVE';
          const divOff = document.createElement('div');
          divOff.classList.add('swap-off', 'text-error', 'text-xs', 'font-bold');
          divOff.textContent = 'PASSIVE';
          labelStatus.appendChild(checkboxStatus);
          labelStatus.appendChild(divOn);
          labelStatus.appendChild(divOff);
          tdStatus.appendChild(labelStatus);
          tr.appendChild(tdStatus);
      
          checkboxStatus.addEventListener('change', function () {
            email['status'] = checkboxStatus.checked ? true : false;
          });
      
          mtb_1.appendChild(tr);
        });
      
        const mtf_1 = document.getElementById('mtf_1');
        const startEntry = startIndex + 1;
        const endEntry = Math.min(endIndex, emails.length);

        const totalPages = Math.ceil(emails.length / itemsPerPage);
        const pageButtonsContainer = document.createElement('div');
        pageButtonsContainer.classList.add('btn-group', 'btn-group-horizontal');

        for (let i = 1; i <= totalPages; i++) {
          console.log('Creating button for page', i);
          const pageButton = document.createElement('button');
          pageButton.classList.add('btn', 'btn-xs');
          pageButton.innerHTML = i;

          if (i === currentPage) {
            pageButton.classList.add('btn-active');
          }

          pageButtonsContainer.appendChild(pageButton);

          pageButton.addEventListener('click', function () {
            currentPage = i;
            renderTable();
          });
        }
        mtf_1.innerHTML = `<div class="container mx-auto flex items-center justify-between"><div>Showing ${startEntry} to ${endEntry} of ${emails.length} entries</div></div>`;
        mtf_1.querySelector('.container').appendChild(pageButtonsContainer);
      }    

      mf_1.style.removeProperty('display');
      mfp_1.style.display = 'none';

      const emailCheckboxes = document.querySelectorAll('#mtb_1 input[id="emailCheckboxes"]');

      selectAllCheckbox.addEventListener('change', function() {
        emailCheckboxes.forEach(function(emailCheckbox) {
          emailCheckbox.checked = selectAllCheckbox.checked;
        });

        if (document.querySelector('#mtb_1 input[id="emailCheckboxes"]:checked')) {
          deleteButton.disabled = false;
        } else {
          deleteButton.disabled = true;
        }
      });

      emailCheckboxes.forEach(function(emailCheckbox) {
        emailCheckbox.addEventListener('change', function() {
          if (document.querySelector('#mtb_1 input[id="emailCheckboxes"]:checked')) {
            deleteButton.disabled = false;
          } else {
            deleteButton.disabled = true;
          }

          if (document.querySelectorAll('#mtb_1 input[id="emailCheckboxes"]').length === document.querySelectorAll('#mtb_1 input[id="emailCheckboxes"]:checked').length) {
            selectAllCheckbox.checked = true;
          } else {
            selectAllCheckbox.checked = false;
          }
        });
      });

      const rows = document.querySelectorAll('#mt_tr');
      deleteButton.addEventListener('click', function() {
        if (document.querySelectorAll('#mtb_1 input[id="emailCheckboxes"]').length === document.querySelectorAll('#mtb_1 input[id="emailCheckboxes"]:checked').length){
          mt_table.remove();
          emails.length = 0;
          saveButton.classList.add('motion-safe:animate-pulse');
          saveChanges();
        } else {
          const checkedIndexes = [];
          emailCheckboxes.forEach(function(emailCheckbox, index) {
            if(emailCheckbox.checked){
              checkedIndexes.push(index);
            }
          });
          const newEmails = emails.filter(function(email, index) {
            return !checkedIndexes.includes(index);
          });
          emails = newEmails;
          rows.forEach(function(row, index) {
            if(checkedIndexes.includes(index)) {
              row.remove();
            }
          });
          saveButton.classList.add('motion-safe:animate-pulse');
          saveChanges();
        }
      });

      saveButton.addEventListener('click', saveChanges);

      function saveChanges(){
        const formData = new FormData();
        formData.append('emails', JSON.stringify(emails));
        const name = ms_1.options[ms_1.selectedIndex].value;
        formData.append('name', name);
        const xhr = new XMLHttpRequest();
    
        mf_1.style.display = 'none';
        mfp_1.style.removeProperty('display');
      
        xhr.open('POST', '/tools/save_emails/')
        xhr.send(formData)
        xhr.onload = function() {
          if (xhr.status == 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
              showSuccesToast('Your changes have been saved.');
            } else {
              console.log(response.error);
              showErrorToast('Your changes can not saved!');
            }
          }
          else{
            showErrorToast('Your changes can not saved! Response is not OK!');
          }
        }
    
        mfp_1.style.display = 'none';
        mf_1.style.removeProperty('display');
      }
    }

    renderTable();
  }
}


async function getEmails(name = null) {
  const url = name ? `/tools/get_emails/?name=${name}` : '/tools/get_emails/';
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') // add the csrfmiddlewaretoken header here
    },
    body: JSON.stringify({})
  });
  if(response.ok){
    const data = await response.json();
    if (data.success) {
      return data.emails[0];
    }
    showErrorToast('Failed to fetch emails');
    return [];
  } else {
    showErrorToast('Failed to fetch emails. Response is not OK!');
    return [];
  }
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* <tr>
<td class="px-6 py-4 whitespace-nowrap text-sm">
  <label class="inline-flex items-center">
    <input type="checkbox" class="checkbox checkbox-sm" id="mtb_1_select">
  </label>
</td>
<td class="px-6 py-4 whitespace-nowrap text-sm" id="mtb_1_name"></td>
<td class="px-6 py-4 whitespace-nowrap text-sm" id="mtb_1_title"></td>
<td class="px-6 py-4 whitespace-nowrap text-sm" id="mtb_1_email"></td>
<td class="px-6 py-4 whitespace-nowrap text-sm">
  <label class="swap swap-rotate">
      <input type="checkbox" id="mtb_1_status" />
      <div class="swap-on text-success text-xs font-bold">ACTIVE</div>
      <div class="swap-off text-error text-xs font-bold">PASSIVE</div>
    </label>
</td>
</tr> */