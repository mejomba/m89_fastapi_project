async function updateUserByAdmin(url="", token, method, data={}) {
    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 204) {
        console.log('ثبت شد')
        alertMessage.innerText = "کاربر حذف شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if(response.status === 206) {
        alertMessage.innerText = "کاربر بروز شد"
        userAlert.classList.remove('alert-danger');
        userAlert.classList.add('alert-success');
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


const deleteUserByAdminForm = document.getElementById('delete-user-by-admin')
const updateUserByAdminForm = document.getElementById('update-user-by-admin')

deleteUserByAdminForm.addEventListener('submit', function (e){
    e.preventDefault()
    updateUserByAdmin(this.action, localStorage.getItem('access_token'), 'DELETE', {})
})

updateUserByAdminForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const selectRole = this.querySelector('#user-role').value
    console.log(this.firstElementChild.firstElementChild)
    updateUserByAdmin(this.action, localStorage.getItem('access_token'), 'PUT', {
        role: selectRole
    })
})