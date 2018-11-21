setInterval (()=> {
    var date = Date();
    document.getElementById('time').innerHTML = date;
}, 999);

document.getElementById('menuIcon').addEventListener('click', ()=>{
    var x = document.getElementById('topNav');
    if(x.className === "responsiveNav"){
        x.className += " responsive";
    }else {
        x.className = "responsiveNav";
    }
});