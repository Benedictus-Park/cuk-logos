document.getElementById("authcode").onkeydown = (e) => {
    if(e.key == "Enter"){
        document.getElementById("btnRegistration").click();
    }
}

document.getElementById("btnRegistration").onclick = () => {
    let email = document.getElementById("email").value;
    let pwd = document.getElementById("pwd").value;
    let pwd_chk = document.getElementById("pwd_chk").value;
    let authcode = document.getElementById("authcode").value;

    if(!email || !pwd || !pwd_chk || !authcode){
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
    else if(authcode.length != 6){
        alert("인증번호 그거 아닌 것 같은디");
        return;
    }
    
    fetch("http://127.0.0.1:4444/registration", {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            "email":email,
            "pwd":pwd,
            "pwd_chk":pwd_chk,
            "authcode":authcode
        })
    }).then((rsp) => {
        rsp.text().then((txt) => {
            alert(txt);
        });

        if(rsp.ok){
            location.href = "index.html";
        }
    });
}