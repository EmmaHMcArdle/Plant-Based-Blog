// let percent_star = 0;
let star1 = document.getElementById("stars-0");
let star2 = document.getElementById("stars-1");
let star3 = document.getElementById("stars-2");
let star4 = document.getElementById("stars-3");
let star5 = document.getElementById("stars-4");
// stars.addEventListener("click", function (event) {
//     let percent_star = round((event.offsetX / 310) * 100);
//     console.log(percent_star + "%")
//     stars.style.setProperty('--percent', percent_star + "%");
// })
makeStars();
// updateStars(3);

function makeStars() {
    for (let i = 1; i <= 5; i++)
    {
        console.log(i);
        document.getElementById("s" + i).innerHTML = "☆";
    }
}

function updateStars(amount) {
    for (let i = 1; i <= amount; i++)
    {
        console.log(i);
        document.getElementById("s" + i).innerHTML = "★";
    }
}


s1.addEventListener("click", function () {
    makeStars();
    updateStars(1);
})
s2.addEventListener("click", function () {
    makeStars();
    updateStars(2);
})
s3.addEventListener("click", function () {
    makeStars();
    updateStars(3);
})
s4.addEventListener("click", function () {
    makeStars();
    updateStars(4);
})
s5.addEventListener("click", function () {
    makeStars();
    updateStars(5);
})

function submitForm() {
    let rating = document.getElementById("s1");
    rating.submit();
}
window.onload = submitForm;

