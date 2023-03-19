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
        alertMessage.innerText = "برای ایجاد پست باید نویسنده باشید، از پروفایل، منو کناری درخواست نویسنده شدن بدهید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }else if(response.status === 406) {
        alertMessage.innerText = "خطا: اشکال در تصویر فرمت فایل را بررسی کنید"
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
    }else if(response.status === 500) {
        alertMessage.innerText = "خطا در ثب پست"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }else {
        alertMessage.innerText = "خطا: فیلد های ورودی را چک کنید"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    }
}






const createPostForm = document.getElementById('create-post-form');
// function init(){
//       document.getElementById('postimage').addEventListener('change', handleFileSelect, false);
//     }

function handleFileSelect(image_file){
  const reader = new FileReader()
  reader.onload = handleFileLoad;
  reader.readAsDataURL(image_file)
}

function handleFileLoad(event){
    const formData = new FormData(createPostForm)
    console.log(this.action)
    createPost(this.action, localStorage.getItem('access_token'), {
        title: formData.get('post_title'),
        content: formData.get('post_content'),
        image: event.target.result
    });
}
createPostForm.addEventListener('submit', function (e){
    e.preventDefault()
    handleFileSelect(e.currentTarget.post_image.files[0])
});

// createPostForm.addEventListener('submit', function (e){
//     e.preventDefault()
//     console.log('salam')
// });

// function handleFileLoad(event){
//     const createPostForm = document.getElementById('create-post-form');
//     createPostForm.addEventListener('submit', function (e) {
//         e.preventDefault()
//         // const newdata = new FormData($('#create-post-form')[0])
//         const newdata = new FormData(createPostForm)
//         const res = createPost(this.action, localStorage.getItem('access_token'), {
//             title: newdata.get('post_title'),
//             content: newdata.get('post_content'),
//             image: event.target.result
//         })
//     });
// }




// create post

// createPostForm = document.getElementById('create-post-form');
// createPostForm.addEventListener('submit', function (e) {
//     e.preventDefault()
    // const newdata = new FormData($('#create-post-form')[0])


    // convertImageToBase64(newdata.get('postimage'), console.log)
    // const res = createPost(this.action, localStorage.getItem('access_token'), {
        // title: newdata.get('post_title'),
        // content: newdata.get('post_content'),
        // image: newdata.get('post_image')
    // })
// });




