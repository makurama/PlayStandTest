let modal = document.getElementById("login_modal");
let btn = document.getElementById("modal_sign");
let logoutBtn = document.getElementById("logout_bnt");
let account = document.getElementById("my_account");
let span = document.getElementsByClassName("close_modal")[0];
let SlideIndex = 1;
let sendBtn = document.getElementById("send_auth");
let a = document.getElementById("user_registration");
let regButton = document.getElementById("send_reg");
let errorMessage = document.getElementById("error_message");
let userNews = document.getElementsByClassName("user_news")[0];
let contactData = document.getElementById("contact_data");
window.eventmass = []

//Слайдер
showSlides(SlideIndex);

btn.onclick = () => {
    modal.style.display = "block";
    eventmass.push({datetime: GetDate(), action: "modal open"})
}


window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
        regButton.style.display = "none";
        sendBtn.style.display = "inline";
        a.style.display = "inline";
        errorMessage.innerText = '';
        errorMessage.style.borderBottom = 'none';
        document.getElementById("send_log").value = '';
        document.getElementById("send_pass").value = '';
        eventmass.push({datetime: GetDate(), action: "modal close"})
    }
}

let plusSlides = (n) => {
    showSlides(SlideIndex += n);
    eventmass.push({datetime: GetDate(), action: "carousel click"})
};

//получение текущей даты
let GetDate = () => {
    let date = new Date();
    let format_date = (date.getDate() + "-" + (date.getMonth()+1) + "-" + date.getFullYear() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds())
    return format_date
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("slide");
    
    if (n > slides.length) {
        SlideIndex = 1;
    }
    if (n < 1) {
        SlideIndex = slides.length;
    };
    
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    };
    
    slides[SlideIndex - 1].style.display = "block";
};

//Авторизация
sendBtn.onclick = async () => {
    let login = document.getElementById("send_log").value;
    let pass = document.getElementById("send_pass").value;
    document.getElementById("send_log").value = '';
    document.getElementById("send_pass").value = '';
    errorMessage.innerText = '';
    errorMessage.style.borderBottom = 'none';

    let user = {
        login: login,
        password: pass
    };
    //в другую функцию что ниже нужно бы вынести
    let response = await fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
    });

    let res = await response.json();
    
    if (response.status === 400) {
        errorMessage.innerText = (res?.password?.[0] ?? '') + '\n' + (res?.login?.[0] ?? '');
        errorMessage.style.display = "block";
        errorMessage.style.borderBottom = '2px solid black';
    } else if (response.status === 404) {
        errorMessage.innerText = res.answer;
        errorMessage.style.display = "block";    
        errorMessage.style.borderBottom = '2px solid black';
    } else {
        eventmass.push({datetime: GetDate(), action: "authorization"});
        modal.style.display = "none";
        btn.style.display = "none";
        account.style.display = "inline";
        logoutBtn.style.display = "inline";
    }

    let responseTodayNews = await fetch(`http://127.0.0.1:5000/news`);
    let respNews = await responseTodayNews.json()

    for (item in respNews){
        InnerNews(respNews)
        }
};

//создание новостей
let InnerNews = (respNews) => {
    let siteName = document.createElement('h3')
    let title = document.createElement('p')
    let description = document.createElement('p')
    let datetime = document.createElement('p')

    siteName.innerText = respNews[item].siteName
    description.innerText = respNews[item].description
    datetime.innerText = respNews[item].datetime
    title.innerHTML = `<a href=${respNews[item].urlNews} class="site_go_url">${respNews[item].title}<\a>`


    siteName.style.cssText = `font-size: 15px; margin: 30px 0 5px 0;`
    title.style.cssText = `font-size: 25px; margin: 0 0 5px 0;`
    description.style.cssText = `font-size: 20px; margin: 0 0 5px 0;`
    datetime.style.cssText = `font-size: 15px; margin: 0;`

    userNews.append(siteName, title, description, datetime)                    
};

//на форму регистрации
a.onclick = () => {
    regButton.style.display = "inline";
    regButton.style.width = "110px";
    sendBtn.style.display = "none";
    a.style.display = "none";
    document.getElementById("send_log").value = '';
    document.getElementById("send_pass").value = '';
    errorMessage.innerText = '';
    errorMessage.style.borderBottom = 'none';  
    eventmass.push({datetime: GetDate(), action: "open registration form"})
};
  
//Регистрация                                  
regButton.onclick = async () => {
    let login = document.getElementById("send_log").value;
    let pass = document.getElementById("send_pass").value;
    let user = {
    login: login,
    password: pass
    };

    let response = await fetch('http://127.0.0.1:5000/user', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
    });

    let res = await response.json();
    
    if (response.status === 400) {
        errorMessage.innerText = (res?.password?.[0] ?? '') + '\n' + (res?.login?.[0] ?? '') + (res?.answer ?? '');
        errorMessage.style.display = "block";
        errorMessage.style.borderBottom = '2px solid black';
    } else {
        eventmass.push({datetime: GetDate(), action: "registration"})
        let userReturn = await fetch(' http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
        });

        let res = await userReturn.json();

        modal.style.display = "none";
        btn.style.display = "none";
        account.style.display = "inline";
        logoutBtn.style.display = "inline";

        let responseTodayNews = await fetch(`http://127.0.0.1:5000/news`);

        let respNews = await responseTodayNews.json()

        for (item in respNews){
            InnerNews(respNews)
            }

}}

//выход
logoutBtn.onclick = async () => {
    send_event()
    await fetch(' http://127.0.0.1:5000/auth/logout', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        }
    });
    btn.style.display = "inline";
    account.style.display = "none";
    logoutBtn.style.display = "none";
    userNews.innerHTML = ""
}


//Learn more
let leadMore = document.getElementById("lead_more");
var counter = 1;
leadMore.onclick = async () => {

                        
    let response = await fetch(`http://127.0.0.1:5000/news?counter_news=${counter}&start_date=${window.firstDate}&finish_date=${ window.secondDate}&key_word=${window.searchNews}`);
    counter += 1;
    let res = await response.json();
     if (response.ok) { // если HTTP-статус в диапазоне 200-299
        for (item in res){
            InnerNews(res)
        }
    } else {
            alert(res.answer)        
        }
    eventmass.push({datetime: GetDate(), action: "learn more news"})
};

//fistDate
//seconDdate        
//keyWord 
let checkInputSearch = (first_date, second_date, key_word) =>{
    if (first_date != ''){
        eventmass.push({datetime: GetDate(), action: "introduced fisrt date"})
    }    
    if (second_date != ''){
        eventmass.push({datetime: GetDate(), action: "introduced second date"})
    }   
    if (key_word != ''){
        eventmass.push({datetime: GetDate(), action: "introduced key word"})
    }   
}
        
//contact us
contactData.onclick = () => eventmass.push({datetime: GetDate(), action: "contact us"});
//myAccount
account.onclick = () => eventmass.push({datetime: GetDate(), action: "go in account"})
//facebook inst vk
let contact_url = document.querySelectorAll(".contact")
for (let i = 0; i < contact_url.length; i++) {
  contact_url[i].onclick = function(){
    eventmass.push({datetime: GetDate(), action: "social networks"})
  };
}
//site url
function on(node, event, className, cb) {
	addEventListener(event, (e) => {
  	if (!e.target.classList.contains(className)) {
    	return false
    }
    cb(e)
  })
}
on(userNews, 'click', 'site_go_url', e => {
  eventmass.push({datetime: GetDate(), action: "go news site"})
})


//Поиск
let getNews = document.getElementById("search");

getNews.onclick = async () => {
    window.firstDate = document.getElementById("first_date").value;
    window.secondDate = document.getElementById("second_date").value;
    window.searchNews = document.getElementById("search_news").value;
    
    checkInputSearch(firstDate, secondDate, searchNews)

    let response = await fetch(`http://127.0.0.1:5000/news?counter_news=0&start_date=${firstDate}&finish_date=${secondDate}&key_word=${searchNews}`);
    let res = await response.json();

    if (response.ok) { // если HTTP-статус в диапазоне 200-299
        userNews.innerHTML = ""
        leadMore.style.display = "inline";
        for (item in res){
            InnerNews(res)
        }
    } else {
        alert(res.answer ?? res._schema)
    };
    eventmass.push({datetime: GetDate(), action: "search news"})
};


let send_event = () => {
    let events = {event: eventmass}
    fetch('http://127.0.0.1:5000/statistic', {
    method: 'POST',
    mode: 'cors',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(events)
    });
}

onbeforeunload = function() {
    send_event()
    return ''
};