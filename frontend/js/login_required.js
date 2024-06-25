if(!sessionStorage.getItem('jwt')){
    alert("잘못된 접근입니다.");
    location.href = "index.html";
}