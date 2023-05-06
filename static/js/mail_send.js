const dropZone = document.getElementById('dropZone');
const containerRect = dropZone.getBoundingClientRect();
let loadLottie = false;
let dropZone_hasFile = false;
let emails;
let hasInvalidFields = false;
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
    modal_box.innerHTML = '<div layz class="sticky inset-x-0 top-0 z-20" id="send-emails-lottie"></div><svg xmlns="http://www.w3.org/2000/svg" class="h-64 w-full sticky inset-x-0 top-0 z-0 hidden" id="send-email-error" viewBox="0 0 2000 2000"><circle cx="1000" cy="1000" r="814.301" fill="#f8fcfe"/><circle cx="1000" cy="1000" r="675.841" fill="#dfecfa"/><path fill="#262f5f" d="M1487.255,872.453l-23.9679,148.6617-4.6007,28.5326c0,22.0918-47.1963,313.1188-71.6426,313.1188l-386.5747-267.113L571.4339,1393.3283c-24.4373,0-50.1374-313.173-50.1374-335.2647l-1.705-36.9489L512.7448,872.886l68.9726-59.6001L972.8926,475.2518a47.9913,47.9913,0,0,1,55.1529,0l390.8054,338.0341Z"/><rect width="758.383" height="714.943" x="622.838" y="645.707" fill="#fff"/><polygon fill="#749dd3" points="1000.525 1261.454 512.745 872.886 512.745 1533.462 1487.255 1533.462 1487.255 872.886 1000.525 1261.454"/><polygon fill="#9ebee5" points="512.745 872.886 512.745 1533.462 927.364 1203.174 512.745 872.886"/><polygon fill="#9ebee5" points="1487.255 872.886 1487.255 1533.462 1072.635 1203.174 1487.255 872.886"/><circle cx="1002.029" cy="936.227" r="137.366" fill="#749dd3"/><path fill="#262f5f" d="M1002.0291,1116.1639c-99.2179,0-179.9369-80.7195-179.9369-179.9374s80.719-179.9372,179.9369-179.9372,179.9377,80.7194,179.9377,179.9372S1101.2469,1116.1639,1002.0291,1116.1639Zm0-339.5797c-88.0267,0-159.642,71.6153-159.642,159.6423,0,88.0272,71.6153,159.6425,159.642,159.6425,88.0275,0,159.6429-71.6153,159.6429-159.6425C1161.672,848.1995,1090.0566,776.5842,1002.0291,776.5842Z"/><path fill="#fff" d="M1001.9377,975.9062a16.18032,16.18032,0,0,0-16.3145,16.2227c0,5.0972,1.7002,9.1563,5.0518,12.0645a16.98809,16.98809,0,0,0,11.4472,4.25,16.59159,16.59159,0,0,0,11.3291-4.3145c3.3076-2.9385,4.9844-6.9756,4.9844-12a15.55841,15.55841,0,0,0-4.8496-11.5034A16.12723,16.12723,0,0,0,1001.9377,975.9062Z"/><path fill="#fff" d="M989.4054,945.5103l.0059.0742c.5859,6.0498,1.5605,10.4863,2.9805,13.5625,1.7041,3.6919,4.8769,5.643,9.1777,5.643a9.7192,9.7192,0,0,0,9.2461-5.7304c1.5644-3.1997,2.5488-7.5611,3.0058-13.314l3.958-45.3657a124.15254,124.15254,0,0,0,.6563-12.5962c0-7.3296-.9561-12.8545-2.9238-16.8906-1.5303-3.1402-5.001-6.8833-12.8379-6.8833a16.22791,16.22791,0,0,0-12.3701,5.0742c-3.1065,3.3198-4.6807,7.9067-4.6807,13.6343,0,3.7817.2803,10.0639.835,18.6777Z"/></svg><div class="space-y-0 z-10" id="modal-log"></div><div class="modal-action relative justify-center items-center z-30"></div>';

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

function showErrorOnSendModal(){
    const modal_send = document.getElementById('modal_send');
    const send_emails_lottie = modal_send.querySelector('#send-emails-lottie');
    const send_email_error = modal_send.querySelector('#send-email-error');
    send_emails_lottie.remove();
    send_email_error.classList.remove('hidden');
}

function finishSendModal(){
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
    errorToast.querySelector('span').innerHTML = message;
    errorToast.classList.remove('hidden');

    setTimeout(() => {
        errorToast.classList.add('hidden');
    }, 3000);
}
  
function showWarningToast(message=''){
    warningToast.querySelector('span').innerHTML = message;
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
                showErrorOnSendModal();
                addSendModalToButton('Try Again', 'error');
                showErrorToast(response.error);
            }
        }
    };
  
    xhr.send(formData);
    updateSendModal(`uploading all attachments`, 'accent', true);
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
    
    // updateSendModal(`downloading email list from:'${pick_list_value}'`, 'accent', true);
    // let emails = await getEmails(pick_list_value);
    if(!emails){
        updateSendModal(`in '${pick_list_value}' emails not found!`, 'error');
        updateSendModal(`you got some errors while downloading emails. Please check your network connection and contact list!`, 'error');
        showErrorOnSendModal();
        addSendModalToButton('Try Again', 'error');
        return;
    }
    updateSendModal(`'from ${pick_list_value}' emails download finished.`, 'success');
    for (let i = 0; i < emails.length; i++) {
        formData.append(`email`, JSON.stringify(emails[i]));
    }
    updateSendModal(`your email is ready to send all email address`, 'normal');

    updateSendModal(`uploading your email contexts`, 'info', true);
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
                resetFieldsContainer();

                updateSendModal(`all emails are sended ${attachment_list.length > 0 ? 'with attachments' : ''}`, 'info');
                finishSendModal();
                addSendModalToButton('Send New Emails', 'info');
            } else {
                updateSendModal(`you got some errors while sending emails. Please check your network connection. ${response.error}`, 'error');
                showErrorOnSendModal();
                addSendModalToButton('Try Again', 'error');
                showErrorToast(response.error);
            }
        }
    };
  
    xhr.send(formData);
    updateSendModal(`sending all emails ${attachment_list.length > 0 ? 'with attachments' : ''}`, 'accent', true);
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
      if (response.ok) {
        const data = await response.json();

        data.names.forEach(name => {
          if(name != 'Pick one'){
            const optionEl = document.createElement('option');
            optionEl.value = name;
            optionEl.textContent = name;
            pickList.appendChild(optionEl);
          }
        });
      } else if (response.status === 401) {
        showErrorToast('You need to be logged in to access this page.');
      } else {
        showErrorToast('There was an error while getting email file names.');
      }
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
    if(required_area || hasInvalidFields){
        if(required_area){
            showWarningToast('Please fill out all required fields correctly.');
        } else {
            showWarningToast('There are unsupported fields in your text.<br>Please update the fields and try again.');
            textarea_message.classList.add('border-error', 'border-opacity-75');
        }
        required_area = false;
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

  /** BADGES **/
function resetFieldsContainer(){
    const badgeContainer = document.getElementById("badge_container");
    const badgeDiv = badgeContainer.querySelector('#badge_div');
    badgeContainer.classList.add("hidden");
    badgeDiv.innerHTML = '';
}

function checkFieldsAndUpdateStyle() {
    const badgeContainer = document.getElementById("badge_container");
    const badgeDiv = badgeContainer.querySelector('#badge_div');

    const allFieldsRegex = /\{([^}]+)\}/g;
    const foundFields = textarea_message.value.match(allFieldsRegex) || [];

    const newBadgeFields = new Set(
        Array.from(badgeDiv.querySelectorAll('.badge')).map(
        (badge) => `${badge.innerText.substring(2)}`
        )
    );

    hasInvalidFields = false;
    foundFields.forEach((field) => {
        if (!newBadgeFields.has(field)) {
        hasInvalidFields = true;
        }
    });

    if (hasInvalidFields) {
        textarea_message.classList.add('underline', 'decoration-red-500', 'decoration-double');
    } else {
        textarea_message.classList.remove('underline', 'decoration-red-500', 'decoration-double');
    }
}

pick_list.addEventListener('change', async function () {
    emails = await getEmails(pick_list.value);
  
    const badgeContainer = document.getElementById("badge_container");
    const badgeDiv = badgeContainer.querySelector('#badge_div');
    const badge_fixer = '<div class="hidden"></div>';
    badgeDiv.innerHTML = badge_fixer;
  
    let badge_container_has_badge = false;
  
    for (const field of Object.keys(emails[0])) {
      if (field !== "email" && field !== "status") {
        badge_container_has_badge = true;
        const tooltip = document.createElement("div");
        tooltip.className = "tooltip";
        tooltip.setAttribute('data-tip', `e.g.: ${emails[0][field]}`);

        const fixer = document.createElement("div");
        fixer.className = "hidden";

        const badge = document.createElement("div");
        badge.className = "badge badge-primary cursor-pointer";
        badge.classList.add('text-xs');
        badge.innerHTML = `+ {${field}}`;

        tooltip.innerHTML = fixer.outerHTML + badge.outerHTML + fixer.outerHTML;
        badgeDiv.appendChild(tooltip);
      }
    }
    badgeDiv.innerHTML += badge_fixer;

    checkFieldsAndUpdateStyle();
  
    if (badge_container_has_badge) {
      badgeContainer.classList.remove("hidden");
    } else {
        badgeContainer.classList.add("hidden");
        badgeDiv.innerHTML = '';
        return;
    }
  
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
      badge.addEventListener('click', () => {
        textarea_message.value += `${badge.innerText.substring(2)}`;
      });
    });
});

textarea_message.addEventListener('input', () => {
    checkFieldsAndUpdateStyle();
});
  /** END BADGES **/