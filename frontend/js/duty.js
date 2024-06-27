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