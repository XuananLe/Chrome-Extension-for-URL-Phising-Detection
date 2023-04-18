function get_url() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var url = tabs[0].url;
    var matches = url.match(/^https?\:\/\/([^\/?#]+)(?:[\/?#]|$)/i);
    var domain = matches && matches[1];
    document.getElementById("site-name").innerHTML = domain;
  });
}
get_url();
let phishingPercent = document.getElementById("phishing-percent");
let result = document.getElementById("result");
let link = "";

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  document.getElementById("site-name").innerHTML = message.Link;
  link = message.Link;
  console.log("the link is " + link);
});



chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  document.getElementById("site-name").innerHTML = message.Link;
  link = message.Link;
  console.log("the link is " + link);
  fetch("http://127.0.0.1:5000", {
    method: "POST",
    body: JSON.stringify({ url: link }),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Network response was not ok.");
      }
    })
    .then((data) => {
      
      console.log(data.prediction);
    })
    .catch((error) => {
      let result = document.querySelector("#result");
      result.textContent = "Something went wrong, please try again later";
      console.error("Error fetching prediction:", error);
    });
});
