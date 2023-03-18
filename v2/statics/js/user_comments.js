async function commentDelete(url="", data={}) {
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

const deleteCommentBtns = document.querySelectorAll('.delete-comment')

deleteCommentBtns.forEach(function (deleteBtn){
    deleteBtn.addEventListener('click', function (e){
        e.preventDefault()
        const res = commentDelete(deleteBtn.parentElement.parentElement.parentElement.action, {"user_action": 'delete'})
    })
})