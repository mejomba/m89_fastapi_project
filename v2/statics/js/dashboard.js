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
requestWriter.addEventListener('click', function (){
    requestForWriter('/dashboard/request/writer', {})
})