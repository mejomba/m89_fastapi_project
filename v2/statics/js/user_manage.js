async function writerAccess(url="", data={}) {
    debugger
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // 'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    })
    if (response.status === 200) {
        alertMessage.innerText = "کاربر با موفقیت به روز شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 401) {
        alertMessage.innerText = "خطا: برای این عملیات ابتدا وارد شوید"
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


// const writerRequestAccept = document.getElementById('writer-request-accept');
// const writerRequestReject = document.getElementById('writer-request-reject');
const writerRequestForms = document.querySelectorAll('.writer-request-form');
writerRequestForms.forEach(function(form){
   form.addEventListener('submit', function(e){
      e.preventDefault()
      console.log(e.currentTarget)
   })
   console.log(form.children[1])
   console.log(form)
})
//const confirm_button = document.getElementById('confirm-request')
//confirm_button.addEventListener('click',function(e){
//   const res = writerAccess(e.currentTarget.parentElement.action, localStorage.getItem('access_token') ,  {
//        user_request_action: "ok"
//    })
//})
//const reject_button = document.getElementById('reject-request')
//reject_button.addEventListener('click',function(e){
//   const res = writerAccess(e.currentTarget.parentElement.action, localStorage.getItem('access_token') ,  {
//        user_request_action: "reject"
//    })
//})
//writerRequestForm.addEventListener('submit', function (e) {
//    e.preventDefault()
//    console.log(this.ok.value)
//    console.log(this.action)
//    console.log(e.target)
//    console.log(e.currentTarget)
//    console.log(e.currentTarget.parent)
//    console.log(e.target.parent)
//    const res = writerAccess(this.action, localStorage.getItem('access_token') ,  {
//        user_request_action: this.ok.value
//    })
//});
