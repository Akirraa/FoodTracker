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
  

  const navbar = document.getElementById("navbar");

  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.classList.remove("bg-transparent");
      navbar.classList.add("bg-black/80", "backdrop-blur");
    } else {
      navbar.classList.remove("bg-black/80", "backdrop-blur");
      navbar.classList.add("bg-transparent");
    }
  });

  // Function to handle password visibility toggle
  function togglePassword() {
    const input = document.getElementById('password-input');
    const icon = document.getElementById('eye-icon');

    const eye = `
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
    `;

    const eyeOff = `
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.269-2.943-9.543-7a10.05 10.05 0 013.111-4.481" />
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M6.618 6.618A9.964 9.964 0 0112 5c4.478 0 8.269 2.943 9.543 7a10.05 10.05 0 01-2.003 3.368M15 12a3 3 0 01-3 3m0-3a3 3 0 013-3m0 0L3 3" />
    `;

    if (input.type === 'password') {
      input.type = 'text';
      icon.innerHTML = eyeOff;
    } else {
      input.type = 'password';
      icon.innerHTML = eye;
    }
  }