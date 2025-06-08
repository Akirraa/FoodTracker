document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("recipe-container");
    const pagination = document.getElementById("pagination");
    let currentPage = 1;

    function fetchRecipes(page = 1) {
        fetch(`/api/recipes/?page=${page}`)
            .then(response => response.json())
            .then(data => {
                renderRecipes(data.results);
                renderPagination(data.count, page, Math.ceil(data.count / 6));
            })
            .catch(error => console.error("Error fetching recipes:", error));
    }

    function renderRecipes(recipes) {
        container.innerHTML = "";
        recipes.forEach(recipe => {
            const card = document.createElement("div");
            card.className = "bg-white text-black rounded overflow-hidden shadow-md flex flex-col items-center mx-auto";
            card.style.maxWidth = "300px";
            card.style.height = "400px";

            card.innerHTML = `
                <img src="${recipe.image_url}" alt="${recipe.title}" class="w-full h-40 object-cover">
                <div class="p-4 flex flex-col items-center text-center h-full w-full">
                    <h3 class="font-bold text-lg mb-2">${recipe.title}</h3>
                    <p class="text-sm text-gray-600 mb-4 flex-grow">${recipe.description.slice(0, 100)}...</p>
                    <div class="mt-auto">
                        <button class="bg-yellow-400 hover:bg-yellow-500 px-6 py-2 rounded text-black font-semibold">Add</button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    function renderPagination(totalItems, current, totalPages) {
        pagination.innerHTML = "";

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement("button");
            btn.className = `px-4 py-2 rounded ${i === current ? 'bg-yellow-400 text-black' : 'bg-gray-300 hover:bg-gray-400'}`;
            btn.textContent = i;
            btn.addEventListener("click", () => {
                currentPage = i;
                fetchRecipes(currentPage);
            });
            pagination.appendChild(btn);
        }
    }

    fetchRecipes(currentPage);
});
