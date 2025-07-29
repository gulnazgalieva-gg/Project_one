document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы
    const modal = document.getElementById("myModal");
    const btn = document.getElementById("openModalBtn");
    const span = document.querySelector(".close");

    // Открываем модальное окно при клике на кнопку
    btn.addEventListener('click', function() {
        modal.style.display = "block";
    });

    // Закрываем модальное окно при клике на крестик
    span.addEventListener('click', function() {
        modal.style.display = "none";
    });

    // Закрываем модальное окно при клике вне его области
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});