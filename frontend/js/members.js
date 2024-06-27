fetch("http://127.0.0.1:4444/get-all-members", {
    method:"POST",
    headers:{
        "Content-Type":"application/json",
        "Authorization":sessionStorage.getItem("jwt")
    }
}).then((rsp) => setTable(rsp));

document.getElementById("btnSync").addEventListener("click", () => {
    fetch("http://127.0.0.1:4444/sync-members", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authorization":sessionStorage.getItem("jwt")
        }
    }).then((rsp) => setTable(rsp));
});

function setTable(rsp){
    if(rsp.ok){
        document.getElementById("tbody").innerHTML = "";
        
        rsp.json().then((json) => {
            let members = json['members'];

            sessionStorage.setItem('jwt', json['jwt']);
            members.sort((a, b) => Number(a[0]) - Number(b[0]));

            for(let i = 0; i < members.length; i++){
                let row = document.createElement('tr');

                for(let j = 0; j < 6; j++){
                    row.appendChild(document.createElement('td'));
                }
            
                row.childNodes[0].textContent = members[i][0];
                row.childNodes[1].textContent = members[i][1];
                row.childNodes[2].textContent = members[i][4];
                row.childNodes[3].textContent = members[i][5];
                row.childNodes[4].textContent = members[i][6];
                row.childNodes[5].textContent = members[i][2];

                document.getElementById("tbody").appendChild(row);
            }
        });
    }
    else{
        alert("아마 GSpread에 너무 많은 요청을 보낸 것 같습니다. 1분 기다려 주세요.");
    }
}