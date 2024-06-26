document.getElementById("pwd").onkeydown = (e) => {
    if(e.key == "Enter"){
        document.getElementById("btnLogin").click();
    }
}

document.getElementById("btnLogin").onclick = () => {
    let email = document.getElementById("email").value;
    let pwd = document.getElementById("pwd").value;

    if(!email || !pwd){
        alert("모든 칸을 입력하시오.");
        return;
    }

    fetch("http://127.0.0.1:4444/authenticate", {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            "email":email,
            "pwd":pwd
        })
    }).then((rsp) => {
        if(rsp.ok){
            rsp.json().then((json) => {
                sessionStorage.setItem('name', json['name']);
                sessionStorage.setItem('jwt', json['jwt']);
                location.href = 'main.html';
            });
        }
        else{
            rsp.text().then((txt) => {
                alert(txt);
            });
        }
    });
};