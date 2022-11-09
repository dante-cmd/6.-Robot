var addItem = document.getElementById("add-item");
let ruc = document.getElementById("ruc");
let total = document.getElementById("total-id");

let out = document.getElementById("output");
let cat = document.getElementById("cat-test");

// Insert data

function insertData(data, callback) {
  // console.log(data);
  if (data["index"]) {
    if (data["index"] == "2") {
      cat.toggleAttribute("data-2");
    }
  } else {
    let row = document.createElement("tr");
    const data_keys = Object.keys(data);
    data_keys.forEach((object_name) => {
      let td = document.createElement("td");
      td.innerText = data[object_name];
      if (object_name == "amount") {
        td.setAttribute("data-amount", "amount");
        row.appendChild(td);
      }
      else if (object_name == "name_product") {
        td.className = "text-left"
        row.appendChild(td);
      }
      else if (object_name == "container") {
        td.className = "text-center"
        row.appendChild(td);
      }
       else {
        row.appendChild(td);
      }
    });
    out.appendChild(row);
  }
  callback();
}

// Post Data

function postData(result, url, callback) {
  // if ()
  const request = new Request(url, {
    method: "POST",
    body: JSON.stringify({ result: result }),
  });

  fetch(request)
    .then((response) => response.json())
    .then((data) => insertData(data, callback));
  
  
}

// Get Total
function getTotal() {

  const dataAmount = document.querySelectorAll("td[data-amount]");
  let dataList = [];
  dataAmount.forEach((el) => {
    dataList.push(Number(el.textContent));
  });
  total.innerText = `S/. ${dataList.reduce((a, b) => a + b)}`;
}

// Get Nothing

function getNothing(){
  console.log('l')
}

// Speech Recognition

// 1. Param

var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var SpeechGrammarList = SpeechGrammarList || window.webkitSpeechGrammarList;
var SpeechRecognitionEvent =
  SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

// 2. Instance

var recognition = new SpeechRecognition();

recognition.continuous = false;
recognition.lang = "es-ES";
recognition.interimResults = false;
recognition.maxAlternatives = 1;

addItem.addEventListener("click", () => {
  // ruc.style.backgroundColor = "red";
  recognition.start();
  console.log("Ready to receive a color command.");
});

recognition.onresult = function (event) {
  const result = event.results[0][0].transcript;

  if (!cat.hasAttribute("data-2")) {
    const url = "http://127.0.0.1:8000/";
    postData(result, url, getNothing);
  } else {
    const url = "http://127.0.0.1:8000/products";
    postData(result, url, getTotal);
  }
};

recognition.onspeechend = function () {
  recognition.stop();
};

// var diagnostic = document.querySelector('.output');

// recognition.onnomatch = function(event) {
//   diagnostic.textContent = "I didn't recognise that color.";
// }

// recognition.onerror = function(event) {
//   diagnostic.textContent = 'Error occurred in recognition: ' + event.error;
// }
