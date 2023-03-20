async function changePostStatusOrDelete(url="", data={}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // 'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 206) {
        alertMessage.innerText = "عملیات موفق"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 401) {
        alertMessage.innerText = "خطا: برای این عملیات ابتدا وارد شوید یا صاحب این پست نیستید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 204) {
        alertMessage.innerText = "حذف پست با موفقیت انجام شد"
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


const confirmPostBtns = document.querySelectorAll('.confirm-post')
const rejectPostBtns = document.querySelectorAll('.reject-post')
const deletePostBtns = document.querySelectorAll('.delete-post')

confirmPostBtns.forEach(function (confirmBtn){
    confirmBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = changePostStatusOrDelete(confirmBtn.parentElement.parentElement.parentElement.action, {"user_action": 'ok'})
    })
})

rejectPostBtns.forEach(function (rejectBtn){
    rejectBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = changePostStatusOrDelete(rejectBtn.parentElement.parentElement.parentElement.action, {"user_action": 'reject'})
    })
})

deletePostBtns.forEach(function (deleteBtn){
    deleteBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = changePostStatusOrDelete(deleteBtn.parentElement.parentElement.parentElement.action, {"user_action": 'delete'})
    })
})