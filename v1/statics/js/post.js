const commentSection = document.getElementById('comment-section');
const cardFooter = document.getElementById('card-footer');

const commentData = document.createElement('div')
async function createComment(url="", token, data={}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    }).then(function (res){
        if (res.status === 201) {
        alertMessage.innerText = "کامنت با موفقیت ثب شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        commentSection.insertBefore(commentData, cardFooter)
    } else if(res.status === 400) {
        alertMessage.innerText = "متن کامنت خالی است"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (res.status === 401) {
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
        return res.json()
    }).then((data) => {
        console.log(data)
        commentData.innerHTML = `<div class="card-body border m-2">
            <div class="d-flex flex-start align-items-center">
              <div class="me-2">
                <h6 class="fw-bold text-primary mb-1"> ${data.user_related.first_name}   ${data.user_related.last_name} </h6>
                <p class="text-muted small mb-0">                 
                </p>
              </div>
            </div>
                <p class="mt-3 mb-4 me-5 pb-2">
                    ${data.content} 
                </p>
                </div>`
    })
}


// create comment
const submitCommentForm = document.getElementById('submit-comment');
submitCommentForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const res = createComment(this.action, localStorage.getItem('access_token') ,  {
        content: this.commentContent.value,
        post_id: this.dataset.postid
    })
});
