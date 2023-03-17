async function writerAccess(url="", token, data={}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // 'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 200) {
        alertMessage.innerText = "کاربر با موفقیت به روز شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 401) {
        alertMessage.innerText = "خطا: برای این عملیات ابتدا وارد شوید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else {
        alertMessage.innerText = "خطا: ناشناخته"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }
}


// const writerRequestAccept = document.getElementById('writer-request-accept');
// const writerRequestReject = document.getElementById('writer-request-reject');
const writerRequestForm = document.getElementById('writer-request-form');

writerRequestForm.addEventListener('submit', function (e) {
    e.preventDefault()
    console.log(this.ok.value)
    const res = writerAccess(this.action, localStorage.getItem('access_token') ,  {
        user_request_action: this.ok.value
    })
});
