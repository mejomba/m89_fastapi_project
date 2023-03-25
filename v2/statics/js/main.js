const modalBtn = document.querySelector('.modal-btn');
const closelBtn = document.querySelector('.close-btn');
const modal = document.querySelector('.modal-overlay');
const modalContainer = document.querySelector('.modal-container');

modalBtn.addEventListener('click', function() {
 modal.classList.toggle('open-modal');
})

closelBtn.addEventListener('click', function() {
 modal.classList.remove('open-modal');
})

modalContainer.addEventListener('overflow', function(e) {
 e.currentTarget.style.overflowY = 'scroll';
})

// switch login and signup form
const login = document.getElementById('login');
const signup = document.getElementById('signup');
const loginFormWrapper = document.getElementById('login-form-wrapper');
const signupFormWrapper = document.getElementById('signup-form-wrapper');
login.addEventListener('click', ()=> {
    loginFormWrapper.classList.remove('d-none');
    signupFormWrapper.classList.add('d-none')
    login.classList.add('bg-info');
    signup.classList.remove('bg-info');
})
signup.addEventListener('click', ()=> {
    loginFormWrapper.classList.add('d-none');
    signupFormWrapper.classList.remove('d-none')
    login.classList.remove('bg-info');
    signup.classList.add('bg-info');
})

const userAlert = document.getElementById('alert');
const alertMessage = document.getElementById('alert-message');
const closeAlert = document.querySelector('.close-alert');
closeAlert.addEventListener('click', function (){
    userAlert.classList.add('d-none')
})
        // signup process
async function signUp(url="", data={}) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        })
    if (response.status === 201){
        alertMessage.innerText = "ثبت نام شما انجام شد"
        userAlert.classList.add('alert-success');
        userAlert.classList.remove('alert-danger');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
    } else if (response.status === 409) {
        alertMessage.innerText = "خطا در ثبت نام (ایمیل یا نام کاربری تکراری)"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        }else if (response.status === 400) {
        alertMessage.innerText = "خطا در ثبت نام (شماره تلفن نامعتبر)"
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        } else {
        alertMessage.innerText = "خطا در ثبت نام "
        userAlert.classList.add('alert-danger');
        userAlert.classList.remove('alert-success');
        userAlert.classList.remove('d-none');
        modal.classList.remove('open-modal');
        }
    }

signupForm = document.getElementById('signup-form');
signupForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const res = signUp(this.action, {
        email: this.email.value,
        username: this.username.value,
        password: this.password.value,
        first_name: this.first_name.value,
        last_name: this.last_name.value,
        phone: this.phone.value
    })
    console.log(res)
})


// login process
const headerBtn = document.getElementById('header-btn');
async function loginUser(url="", data={}) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }).then(function (res){
            console.log(res.status)
            return res.json()
        })
            .then((data) => {
                if (data.access_token){
                    localStorage.setItem('access_token', data.access_token)
                    window.location.replace('');

                    alertMessage.innerText = "ورود موفق"
                    userAlert.classList.add('alert-success');
                    userAlert.classList.remove('alert-danger');
                    userAlert.classList.remove('d-none');
                    modal.classList.remove('open-modal');
                } else {
                    alertMessage.innerText = "نام کاربری یا رمز عبور اشتباه"
                    userAlert.classList.add('alert-danger');
                    userAlert.classList.remove('d-none');
                    modal.classList.remove('open-modal');

                }
            }).catch(err => {
                alert(err)
            })
    }
loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const res = loginUser(this.action, {
        email: this.email.value,
        password: this.password.value
    })
})

// load profile
function fetchProfile(token){
    fetch('/dashboard', {
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        }
    }).then(response=>response.text())
        .then(data=>{
            document.body.innerHTML = data;
        })
}

function get_cookie(name){
    return document.cookie.split(';').some(c => {
        return c.trim().startsWith(name + '=');
    });
}

function delete_cookie( name, path, domain ) {
  if( get_cookie( name ) ) {
    document.cookie = name + "=" +
      ((path) ? ";path="+path:"")+
      ((domain)?";domain="+domain:"") +
      ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
  }
}

// logout process
function logout(token) {
    fetch('/logout', {
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        if (response.status === 200) {
            delete_cookie('access_token')
            localStorage.removeItem('access_token');
        }
        response.text().then((data) => {
            delete_cookie('access_token')
            localStorage.removeItem('access_token');
            window.location.replace('/')
            document.body.innerHTML = data
            console.log(localStorage.getItem('access_token'))
        })
    })
}

    function getPostByUserName(username, token){
    fetch(`/users/${username}`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        response.text().then((data) => {
            document.body.innerHTML = data
        })
    })
    }


// const searchForm = document.getElementById('search-form')
// searchForm.addEventListener('submit', function (e) {
//     e.preventDefault()
// })