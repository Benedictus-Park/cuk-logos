if(!sessionStorage.getItem('is_king')){
    alert("잘못된 접근입니다.");
    location.href = "index.html";
}

document.getElementById("username").innerHTML = sessionStorage.getItem("name") + ((Boolean(sessionStorage.getItem("is_king"))) ? " 단장" : " 부단장");

let btnCheckDutyTable = document.getElementById("btnCheckDutyTable");
let btnRegisterMembers = document.getElementById("btnRegisterMembers");
let btnIssueAccount = document.getElementById("btnIssueAccount");
let btnScoreTable = document.getElementById("btnScoreTable");
let btnExportReport = document.getElementById("btnExportReport");
let btnSuicide = document.getElementById("btnSuicide");
