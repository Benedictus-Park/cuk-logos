fetch("http://127.0.0.1:4444/get-scoretable", {
    method:"POST",
    headers:{
        "Content-Type":"application/json",
        "Authorization":sessionStorage.getItem("jwt")
    }
}).then((rsp) => setTable(rsp));

document.getElementById("btnSync").addEventListener('click', () => {
    fetch("http://127.0.0.1:4444/sync-scoretable", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authorization":sessionStorage.getItem("jwt")
        }
    }).then((rsp) => setTable(rsp));
});

function setTable(rsp){
    document.getElementById("tbody").innerHTML = "";

    if(rsp.ok){
        rsp.json().then((json) => {
            let subjects = json['subjects'];

            sessionStorage.setItem('jwt', json['jwt']);
            subjects.sort((a, b) => Number(a[0]) - Number(b[0]));

            for(let i = 0; i < subjects.length; i++){
                let row = document.createElement('tr');

                for(let j = 0; j < 6; j++){
                    row.appendChild(document.createElement('td'));
                }
            
                row.childNodes[0].textContent = subjects[i][0];
                row.childNodes[1].textContent = subjects[i][1];
                row.childNodes[2].textContent = subjects[i][2];

                document.getElementById("tbody").appendChild(row);
            }
        });
    }
    else{
        alert("아마 GSpread에 너무 많은 요청을 보낸 것 같습니다. 1분 기다려 주세요.");
    }
}