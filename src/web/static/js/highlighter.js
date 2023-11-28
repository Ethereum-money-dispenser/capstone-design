function highlightSidebar() {
    const sidebar_list = document.querySelectorAll('li.nav-item');
    const title_name = document.querySelector('h1.h3').textContent;

    switch (title_name) {
        case 'Dashboard':
            sidebar_list[0].classList.add('active');
            break;
        case 'Charts':
            sidebar_list[1].classList.add('active');
            break;
        case 'Tables':
            sidebar_list[2].classList.add('active');
            break;
        case 'Admin':
            sidebar_list[3].classList.add('active');
            sidebar_list[3].querySelectorAll('a.collapse-item')[0].innerHTML = "<b>admin<b/>";
            break;
        case 'Cards':
            sidebar_list[3].classList.add('active');
            sidebar_list[3].querySelectorAll('a.collapse-item')[1].innerHTML = "<b>cards<b/>";
            break;
        default:
            break;
    }
}

highlightSidebar();