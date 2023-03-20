async function updatePost(url="", token, data={}) {
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
        alertMessage.innerText = "پست با موفقیت بروز شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }else if(response.status === 403) {
        alertMessage.innerText = "برای ایجاد پست باید نویسنده باشید، از پروفایل، منو کناری درخواست نویسنده شدن بدهید"
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



// update post

function updateFileSelect(image_file){
      const reader = new FileReader()
      reader.onload = updateFileLoad;
      reader.readAsDataURL(image_file)
}

function updateFileLoad(event){
    const formData = new FormData(updatePostForm)
    console.log("remove post: ",formData.get('remove_post_image'))
        updatePost(this.action, localStorage.getItem('access_token'), {
        title: formData.get('post_title'),
        content: formData.get('post_content'),
        image: event.target.result,
        remove_image: formData.get('remove_post_image')
    });
}

const updatePostForm = document.getElementById('update-post-form');
updatePostForm.addEventListener('submit', function (e){
    e.preventDefault()
    const update_post_image = e.currentTarget.update_post_image.files[0]
    if (update_post_image){
        updateFileSelect(update_post_image)
    }else {
        updateFileLoad(e)
    }

});

// const updatePostForm = document.getElementById('update-post-form');
// updatePostForm.addEventListener('submit', function (e){
//     e.preventDefault()
//     const update_post_image = e.currentTarget.update_post_image.files[0]
//     if (update_post_image){
//         handleFileSelect(update_post_image)
//     }else {
//         handleFileLoad(e, updatePostForm)
//     }
// });


// updatePostForm.addEventListener('submit', function (e) {
//     e.preventDefault()
//     const res = updatePost(this.action, localStorage.getItem('access_token') ,  {
//         title: this.updateposttitle.value,
//         content: this.updatepostcontent.value,
//     })
// });


