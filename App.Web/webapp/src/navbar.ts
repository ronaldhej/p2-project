const views:string[] = [
    "home",
    "scenario designer",
    "browse",
    "about",
    "contact"
]
const textValues:string[] = [
    "home",
    "scenario designer",
    "browse",
    "about",
    "contact"
]

export default function navbar() {
    return (`
    <div class="navbar" id="navbar">
    </div>
    `)
}

export function setupNavbar() {
    const navbar = document.getElementById("navbar");
    if (navbar === null) return
    for (let i in views) {
        const link = document.createElement("button");
        const span = document.createElement("span");
        link.innerText = textValues[i];
        navbar?.appendChild(link);
        link.appendChild(span);

        link.addEventListener('click', e => {
            console.log(e.target, views[i]);
            const clicked = e.target;

            for (let btn of navbar.children) {
                btn.classList.remove("active-link");
                if (clicked) clicked.classList.add("active-link");
            }
        });
    }
}