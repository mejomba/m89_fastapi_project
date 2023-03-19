async function changeCommentStatusOrDelete(url="", data={}) {
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
        alertMessage.innerText = "خطا: برای این عملیات ابتدا وارد شوید یا صاحب این کامنت نیستید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 204) {
        alertMessage.innerText = "حذف کامنت با موفقیت انجام شد"
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


const confirmCommentBtns = document.querySelectorAll('.confirm-comment')
const rejectCommentBtns = document.querySelectorAll('.reject-comment')
const deleteCommentBtns = document.querySelectorAll('.delete-comment')

confirmCommentBtns.forEach(function (confirmBtn){
    console.log(confirmBtn)
    console.log(confirmBtn.parentElement.parentElement.parentElement.action)
    confirmBtn.addEventListener('click', function (e){
        console.log(confirmBtn.parentElement.parentElement.parentElement.action)
        e.preventDefault()
        const res = changeCommentStatusOrDelete(confirmBtn.parentElement.parentElement.parentElement.action, {"user_action": 'ok'})
        console.log(res)
    })
})

rejectCommentBtns.forEach(function (rejectBtn){
    console.log(rejectBtn)
    console.log(rejectBtn.parentElement.parentElement.parentElement.action)
    rejectBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = changeCommentStatusOrDelete(rejectBtn.parentElement.parentElement.parentElement.action, {"user_action": 'reject'})
        console.log(res)
    })
})

deleteCommentBtns.forEach(function (deleteBtn){
    console.log(deleteBtn)
    console.log(deleteBtn.parentElement.parentElement.parentElement.action)
    deleteBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = changeCommentStatusOrDelete(deleteBtn.parentElement.parentElement.parentElement.action, {"user_action": 'delete'})
        console.log(res)
    })
})