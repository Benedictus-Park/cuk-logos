let pwd_chk_element = document.getElementById("pwd_chk");

pwd_chk_element.onkeydown = (e) => {
    if(e.key == "Enter"){
        document.getElementById("btnResetPwd").click();
    }
}

document.getElementById("btnResetPwd").onclick = () => {
    let pwd = document.getElementById("pwd").value;
    let pwd_chk = pwd_chk_element.value;
    let key = location.href.split('key=')[1];

    if(!pwd || !pwd_chk){
        alert("모든 칸을 입력하시오.");
        return;
    }
    else if(pwd != pwd_chk){
        alert("패스워드를 다시 확인하시오.");
        return;
    }
    else if(pwd.length < 8){
        alert("거 패스워드가 너무 짧은 거 아니오?");
        return;
    }
    else{
        fetch("http://127.0.0.1:4444/reset-pwd", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                "pwd":pwd,
                "pwd_chk":pwd_chk,
                "key":key
            })
        }).then((rsp) => {
            if(rsp.ok){
                alert("재설정 성공! 앞으로는 정신 똑띠 차리라우.");
                location.href = "index.html";
            }
            else{
                rsp.text().then((txt) => {
                    alert(txt);
                });
            }
        })
    }
}