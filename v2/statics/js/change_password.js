async function changePassword(url="", token, data={}) {
    const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 206) {
        alertMessage.innerText = "اطلاعات با موفقیت بروز شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if(response.status === 400) {
        alertMessage.innerText = "تکرار رمز عبور نامعتبر"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if(response.status === 406) {
        alertMessage.innerText = "رمز عبور اشتباه"
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

const changePasswordForm = document.getElementById('change-password-form')
changePasswordForm.addEventListener('submit', function (e) {
    e.preventDefault()
    changePassword(this.action, localStorage.getItem('access_token'), {
        password_old: this.password.value,
        password: this.password1.value,
        password_repeat: this.password2.value
    })
})