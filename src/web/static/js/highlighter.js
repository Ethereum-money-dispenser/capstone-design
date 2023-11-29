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
        case 'Cards':
            sidebar_list[3].classList.add('active');
            break;
        case 'Admin':
            sidebar_list[4].classList.add('active');
            sidebar_list[4].querySelectorAll('a.collapse-item')[0].innerHTML = "<b>Admin<b/>";
            break;
        case 'Users receiving':
            sidebar_list[4].classList.add('active');
            sidebar_list[4].querySelectorAll('a.collapse-item')[1].innerHTML = "<b>Users receiving<b/>";
            break;
        case 'Users sending':
            sidebar_list[4].classList.add('active');
            sidebar_list[4].querySelectorAll('a.collapse-item')[2].innerHTML = "<b>Users sending<b/>";
            break;
        default:
            break;
    }
}

highlightSidebar();