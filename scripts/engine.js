// título provisório


// function to move page apon button click
// IMPORTANT: give class "js-move-page-button" to every button that moves a page
// and assign what page to move to with data-page
document.addEventListener("click", function(event) {
  if (event.target.matches(".js-move-page-button")) {
    console.log('teste1');
    const targetPage = event.target.getAttribute("data-page"); // Get the page from data-page
    window.location.href = targetPage; // Redirect to that page
  }
});


