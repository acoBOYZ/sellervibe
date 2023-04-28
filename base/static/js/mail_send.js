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
const input_from = document.getElementById('input_from');
const input_replyTo = document.getElementById('input_replyTo');
const input_cc = document.getElementById('input_cc');
const input_subject = document.getElementById('input_subject');
const textarea_message = document.getElementById('textarea_message');
const submit_send = document.getElementById('submit_send');


function openSendModal() {
    const modal_send = document.getElementById('modal_send');
    const modal_box = modal_send.querySelector('.modal-box');
    modal_box.innerHTML = '<div layz class="sticky inset-x-0 top-0 z-10" id="send-emails-lottie"></div><div class="overflow-y-scroll space-y-0 z-0" id="modal-log"></div><div class="modal-action relative justify-center items-center z-20"></div>';

    lottie.loadAnimation({
        container: document.getElementById('send-emails-lottie'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: '../../static/img/send-emails-lottie.json',
        rendererSettings: {
        preserveAspectRatio: 'xMidYMid meet',
        progressiveLoad: true,
        scaleMode: 'noScale',
        hideOnTransparent: true
        }
    });
    window.location.hash = "modal_send";
}

let stopAnimation = true;
let log_id_context = 0;
let animationTimeouts = [];

function updateSendModal(command, color, animate=false){
    animationTimeouts.forEach(timeout => clearTimeout(timeout));
    animationTimeouts = [];

    const log_id = 'log-command-' + log_id_context.toString();
    log_id_context ++;
    const modal_send = document.getElementById('modal_send');
    const modal_log = modal_send.querySelector('#modal-log');
    modal_log.innerHTML += `<pre class="antialiased text-xs/tight text-${color}"><code id="${log_id}">> ${command} </code></pre>`;
    modal_log.scrollIntoView({ behavior: 'smooth' });

    function getRandomDecimal(min, max) {
        return Math.random() * (max - min) + min;
    }

    function animate_func() {
        modal_log_animate = modal_log.querySelector(`#${log_id}`);
        modal_log_animate.innerHTML += '░';

        if (!stopAnimation) {
            const animationIntervalValue = getRandomDecimal(100, 300);
            const newTimeout = setTimeout(animate_func, animationIntervalValue);
            animationTimeouts.push(newTimeout);
        }
    }

    if(animate){
        stopAnimation = false;
        animate_func();
    }
    else{
        stopAnimation = true;
    }
}

function finishSendModal(success=true){
    const modal_send = document.getElementById('modal_send');
    const modal_box = modal_send.querySelector('.modal-box');
    modal_box.innerHTML = '<div layz class="z-10 w-auto h-36 relative justify-center items-center" id="send-emails-success-lottie"></div><div class="space-y-0 z-0 text-success flex justify-center items-center" id="modal-log">All emails sent successfully</div><div class="modal-action flex justify-center items-center z-20"></div>';

    lottie.loadAnimation({
        container: document.getElementById('send-emails-success-lottie'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: '../../static/img/send-emails-success-lottie.json',
        rendererSettings: {
        preserveAspectRatio: 'xMidYMid meet',
        progressiveLoad: true,
        scaleMode: 'noScale',
        hideOnTransparent: true
        }
    });
}

function addSendModalToButton(innerValue, type){
    const modal_send = document.getElementById('modal_send');
    const modal_action = modal_send.querySelector('.modal-action');
    modal_action.innerHTML += `<a href="#" class="btn btn-wide btn-outline btn-${type}">${innerValue}</a>`;
    modal_action.scrollIntoView({ behavior: 'smooth' });
}

function closeSendModal() {
    window.location.hash = "";
}

getEmailFileNames(pick_list);


const successToast = document.getElementById('successToast');
const errorToast = document.getElementById('errorToast');
const warningToast = document.getElementById('warningToast');

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
  
function showWarningToast(message=''){
    warningToast.innerHTML = message;
    warningToast.classList.remove('hidden');

    setTimeout(() => {
        warningToast.classList.add('hidden');
    }, 3000);
}

let required_area = false;
let input_from_value;
let input_replyTo_value;
let input_cc_value_list = [];
let pick_list_value;
let input_subject_value;
let textarea_message_value;
let attachment_list = [];

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
        var fileSize = Math.floor(files[i].size / 1024);
        dropZone_fileBase.innerHTML += `<div class="flex flex-row justify-between items-center bg-base-200 rounded-xl"><div class="flex items-center space-x-2 mx-2"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4"><title/><g><g><g><g><path d="M18,22H6a2,2,0,0,1-2-2V4A2,2,0,0,1,6,2h7.1a2,2,0,0,1,1.5.6l4.9,5.2A2,2,0,0,1,20,9.2V20A2,2,0,0,1,18,22Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="17.5" y2="17.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.9" x2="16.1" y1="13.5" y2="13.5"/><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="8" x2="13" y1="9.5" y2="9.5"/></g></g></g></g></svg><div class="text-xs">${fileName} <span class="text-xs opacity-50">${fileSize}kb</span></div></div><div><button class="btn btn-xs btn-circle btn-outline" id="remove_file_btn" name="${fileName}"><svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div></div>`;
        attachment_list.push(files[i]);
    }
    
    const removeFileBtns = document.querySelectorAll('#dropZone_fileBase button[id="remove_file_btn"]');
    removeFileBtns.forEach(function (removeFileBtn) {
      removeFileBtn.addEventListener('click', function () {
        remainingFiles--;
        attachment_list = attachment_list.filter(function (file) {
            return file.name !== removeFileBtn.name;
        });
        removeFileBtn.parentElement.parentElement.remove();          
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
}

function sendFilesToServer() {
    const formData = new FormData();
    for (let i = 0; i < attachment_list.length; i++) {
      formData.append(`attachment`, attachment_list[i]);
      updateSendModal(`found ${attachment_list[i].name}`, 'normal');
    }
  
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/tools/upload_attachments/', true);
  
    const csrftoken = getAttachmentsCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  
    xhr.onreadystatechange = function () {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            const response = JSON.parse(this.responseText);
            
            const success_responses = response.success_responses;
            const error_responses = response.error_responses;
            if (success_responses.length > 0) {
                attachment_list = success_responses.map(item => item.unique_name);
                attachment_list.forEach(function (fileName){
                    updateSendModal(`${fileName} uploaded.`, 'success');
                });
                error_responses.forEach(function (err){
                    updateSendModal(`${err.name} failed. ${err.error}`, 'error');
                });
                sendEmailsToServer();
            } else {
                updateSendModal(`you got some errors while uploading files. Please check your network connection. ${response.error}`, 'error');
                addSendModalToButton('Try Again', 'error');
                showErrorToast(response.error);
            }
        }
    };
  
    xhr.send(formData);
    updateSendModal(`uploading all attachments`, 'secondary', true);
}
  
function getAttachmentsCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function sendEmailsToServer() {
    const formData = new FormData();
    for (let i = 0; i < attachment_list.length; i++) {
      formData.append(`attachment`, attachment_list[i]);
      updateSendModal(`${attachment_list[i]} added to email attachments`, 'normal');
    }
    
    updateSendModal(`downloading email list from:'${pick_list_value}'`, 'secondary', true);
    let emails = await getEmails(pick_list_value);
    if(!emails){
        updateSendModal(`in '${pick_list_value}' emails not found!`, 'error');
        updateSendModal(`you got some errors while downloading emails. Please check your network connection and contact list!`, 'error');
        addSendModalToButton('Try Again', 'error');
        return;
    }
    updateSendModal(`'${pick_list_value}' download finished.`, 'success');
    for (let i = 0; i < emails.length; i++) {
        formData.append(`email`, JSON.stringify(emails[i]));
    }
    updateSendModal(`your email is ready to send all email address`, 'normal');

    updateSendModal(`uploading your email contexts`, 'primary', true);
    formData.append('from', input_from_value);
    formData.append('replyTo', input_replyTo_value);
    formData.append('cc', input_cc_value_list);
    formData.append('subject', input_subject_value);
    formData.append('message', textarea_message_value);
    updateSendModal(`your email contexts ready`, 'normal');

  
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/tools/send_bulk_emails/', true);
  
    const csrftoken = getAttachmentsCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  
    xhr.onreadystatechange = function () {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            const response = JSON.parse(this.responseText);
            
            if (response.success) {

                dropZone_fileBase.innerHTML = '';
                dropZone_base.style.removeProperty('display');
                success_lottie.style.display = 'none';
                dropZone_fileBase.style.display = 'none';
                dropZone_progress.style.display = 'none';
                dropZone.classList.remove('border-success');
                loadLottie = false;
                dropZone_hasFile = false;
                attachment_list.length = 0;
                input_replyTo.classList.remove('border-error', 'border-opacity-75');
                pick_list.classList.remove('border-error', 'border-opacity-75');
                input_subject.classList.remove('border-error', 'border-opacity-75');
                textarea_message.classList.remove('border-error', 'border-opacity-75');
                dropZone.scrollIntoView({ behavior: 'smooth' });
                input_replyTo.value = '';
                input_cc.value = '';
                pick_list.selectedIndex = 0;
                input_subject.value = '';
                textarea_message.value = '';

                updateSendModal(`all emails are sended ${attachment_list.length > 0 ? 'with attachments' : ''}`, 'primary');
                finishSendModal();
                addSendModalToButton('Send New Emails', 'primary');
            } else {
                updateSendModal(`you got some errors while sending emails. Please check your network connection. ${response.error}`, 'error');
                addSendModalToButton('Try Again', 'error');
                showErrorToast(response.error);
            }
        }
    };
  
    xhr.send(formData);
    updateSendModal(`sending all emails ${attachment_list.length > 0 ? 'with attachments' : ''}`, 'secondary', true);
}

async function getEmails(name = null) {
    const url = name ? `/tools/get_emails/?name=${name}` : '/tools/get_emails/';
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getEmailsCookie('csrftoken')
      },
      body: JSON.stringify({})
    });
    if(response.ok){
      const data = await response.json();
      if (data.success) {
        return data.emails[0];
      }
      showErrorToast('Failed to fetch emails');
      return null;
    } else {
      showErrorToast('Failed to fetch emails. Response is not OK!');
      return null;
    }
  }
  
  function getEmailsCookie(name) {
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

  submit_send.addEventListener('click', function() {
    if(input_from.value.trim() != 'info@sellervibe.co' && !isValidEmail(input_from.value.trim())){
        showErrorToast('From: segment have not correct email address!<br>Please refresh page and try again.');
        required_area = true;
    }
    input_from_value = input_from.value;

    if(!isValidEmail(input_replyTo.value.trim())){
        input_replyTo.classList.add('border-error', 'border-opacity-75');
        required_area = true;
    }
    input_replyTo_value = input_replyTo.value.trim();

    if(input_cc.value.trim()){
        const cc_list = input_cc.value.trim().split(',');
        let valid_count = 0;
        input_cc.value = '';
        cc_list.forEach(email => {
            const trimmedEmail = email.trim();
            console.log('email', trimmedEmail);
            if(!isValidEmail(trimmedEmail)){
                showWarningToast(`${trimmedEmail} does not valid`);
            } else {
                valid_count++;
                input_cc.value += valid_count > 1 ? ', ' : input_cc.value;
                input_cc_value_list.push(trimmedEmail);
                input_cc.value += `${trimmedEmail}`;
            }
        });
    } 

    if(pick_list.options[pick_list.selectedIndex].value === 'Select a contact'){
        pick_list.classList.add('border-error', 'border-opacity-75');
        required_area = true;
    }
    pick_list_value = pick_list.options[pick_list.selectedIndex].value;

    if(!input_subject.value.trim()){
        input_subject.classList.add('border-error', 'border-opacity-75');
        required_area = true;
    }
    input_subject_value = input_subject.value;

    if(!textarea_message.value.trim()){
        textarea_message.classList.add('border-error', 'border-opacity-75');
        required_area = true;
    }
    textarea_message_value = textarea_message.value;

    // required_area = false;
    if(required_area){
        required_area = false;
        showWarningToast('Please fill out all required fields correctly.');
        input_from_value = '';
        input_replyTo_value = '';
        input_cc_value_list = [];
        pick_list_value = '';
        input_subject_value = '';
        textarea_message_value = '';
        return;
    }

    openSendModal();

    if(attachment_list.length > 0){
        sendFilesToServer();
    } else {
        sendEmailsToServer();
    }
  });

  input_replyTo.addEventListener('focus', function() {
    this.classList.remove('border-error', 'border-opacity-75');
  });

  pick_list.addEventListener('focus', function() {
    this.classList.remove('border-error', 'border-opacity-75');
  });

  input_subject.addEventListener('focus', function() {
    this.classList.remove('border-error', 'border-opacity-75');
  });

  textarea_message.addEventListener('focus', function() {
    this.classList.remove('border-error', 'border-opacity-75');
  });

  function isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
  }