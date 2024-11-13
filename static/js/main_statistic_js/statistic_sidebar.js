function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.querySelector(".toggle-btn");

    sidebar.classList.toggle("collapsed");

    // Міняємо напрям стрілки в залежності від стану панелі
    if (sidebar.classList.contains("collapsed")) {
        toggleButton.innerHTML = "⟫"; // Панель схована
    } else {
        toggleButton.innerHTML = "⟪"; // Панель відкрита
    }
}

function setInitialSidebarState() {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.querySelector(".toggle-btn");

    if (sidebar.classList.contains("collapsed")) {
        toggleButton.innerHTML = "⟫";
    }
}
document.addEventListener("DOMContentLoaded", setInitialSidebarState);


