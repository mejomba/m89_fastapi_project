async function writerAccess(url="", data={}) {
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

const confirmRequestBtns = document.querySelectorAll('.confirm-request')
const rejectRequestBtns = document.querySelectorAll('.reject-request')
confirmRequestBtns.forEach(function (confirmBtn){
    confirmBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = writerAccess(confirmBtn.parentElement.action, {"user_request_action": 'ok'})
        console.log(res)
    })
})

rejectRequestBtns.forEach(function (rejectBtn){
    rejectBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = writerAccess(rejectBtn.parentElement.action, {"user_request_action": 'reject'})
        console.log(res)
    })
})
