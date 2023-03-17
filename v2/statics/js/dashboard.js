async function requestForWriter(url="", data={}) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        })
    if (response.status === 201){
        alertMessage.innerText = "ثبت درخواست شما انجام شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 400) {
        alertMessage.innerText = "خطا در ثبت نام (این درخواست قبلا ارسال شده است)"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        } else {
        alertMessage.innerText = "خطا در ثبت درخواست "
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        }
    }


const requestWriter = document.getElementById('request-writer');
if (requestWriter){
    requestWriter.addEventListener('click', function (){
    requestForWriter('/dashboard/request/writer', {})
})
}


// delete post process
async function deletePostProcess(url="", data={}) {
        const response = await fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        })
    if (response.status === 204){
        alertMessage.innerText = "پست با موفقیت پاک شد، صفحه را مجدد بارگذاری کنید"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 404) {
        alertMessage.innerText = "همچین پستی نداریم"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        } else if(response.status === 403) {
        alertMessage.innerText = "شما مالک این پست نیستین "
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        } else {
        alertMessage.innerText = "خطای ناشناخته "
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }
}

const deletePost = document.getElementById('delete-post');
if (deletePost){
    deletePost.addEventListener('click', function (e){
        e.preventDefault()
    const res = deletePostProcess(e.currentTarget.parentElement.action, {})
})
}
