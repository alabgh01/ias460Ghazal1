/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
/* jshint jquery: true */
'use strict';

console.log("js working");

const BASE_URL = "http://ghazalal.pythonanywhere.com/api/psgn1/";

function passPhraseSep(){
    // if pasphrase is chosen, display, seperator choices
    let pf = document.querySelector("#pf");
    let spDiv = document.querySelector("#spDiv");
    if(pf.checked){
        if(spDiv.innerHTML === ''){
            let lbl = document.createElement("label");
            lbl.setAttribute("class","form-check-label m-3");
            lbl.setAttribute("for", "spChoice");
            lbl.innerHTML = "Please choose a Seperator";
            spDiv.appendChild(lbl);
            let slct = document.createElement("select");
            slct.setAttribute("class", "form-select m-3");
            slct.setAttribute("id", "sprtr");
            let symbols = ["*", "-", "_", "$", "."];
            for (let s of symbols){
                let op = document.createElement("option");
                op.setAttribute("vlaue", `${s}`);
                op.innerHTML = `${s}`;
                slct.appendChild(op);
            }
            spDiv.appendChild(slct);
        }
    }
}

function nopf(){
    // if pw chosen after choosing pf
    let spDiv = document.querySelector("#spDiv");
    if(spDiv.innerHTML != ''){
        spDiv.innerHTML = '';
    }
}

function printPasswords(passes){
    //display passwords
    //will be called in requestPasswords
    let passDiv = document.querySelector("#pass-div");
    passDiv.innerHTML = "";
    let tbl = document.createElement("table");
    tbl.setAttribute("class", "table mt-3");
    let thd = document.createElement("thead");
    let th1 = document.createElement("th");
    th1.innerHTML = "Results";
    let th2 = document.createElement("th");
    th2.innerHTML = "Strengths";
    thd.appendChild(th1);
    thd.appendChild(th2);
    tbl.appendChild(thd);
    let tbod = document.createElement("tbody");
    for (let [k, v] of Object.entries(passes)){
        let tr = document.createElement("tr");
        let td1 = document.createElement("td");
        td1.innerHTML = k;
        let td2 = document.createElement("td");
        if(v >= 100){
            td2.innerHTML = "Very Strong";
            tr.setAttribute("class", "text-success");
        }else if (v >= 80 && v < 100){
            td2.innerHTML = "Strong";
            tr.setAttribute("class", "text-success");
        }else if (v >= 60 && v < 80){
            td2.innerHTML = "Weak";
            tr.setAttribute("class", "text-warning");
        }else if (v >= 40 && v < 60){
            td2.innerHTML = "Very Weak";
            tr.setAttribute("class", "text-warning");
        }else if (v < 40){
            td2.innerHTML = "Avoid";
            tr.setAttribute("class", "text-danger");
        }
        tr.appendChild(td1);
        tr.appendChild(td2);
        tbod.appendChild(tr);
        tbl.appendChild(tr);
    }
    passDiv.appendChild(tbl);
}

async function requestPasswords(){
    //get passwords from api
    let contains = document.querySelector("#contains").value;
    let ln = document.querySelector("#len").value;
    let num = document.querySelector("#num").value;
    let pw = document.querySelector("#pw");
    let pf = document.querySelector("#pf");
    if (contains && ln && num){
        if (pw.checked){
            return await fetch(`${BASE_URL}/${contains}/${ln}/${num}`)
            .then(response => response.json())
            .then(json => printPasswords(json))
            .catch(error => console.log(error));
        }else if (pf.checked){
            let sprtr = document.querySelector("#sprtr").value;
            return await fetch(`${BASE_URL}/psphrs/${sprtr}/${ln}/${num}`)
            .then(response => response.json())
            .then(json => printPasswords(json))
            .catch(error => console.log(error));
        }else{
            let mn = document.querySelector("#pass-div");
            let alrt = document.createElement("div");
            alrt.setAttribute("class", "alert alert-danger m-3");
            alrt.setAttribute("role", "alert");
            alrt.innerHTML = "Please choose a password or a passphrase.";
            mn.appendChild(alrt);
        }
    }else{
        let mn = document.querySelector("#pass-div");
        let alrt = document.createElement("div");
        alrt.setAttribute("class", "alert alert-danger m-3");
        alrt.setAttribute("role", "alert");
        alrt.innerHTML = "Some information is missing, please make sure to fill out all the fields in the form.";
        mn.appendChild(alrt);
    }
}
