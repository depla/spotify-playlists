const form = document.querySelector("#prompt-form");
const spinner = document.getElementById("generator-load-spinner");
const button = document.querySelector(".generate-btn");
const login = document.getElementById("login");
const logout = document.getElementById("logout");

spinner.style.display = "none";

form.addEventListener("submit", function (e) {
    if (!form.checkValidity()) {
        e.preventDefault()
        e.stopPropagation()
        form.classList.add('was-validated')
        return false
    }
    e.preventDefault();
    button.disabled = true;
    spinner.style.display = "";
    console.log("in e listener");
    createPlayList();
})

login.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/login", {
        method: "POST"
    });
})

logout.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/logout", {
        method: "POST"
    });
})

function createPlayList() {
    const prompt = form.elements.prompt.value;
    const num_songs = form.elements.num_songs.value;

    fetch("/playlist", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            prompt: prompt,
            num_songs: num_songs
        })
    })
        .then((response) => {
            console.log(response)
            return response.json();
        })
        .then((data) => {
            console.log(data);
            button.disabled = false;
            spinner.style.display = "none";
        })
}