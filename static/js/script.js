// Smooth Scroll untuk anchor
document.querySelectorAll('a.nav-link').forEach(link => {
    link.addEventListener('click', function(e){
        if(this.hash !== ''){
            e.preventDefault();
            document.querySelector(this.hash).scrollIntoView({behavior:'smooth'});
        }
    });
});

// Alert fade out otomatis
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 1000);
    });
}, 3500);

// Hover effect tambahan untuk cards
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'scale(1.03)';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'scale(1)';
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // 1. Navbar auto-hide saat scroll
    let prevScrollpos = window.pageYOffset;
    const navbar = document.querySelector(".navbar");
    window.onscroll = function () {
        let currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            navbar.style.top = "0";
        } else {
            navbar.style.top = "-80px"; // sembunyikan
        }
        prevScrollpos = currentScrollPos;
    };

    // 2. Smooth scroll untuk link anchor
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
            });
        });
    });

    // 3. Card hover effect (zoom-in)
    const cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.classList.add("shadow-lg");
            card.style.transform = "scale(1.03)";
            card.style.transition = "all 0.3s ease-in-out";
        });
        card.addEventListener("mouseleave", () => {
            card.classList.remove("shadow-lg");
            card.style.transform = "scale(1)";
        });
    });

    // 4. Back to top button
    const backToTop = document.getElementById("backToTop");
    window.addEventListener("scroll", function () {
        if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
            backToTop.style.display = "block";
        } else {
            backToTop.style.display = "none";
        }
    });
    backToTop.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // 5. Auto-dismiss alert (Bootstrap)
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(alert => {
        setTimeout(() => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000); // auto close setelah 4 detik
    });

    // 6. Dark/Light Mode Toggle
    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");
            if (document.body.classList.contains("dark-mode")) {
                themeToggle.innerHTML = "☀️ Light Mode";
            } else {
                themeToggle.innerHTML = "🌙 Dark Mode";
            }
        });
    }
});

