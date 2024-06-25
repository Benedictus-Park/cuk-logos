document.getElementById("pwd").onkeydown = (e) => {
    if(e.key == "Enter"){
        document.getElementById("btnSuicide").click();
    }
}

document.getElementById("btnSuicide").onclick = () => {
    let pwd = document.getElementById("pwd").value;
    
    if(!pwd){
        alert("입력된 게 없는디...");
        return;
    }
    else{
        fetch("http://127.0.0.1:4444/withdraw", {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "authorization":sessionStorage.getItem('jwt')
            },
            body:JSON.stringify({
                "pwd":pwd,
            })
        }).then((rsp) => {
            if(rsp.ok){
                alert("아아... 그는 갔습니다... 잘 가시오 " + sessionStorage.getItem('name') + " 동지");
                sessionStorage.clear();
                location.href = 'index.html';
                return;
            }
            else{
                rsp.text().then((txt) => {
                    alert(txt);
                });
            }
        });
    }
}