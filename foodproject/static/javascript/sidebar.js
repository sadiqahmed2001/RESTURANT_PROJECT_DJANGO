
function openNav() {
    document.getElementById("myAsidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

 function closeNav() {
    document.getElementById("myAsidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";

}

// Add an event listener to close the sidebar when scrolling
window.addEventListener('scroll', function() {
    closeNav();
});
   