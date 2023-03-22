async function updateUser(url="", token, data={}) {
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
        alertMessage.innerText = "اطلاعات با موفقیت بروز شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if(response.status === 400) {
        alertMessage.innerText = "فرمت تلفن اشتباه"
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



// update user
function updateProfileImageSelect(image_file){
      const reader = new FileReader()
      reader.onload = updateProfileImageFileLoad;
      reader.readAsDataURL(image_file)
}

function updateProfileImageFileLoad(event){
    const formData = new FormData(updateUserForm)
        updateUser(this.action, localStorage.getItem('access_token'), {
        username: formData.get('username'),
        password: formData.get('password'),
        email: formData.get('email'),
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        phone: formData.get('phone'),
        image: event.target.result,
        remove_image: formData.get('remove_user_image')
    });
}

const updateUserForm = document.getElementById('update-user-form')
updateUserForm.addEventListener('submit', function (e){
    e.preventDefault()
    const update_user_image = e.currentTarget.update_user_image.files[0]
    if (update_user_image){
        updateProfileImageSelect(update_user_image)
    }else {
        updateProfileImageFileLoad(e)
    }

});
