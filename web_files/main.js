
const initialize = () => {
    setTimeout(updateProgress, 0)
}

function updateProgress() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        progress = JSON.parse(this.responseText)['progress']
        if (progress == "DONE") {
          p = document.querySelector("#finished-memo");
          p.style.visibility = 'visible';
          progressbar = document.querySelector('#myprogressBar');
          progressbar.style.width = "100%";
        }
        else {
          progressbar = document.querySelector('#myprogressBar');
          progressbar.style.width = progress + "%";
        }
      }
    };
    xhttp.open("GET", "/progress", true);
    xhttp.send();
    setTimeout(updateProgress, 1000)
  }

document.addEventListener('DOMContentLoaded', initialize);