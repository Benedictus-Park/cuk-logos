let name_element = document.getElementById("name");
let btnSubmit = document.getElementById("btnSubmit");

name_element.addEventListener('keydown', (e) => {
    if(e.key == "Enter" && name_element.value){
        btnSubmit.click();
    }
});

btnSubmit.addEventListener('click', () => {
    if(!name_element.value){
        alert("입력은 하고 누르셔야죠...");
        return;
    }
    else{
        if(confirm("가입예정자 이름: " + name_element.value + "\n정말 맞아요?")){
            fetch("http://127.0.0.1:4444/issue-authcode", {
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization":sessionStorage.getItem("jwt")
                },
                body:JSON.stringify({
                    "name":name_element.value
                })
            }).then((rsp) => {
                if(rsp.ok){
                    rsp.json().then((obj) => {
                        document.getElementById("issued_name").setAttribute("value", obj['name']);
                        document.getElementById("issued_code").setAttribute("value", obj['authcode']);
                        sessionStorage.setItem('jwt', obj['jwt']);
                    });
                    alert("성공, 하단 확인.");
                }
                else{
                    rsp.text().then((txt) => {
                        alert(txt);
                    });
                }
            });
        }
        else{
            return;
        }
    }
});