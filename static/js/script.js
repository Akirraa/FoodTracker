document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("input[name='q']");
    const suggestionBox = createSuggestionBox();
  
    input.parentNode.appendChild(suggestionBox);
  
    input.addEventListener("input", () =>
      handleSearchInput(input.value, suggestionBox)
    );
  
    document.addEventListener("click", (e) => {
      if (!input.contains(e.target) && !suggestionBox.contains(e.target)) {
        clearSuggestions(suggestionBox);
        suggestionBox.classList.add("hidden");
      }
    });
  });
  
  // Create the suggestion dropdown
  function createSuggestionBox() {
    const box = document.createElement("ul");
    box.className = `
      absolute left-1/2 top-10 mt-2
      w-72 -translate-x-1/2
      rounded-xl shadow z-20
      bg-white/20 backdrop-blur-sm text-black
      max-h-36 overflow-y-auto scrollbar-none
      border border-white/20
      hidden
    `;
    return box;
  }
  
  // Handle input logic
  function handleSearchInput(query, suggestionBox) {
    if (query.length < 2) {
      clearSuggestions(suggestionBox);
      suggestionBox.classList.add("hidden");
      return;
    }
  
    fetchSuggestions(query).then((results) => {
      renderSuggestions(results, suggestionBox);
      if (results.length > 0) {
        suggestionBox.classList.remove("hidden");
      } else {
        suggestionBox.classList.add("hidden");
      }
    });
  }
  
  // Fetch data from your API view
  function fetchSuggestions(query) {
    return fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
      .then((response) => response.json())
      .then((data) => data.results || []);
  }
  
  // Render the dropdown results
  function renderSuggestions(results, suggestionBox) {
    clearSuggestions(suggestionBox);
  
    results.forEach((item) => {
      const li = document.createElement("li");
      li.className = "px-4 py-2 hover:bg-gray-400 cursor-pointer rounded-xl overflow-y-auto";
      li.textContent = `${item.name} (${item.type})`;
      li.addEventListener("click", () => {
        window.location.href = item.url;
      });
      suggestionBox.appendChild(li);
    });
  }
  
  // Clear all dropdown suggestions
  function clearSuggestions(suggestionBox) {
    suggestionBox.innerHTML = "";
  }
  