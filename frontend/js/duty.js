fetch("http://127.0.0.1:4444/sync-duty", {
    method:"POST",
    headers:{
        "Content-Type":"application/json",
        "Authorization":sessionStorage.getItem("jwt")
    }
}).then((rsp) => {
    if(rsp.ok){
        rsp.json().then((json) => {
            let duties = json['duties'];

            sessionStorage.setItem('jwt', json['jwt']);

            for(let i = 0; i < duties.length; i++){
                let row = document.createElement('tr');

                for(let j = 0; j < 4; j++){
                    row.appendChild(document.createElement('td'));
                }

                row.childNodes[0].textContent = duties[i][0];
                row.childNodes[1].textContent = duties[i][1];
                row.childNodes[2].textContent = duties[i][2];

                document.getElementById("tbody").appendChild(row);
            }
        });
    }
    else{
        alert("아마 GSpread에 너무 많은 요청을 보낸 것 같습니다. 1분 기다려 주세요.");
    }
});

document.getElementById("btnFill_thisMonth").addEventListener('click', () => {
    fetch("http://127.0.0.1:4444/fill-gspread-date", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authorization":sessionStorage.getItem("jwt")
        },
        body:JSON.stringify({
            "month_plus":0
        })
    }).then((rsp) => {
        if(rsp.ok){
            rsp.json().then((json) => {
                sessionStorage.setItem('jwt', json['jwt']);
            });
        }
    });
});

document.getElementById("btnFill_nextMonth").addEventListener('click', () => {
    fetch("http://127.0.0.1:4444/fill-gspread-date", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authorization":sessionStorage.getItem("jwt")
        },
        body:JSON.stringify({
            "month_plus":1
        })
    }).then((rsp) => {
        if(rsp.ok){
            rsp.json().then((json) => {
                sessionStorage.setItem('jwt', json['jwt']);
            });
        }
    });
});