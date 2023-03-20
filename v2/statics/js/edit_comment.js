async function editComment(url="", token, data={}) {
    const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 206) {
        console.log('ثبت شد')
        alertMessage.innerText = "کامنت با موفقیت بروز شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }else if(response.status === 403) {
        alertMessage.innerText = "شما مالک این کامنت نیستین"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if(response.status === 400) {
        alertMessage.innerText = "فیلدهای ورودی اجباری هستن"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if(response.status === 401) {
        alertMessage.innerText = "ابتدا وارد شوید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else {
        alertMessage.innerText = "خطا: فیلد های ورودی را چک کنید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }
}



// edit comment
const updateCommentForm = document.getElementById('update-comment-form');
updateCommentForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const res = editComment(this.action, localStorage.getItem('access_token') ,  {
        content: this.updatecommentcontent.value
    })
});


