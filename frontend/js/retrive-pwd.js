let btnSubmit = document.getElementById("btnSubmit");

document.getElementById("email").onkeydown = (e) => {
    if(e.key == "Enter"){
        btnSubmit.click();
    }
};

btnSubmit.onclick = () => {
    let email = document.getElementById("email").value;

    if(!email){
        alert("이메일 입력을 안 했잖소?");
        return;
    }

    fetch("http://127.0.0.1:4444/retrive-pwd-req", {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            "email":email,
        })
    }).then((rsp) => {
        if(rsp.ok){
            alert("이메일을 확인하여 패스워드를 재설정하시오.");
            location.href = "index.html";
        }
        else{
            rsp.text().then((txt) => {
                alert(txt);
            });
        }
    });
};