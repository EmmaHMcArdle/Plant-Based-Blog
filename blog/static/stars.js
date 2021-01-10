let stars = document.querySelector(".Stars");
let percent_star = 0
stars.setAttribute('data-before', "☆☆☆☆☆")

// stars.addEventListener("click", function (event) {
//     let percent_star = round((event.offsetX / 310) * 100);
//     console.log(percent_star + "%")
//     stars.style.setProperty('--percent', percent_star + "%");
// })

stars.addEventListener("click", function (event) {
    console.log(event.offsetX);
    if (event.offsetX < 66) {
        stars.setAttribute('data-before', "★☆☆☆☆");
    } else if (event.offsetX < 131) {
        stars.setAttribute('data-before', "★★☆☆☆");
    } else if (event.offsetX < 193) {
        stars.setAttribute('data-before', "★★★☆☆");
    } else if (event.offsetX < 255) {
        stars.setAttribute('data-before', "★★★★☆");
    } else {
        stars.setAttribute('data-before', "★★★★★");
    }
    // 66, 131, 193, 255, else


    
})


