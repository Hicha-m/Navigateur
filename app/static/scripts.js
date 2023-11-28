function white(){
    document.body.className = '';
    btn.textContent = 'NUIT';
    btn.setAttribute('onclick','dark()');
}
function dark(){
    document.body.className = 'dark';
    btn.textContent = 'JOUR';
    btn.setAttribute('onclick','white()');
}

let btn = document.querySelector(".btn");