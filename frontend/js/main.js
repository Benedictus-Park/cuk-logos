document.getElementById("username").innerHTML = sessionStorage.getItem("name");

document.getElementById("btnCheckDutyTable");
document.getElementById("btnRegisterMembers");
document.getElementById("btnIssueAccount").addEventListener('click', () => { location.href = "issue-account.html"; });
document.getElementById("btnScoreTable");
document.getElementById("btnExportReport");
document.getElementById("btnSuicide").addEventListener('click', () => { location.href = "withdraw.html"; });