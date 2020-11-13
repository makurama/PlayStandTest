let getEvent = document.getElementById("search");
let EventList = document.getElementsByClassName("user_logs")[0];

getEvent.onclick = async () => {

    let firstDate = document.getElementById("first_date").value;
    let secondDate = document.getElementById("second_date").value;
    let searchNews = document.getElementById("search_news").value;
    if (firstDate != '' && secondDate != '' && searchNews != '') {
        alert('На выбор доступны промежуток дат или временной период')
    } else {
        let response = await fetch(`http://127.0.0.1:5000/statistic?start_date=${firstDate}&finish_date=${secondDate}&ready_date=${searchNews}`);
        let res = await response.json();
        console.log(res)
        if (response.ok) { // если HTTP-статус в диапазоне 200-299
            EventList.innerHTML = ""
            for (item in res){
                let result_string = document.createElement('p')
                result_string.innerText = item + ' ' + res[item].action + ' ' + res[item].datetime + ' ' + res[item].user_id + '\n'
                EventList.append(result_string)
            }
        } else {
            alert(res.ready_date ?? res._schema)
        };
        }
};