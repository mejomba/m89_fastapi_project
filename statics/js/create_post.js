async function createPost(url="", token, data={}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 201) {
        console.log('ثبت شد')
        alertMessage.innerText = "پست با موفقیت ثب شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }else if(response.status === 403) {
        alertMessage.innerText = "برای ایجاد پست باید نویسنده باشید، از منو کناری درخواست نویسنده شدن بدهید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }
    else if(response.status === 400) {
        console.log('title and content required')
        alertMessage.innerText = "برای ایجاد پست باید نویسنده باشید، از منو کناری درخواست نویسنده شدن بدهید"
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



// create post
createPostForm = document.getElementById('create-post-form');
createPostForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const res = createPost(this.action, localStorage.getItem('access_token') ,  {
        title: this.posttitle.value,
        content: this.postcontent.value
    })
    console.log(res)
});


