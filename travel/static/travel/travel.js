   
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#mobile-menu').onclick = toggleMobileMenu;
    document.querySelector('#navbarDropdownMobile').onclick = toggleMobileDropDownMenu;
    document.querySelector('#navbarDropdown').onclick = toggleDropDownMenu;
    window.onscroll = scrollFunction;
    document.querySelector('#jumpToTop').onclick = topFunction;
});

function toggleMobileMenu() {
    const menu = document.querySelector('#menu')
    if (menu.style.display.trim() === 'block') {
        menu.style.display = 'none';
        document.querySelector('#mobile-menu').innerHTML = 'Menu'
    } else {
        menu.style.display = 'block';
        document.querySelector('#mobile-menu').innerHTML = 'X'
    }
}

function toggleDropDownMenu() {
    const menu = document.querySelector('#dropdownMenu')
    if (menu.style.display.trim() != 'block') {
        menu.style.display = 'block';
        document.querySelector('.content').onmouseover = function(){
            menu.style.display = 'none';
        }
    } else {
        menu.style.display = 'none';
    }
}

function toggleMobileDropDownMenu() {
    const menu = document.querySelector('#dropdownMenuMobile')
    if (menu.style.display.trim() != 'block') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

//from W3 Schools
function scrollFunction() {
    let jumpBtn = document.querySelector('#jumpToTop');
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
      jumpBtn.style.display = "block";
    } else {
      jumpBtn.style.display = "none";
    }
  }
  
  //from w3 schools
  // When the user clicks on the button, scroll to the top of the document
  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }