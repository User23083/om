document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
    var element = document.getElementById("elementToDisplay");
  	element.style.display = "block";
	   var element1 = document.getElementById("elementToHide");
  	element1.setAttribute("class", "d-none");
  }, 1000); // Delay in milliseconds (1 second in this case)
});

