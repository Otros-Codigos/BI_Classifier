/*!
 * Start Bootstrap - Creative v7.0.6 (https://startbootstrap.com/theme/creative)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
 */
//
// Scripts
//

window.addEventListener("DOMContentLoaded", (event) => {
  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector("#mainNav");
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove("navbar-shrink");
    } else {
      navbarCollapsible.classList.add("navbar-shrink");
    }
  };

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener("scroll", navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector("#mainNav");
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: "#mainNav",
      offset: 74,
    });
  }

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector(".navbar-toggler");
  const responsiveNavItems = [].slice.call(
    document.querySelectorAll("#navbarResponsive .nav-link")
  );
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener("click", () => {
      if (window.getComputedStyle(navbarToggler).display !== "none") {
        navbarToggler.click();
      }
    });
  });

  // Activate SimpleLightbox plugin for portfolio items
  new SimpleLightbox({
    elements: "#portfolio a.portfolio-box",
  });
});

// ------------------------------------------------------------------------------------------

function remove_data() {
  const menu = document.getElementById("masterhead");
  menu.remove();
}

let data = [];
url = "/data";

function get_Data(callback) {
  fetch(url)
    .then((res) => res.json())
    .then((res) => {
      callback(res);
    });
}

function charge_data(id) {
  get_Data((value) => {
    remove_data();

    const father = document.getElementById("root");

    let master = document.createElement("div");
    master.className = "masterhead";
    master.id = "masterhead";

    let cloud = document.createElement("ul");
    cloud.className = "cloud";
    cloud.role = "navigation";

    father.appendChild(master);

    let title = document.createElement("h1");
    title.innerHTML = "CLOUD WORD";
    title.className = "cName";
    master.appendChild(title);

    let row = document.createElement("div");
    row.className = "row";
    master.append(row);

    let b1 = document.createElement("div");
    b1.className = "col-1";
    row.appendChild(b1);

    let b2 = document.createElement("div");
    b2.className = "col-10";
    row.appendChild(b2);
    b2.appendChild(cloud);

    let b3 = document.createElement("div");
    b3.className = "col-1";
    row.appendChild(b3);

    data = eval(value);

    for (let i = 0; i < data.length; i++) {
      let diag = data[i].Diagnose;
      let word = data[i].Word;
      let occur = data[i].Occurrences;

      if (diag === id && occur > 8) {
        let li = document.createElement("li");
        let a = document.createElement("a");

        cloud.appendChild(li);
        li.append(a);
        a.innerHTML = word;
        a.className = "w" + occur;
      }
    }
  });
}
