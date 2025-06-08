let allFoods = [];
let selectedFoods = [];
let pieChart = null;
let barChart = null;
const today = new Date().toISOString().split("T")[0];
function resetDailyStorage() {
  const today = new Date().toISOString().split('T')[0]; 
  const lastUpdated = localStorage.getItem('lastUpdated');

  if (lastUpdated !== today) {
    console.log("Resetting daily storage");
    localStorage.removeItem('selectedFoods');  // Clear specific key
    localStorage.clear(); // Clear all localStorage
    localStorage.setItem('lastUpdated', today);
  }
  else {
    console.log("Daily storage already reset today");
  }
}
resetDailyStorage();

async function fetchFoods() {
  try {
    const response = await fetch('/api/foods/');
    const data = await response.json();
    allFoods = data;

    const datalist = document.getElementById('food-suggestions');
    datalist.innerHTML = '';
    allFoods.forEach(food => {
      const option = document.createElement('option');
      option.value = food.name;
      datalist.appendChild(option);
    });
  } catch (error) {
    console.error("Failed to fetch foods:", error);
  }
}

function saveSelectedFoods() {
  localStorage.setItem('selectedFoods', JSON.stringify(selectedFoods));
}


function addFood() {
  const input = document.getElementById('search');
  const name = input.value.trim();
  if (!name) return;

  const food = allFoods.find(f => f.name.toLowerCase() === name.toLowerCase());
  if (!food) {
    alert("Food not found.");
    return;
  }

  if (selectedFoods.find(f => f.name.toLowerCase() === food.name.toLowerCase())) {
    alert("Food is already added.");
    return;
  }

  selectedFoods.push({ ...food, multiplier: 1 });
  saveSelectedFoods(); 
  updateTable();
  updateNutrientPieChart();
  updateChart();
  generateNutritionTip();
  input.value = '';
}

function updateTable() {
  const tbody = document.getElementById('intake-table-body');
  tbody.innerHTML = '';
  let totalCalories = 0;

  selectedFoods.forEach((food, index) => {
    totalCalories += food.calories * food.multiplier;
    //save or update the total calories in localStorage
    localStorage.setItem('totalCalories', totalCalories);
    const row = `
      <tr class="text-white">
        <td class="px-4 py-2">${food.name}</td>
        <td class="px-4 py-2">
          <input type="number" min="0" step="0.01" value="${food.multiplier}" 
            onchange="updateMultiplier(${index}, this.value)"
            class="w-16 bg-gray-800 border border-gray-600 text-white px-1 rounded">
        </td>
        <td class="px-4 py-2">${(food.calories * food.multiplier).toFixed(1)}</td>
        <td class="px-4 py-2">${(food.protein * food.multiplier).toFixed(1)}</td>
        <td class="px-4 py-2">${(food.carbs * food.multiplier).toFixed(1)}</td>
        <td class="px-4 py-2">${(food.fats * food.multiplier).toFixed(1)}</td>
        <td class="px-4 py-2">
          <button onclick="removeFood(${index})" class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded">Delete</button>
        </td>
      </tr>`;
    tbody.innerHTML += row;
  });

  document.getElementById('totalCalories').innerText = totalCalories.toFixed(1);
  const maxCalories = 2500;
  const progress = (totalCalories / maxCalories) * 100;
  document.getElementById('caloriesProgress').style.width = `${progress}%`;
}

function updateMultiplier(index, newValue) {
  const val = parseFloat(newValue);
  selectedFoods[index].multiplier = isNaN(val) || val < 0 ? 1 : val;
  saveSelectedFoods(); 
  updateTable();
  updateNutrientPieChart();
  updateChart();
  generateNutritionTip();
}

function updateNutrientPieChart() {
  const totals = { protein: 0, carbs: 0, fats: 0 };

  selectedFoods.forEach(f => {
    totals.protein += f.protein * f.multiplier;
    totals.carbs += f.carbs * f.multiplier;
    totals.fats += f.fats * f.multiplier;
  });

  const ctx = document.getElementById('progressChart').getContext('2d');
  if (pieChart) pieChart.destroy();
  pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Protein', 'Carbs', 'Fats'],
      datasets: [{
        data: [totals.protein, totals.carbs, totals.fats],
        backgroundColor: ['#3b82f6', '#f59e0b', '#10b981'],
        hoverOffset: 4,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { color: 'white' }
        },
        tooltip: {
          bodyColor: 'white',
          titleColor: 'white'
        }
      }
    }
  });
}

function updateChart() {
  const totals = {
    Protein: 0, Carbs: 0, Fats: 0, Fiber: 0, Sugar: 0,
    Water: 0, Sodium: 0, Calcium: 0, Iron: 0, Potassium: 0, Cholesterol: 0
  };

  selectedFoods.forEach(f => {
    for (let key in totals) {
      if (f[key.toLowerCase()] !== undefined) {
        totals[key] += f[key.toLowerCase()] * f.multiplier;
      }
    }
  });

  const nutrientColors = {
    Protein: '#3b82f6', Carbs: '#f59e0b', Fats: '#10b981',
    Fiber: '#a78bfa', Sugar: '#f472b6', Water: '#60a5fa',
    Sodium: '#f87171', Calcium: '#34d399', Iron: '#fb923c',
    Potassium: '#8b5cf6', Cholesterol: '#f43f5e'
  };

  const datasets = Object.keys(totals).map(nutrient => ({
    label: nutrient,
    data: [totals[nutrient]],
    backgroundColor: nutrientColors[nutrient],
    borderRadius: 5
  }));

  const ctx = document.getElementById('nutrientChart').getContext('2d');
  if (barChart) barChart.destroy();
  barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Total Nutrients'],
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { color: 'white' }
        },
        tooltip: {
          bodyColor: 'white',
          titleColor: 'white'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: 'white' }
        },
        x: {
          ticks: { color: 'white' }
        }
      }
    }
  });
}

function removeFood(index) {
  selectedFoods.splice(index, 1);
  saveSelectedFoods(); 
  updateTable();
  updateNutrientPieChart();
  updateChart();
  generateNutritionTip();
}

// CSRF token helper
function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue;
}

// Send food data to backend and display tip with better styling and more nutrients considered


function toggleTips() {
  const tipsContent = document.getElementById('tipsContent');
  const toggleIcon = document.getElementById('toggleIcon');

  if (!tipsContent || !toggleIcon) return; // Safety check

  if (tipsContent.classList.contains('max-h-0')) {
    tipsContent.classList.remove('max-h-0', 'overflow-hidden');
    tipsContent.classList.add('max-h-screen');
    toggleIcon.textContent = '−';
  } else {
    tipsContent.classList.remove('max-h-screen');
    tipsContent.classList.add('max-h-0', 'overflow-hidden');
    toggleIcon.textContent = '+';
  }
}

async function generateNutritionTip() {
  const tipContainer = document.getElementById('nutritionTip');
  const addBtn = document.getElementById('addFoodButton');

  tipContainer.innerHTML = `
    <div class="bg-white/10 p-4 rounded-lg shadow-md text-white text-sm font-semibold">
      Generating tips...
    </div>`;
  if (addBtn) addBtn.disabled = true;

  if (selectedFoods.length === 0) {
    tipContainer.innerHTML = `
      <div class="bg-gray-800 p-4 rounded-lg shadow-md text-white text-sm font-semibold">
        Add some foods to get tips!
      </div>`;
    if (addBtn) addBtn.disabled = false;
    return;
  }

  const totals = {
    calories: 0, protein: 0, carbs: 0, fats: 0,
    cholesterol: 0, sugar: 0, fiber: 0, water: 0,
    sodium: 0, calcium: 0, iron: 0, potassium: 0
  };

  selectedFoods.forEach(f => {
    totals.calories += (f.calories || 0) * f.multiplier;
    totals.protein += (f.protein || 0) * f.multiplier;
    totals.carbs += (f.carbs || 0) * f.multiplier;
    totals.fats += (f.fats || 0) * f.multiplier;
    totals.cholesterol += (f.cholesterol || 0) * f.multiplier;
    totals.sugar += (f.sugar || 0) * f.multiplier;
    totals.fiber += (f.fiber || 0) * f.multiplier;
    totals.water += (f.water || 0) * f.multiplier;
    totals.sodium += (f.sodium || 0) * f.multiplier;
    totals.calcium += (f.calcium || 0) * f.multiplier;
    totals.iron += (f.iron || 0) * f.multiplier;
    totals.potassium += (f.potassium || 0) * f.multiplier;
  });
  localStorage.setItem('nutritionTotals', JSON.stringify(totals));
  try {
    const response = await fetch('/api/generate-tip/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({ nutrition: totals })
    });

    if (!response.ok) throw new Error(`Tip generation failed: ${response.status}`);

    const data = await response.json();

    if (Array.isArray(data.tips)) {
      tipContainer.innerHTML = `
        <div class="bg-white/10 backdrop-blur-xl p-4 rounded-lg shadow-md text-white text-sm flex flex-col">
          <div class="flex justify-between items-center mb-2">
            <h4 class="text-lg font-semibold text-white">Nutrition Tips</h4>
            <button onclick="toggleTips()" class="text-white/70 hover:text-yellow-400 text-sm focus:outline-none">
              <span id="toggleIcon">−</span>
            </button>
          </div>
          <div id="tipsContent" class="transition-all duration-300 ease-in-out max-h-screen overflow-hidden">
            <ul class="list-disc list-inside space-y-2 pl-5 pr-2 text-white/90 leading-relaxed">
              ${data.tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
          </div>
        </div>`;
    } else {
      tipContainer.innerHTML = `
        <div class="bg-gray-800 p-4 rounded-lg shadow-md text-white text-sm font-semibold">
          No tips received.
        </div>`;
    }
  } catch (error) {
    console.error("Tip generation error:", error);
    tipContainer.innerHTML = `
      <div class="bg-gray-800 p-4 rounded-lg shadow-md text-white text-sm font-semibold">
        Failed to fetch tips.
      </div>`;
  } finally {
    if (addBtn) addBtn.disabled = false;
  }
}

function sendSelectedFoodsToServer() {
  const selectedFoods = JSON.parse(localStorage.getItem('selectedFoods') || '[]');
  const nutritionTotals = JSON.parse(localStorage.getItem('nutritionTotals') || '{}');

  fetch('/api/save-selected-foods/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()  // make sure CSRF token is sent if needed
    },
    body: JSON.stringify({ foods: selectedFoods, nutritionTotals: nutritionTotals })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Server response:', data);
  })
  .catch(error => {
    console.error('Error sending selected foods:', error);
  });
}
  document.addEventListener('DOMContentLoaded', function () {
    const syncButton = document.getElementById('syncButton');
    if (syncButton) {
      syncButton.addEventListener('click', sendSelectedFoodsToServer);
    }
  });


document.addEventListener('DOMContentLoaded', () => {
  fetchFoods();

  const storedFoods = localStorage.getItem('selectedFoods');
  if (storedFoods) {
    selectedFoods = JSON.parse(storedFoods);
    updateTable();
    updateNutrientPieChart();
    updateChart();
    generateNutritionTip();
  }
});
