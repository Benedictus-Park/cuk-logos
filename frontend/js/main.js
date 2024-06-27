document.getElementById("username").innerHTML = sessionStorage.getItem("name");

document.getElementById("btnCheckDutyTable").addEventListener('click', () => { location.href = "duty.html"; });
document.getElementById("btnMembers").addEventListener('click', () => { location.href = "members.html"; });
document.getElementById("btnIssueAccount").addEventListener('click', () => { location.href = "issue-account.html"; });
document.getElementById("btnScoreTable").addEventListener('click', () => { location.href = "scoretable.html"; });
document.getElementById("btnExportReport");
document.getElementById("btnSuicide").addEventListener('click', () => { location.href = "withdraw.html"; });