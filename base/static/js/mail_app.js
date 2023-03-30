// Add event listeners to the drop zone
var dropZone = document.querySelector('#drop-zone');
dropZone.addEventListener('dragover', function(event) {
    event.preventDefault();
    this.classList.add('active');
});
dropZone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    this.classList.remove('active');
});
dropZone.addEventListener('drop', function(event) {
    event.preventDefault();
    this.classList.remove('active');
    var files = event.dataTransfer.files;
    handleFiles(files);
});

// Add event listener to the file input field
var fileInput = document.querySelector('#attachment');
fileInput.addEventListener('change', function(event) {
    var files = event.target.files;
    handleFiles(files);
});

 // Add click event listener to the drop zone
 dropZone.addEventListener('click', function(event) {
    event.preventDefault();
    fileInput.click();
});

// Function to handle the selected files
function handleFiles(files) {
    console.log(files);
    if (files.length === 0) {
        return;
    }

    // Update the drop zone border to show the file name
    var dropZone = document.querySelector('#drop-zone');
    dropZone.classList.add('has-file');
    var fileName = files[0].name;
    if (files.length > 1) {
        fileName = files.length + ' files selected';
    }
    dropZone.setAttribute('data-name', fileName);

    console.log(files.pattern)

    // Your code to handle the selected files here
}


const apiUrl = 'https://api.elasticemail.com/v2/email/send';
const apiKey = '1AE90F9EA7AD6700F4891A3A548805AD389EC999501F39F74155CB0ABF3EE9B603E768D37CC12053C3C8B587C5801965';
const apiMail = 'info@sellervibe.co'

const recipient_list = document.getElementById('recipient');
const yourName = document.getElementById('name');
const yourEmail = document.getElementById('email');
const subject = document.getElementById('subject');
const message = document.getElementById('message');

const sendEmail = async () => {
    let i = 0;
    const intervalId = setInterval(() => {
    if (i >= 100) {
        clearInterval(intervalId);
    } else {
        i++;
        progressBarValue.style.width = `${i}%`;
    //   progressBarValue.innerText = `${i}%`;
    }
    }, 50);

pattern = [
    `&subject=${subject.value}`,
    `&from=${apiMail}`,
    `&fromName=${yourName.value}`,
    `&replyTo=${yourEmail.value}`,
    `&to=${recipient_list.value.trim()}`,
    `&bodyText=${encodeURIComponent(message.value)}`,
]

const response = await fetch(`${apiUrl}?apikey=${apiKey}${pattern.map(item => item).join('')}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    }
    });
    clearInterval(intervalId);
    if (!response.ok) {
    throw new Error(response.statusText);
    }
};

const progressBar = document.getElementById('progress-bar');
const progressBarValue = document.getElementById('progress-bar-value');
const button = document.getElementById('send-email-button');
button.addEventListener('click', async () => {
    progressBar.style.display = 'block';
    try {
    await sendEmail();
    progressBar.style.display = 'none';
    console.log('Email sent successfully');
    } catch (error) {
    progressBar.style.display = 'none';
    console.error(error);
    }
});