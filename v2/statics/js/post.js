const commentSection = document.getElementById('comment-section');
const cardFooter = document.getElementById('card-footer');

const commentData = document.createElement('div')
commentData.innerHTML = `<div class="card-body border m-2">
            <div class="d-flex flex-start align-items-center">
              <img class="rounded-circle shadow-1-strong me-3"
                src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(19).webp" alt="avatar" width="60"
                height="60" />
              <div class="me-2">
                <h6 class="fw-bold text-primary mb-1"> comment.user_related.first_name   comment.user_related.last_name </h6>
                <p class="text-muted small mb-0">
                     comment.publish_date.date() 
                </p>
              </div>
            </div>
                <p class="mt-3 mb-4 me-5 pb-2">
                    comment content 
                </p>
                </div>`

async function createComment(url="", token, data={}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 201) {
        alertMessage.innerText = "کامنت با موفقیت ثب شد وپس از تایید نمایش داده میشود"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        // commentSection.insertBefore(commentData, cardFooter)
    } else if(response.status === 400) {
        alertMessage.innerText = "متن کامنت خالی است"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 401) {
        alertMessage.innerText = "خطا: برای نظر دادن ابتدا وارد شوید"
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


// create comment
const submitCommentForm = document.getElementById('submit-comment');
submitCommentForm.addEventListener('submit', function (e) {
    console.log(this.commentContent.value);
    e.preventDefault()
    const res = createComment(this.action, localStorage.getItem('access_token') ,  {
        content: this.commentContent.value,
        post_id: this.dataset.postid
    })
});


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
        commentDelete(deleteBtn.parentElement.parentElement.parentElement.action, {"user_action": 'delete'})
    })
})