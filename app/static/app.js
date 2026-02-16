const API = "/api/v1/recipes";

function splitInput(value) {
    return value.split(",").map(v => v.trim()).filter(v => v);
}
function formatDate(dateStr) {
    const date = new Date(dateStr + "Z");
    return date.toLocaleString();
}


async function createRecipe() {

    const data = {
        title: document.getElementById("title").value,
        ingredients: splitInput(document.getElementById("ingredients").value),
        steps: splitInput(document.getElementById("steps").value),
        tags: splitInput(document.getElementById("tags").value)
    };

    const res = await fetch(API + "/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        loadRecipes();
    } else {
        alert("Ошибка создания");
    }
}

async function loadRecipes() {

    const search = document.getElementById("filterSearch").value.trim();
    const url = API + "/" + (search ? "?q=" + encodeURIComponent(search) : "");

    const res = await fetch(url);
    const recipes = await res.json();

    const container = document.getElementById("recipes");
    container.innerHTML = "";

    recipes.forEach(r => {
        const div = document.createElement("div");
        div.className = "recipe";

        div.innerHTML = `
            <h3>${r.title}</h3>
            <b>Время создания:</b> ${formatDate(r.created_at)}</small><br><br>
            <b>Ингредиенты:</b> ${r.ingredients.join(", ")}<br>
            <b>Шаги:</b> ${r.steps.join(" → ")}<br>
            <b>Теги:</b> ${(r.tags || []).join(", ")}
            
        `;

        container.appendChild(div);
    });
}

loadRecipes();
