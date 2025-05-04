let allFoods = [];
let selectedFoods = [];
let pieChart = null;
let barChart = null;
  

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

function addFood() {
  const input = document.getElementById('search');
  const name = input.value.trim();
  if (!name) return;

  const food = allFoods.find(f => f.name.toLowerCase() === name.toLowerCase());
  if (!food) {
    alert("Food not found.");
    return;
  }

  // Check if the food is already added
  const existingFoodIndex = selectedFoods.findIndex(f => f.name.toLowerCase() === food.name.toLowerCase());
  if (existingFoodIndex !== -1) {
    alert("Food is already added.");
    return;
  }

  // Add food with default multiplier of 1
  selectedFoods.push({ ...food, multiplier: 1 });
  updateTable();
  updateNutrientPieChart();  // Update the pie chart for nutrient breakdown
  updateChart();  // Update the overall nutrient chart (bar chart)
  generateNutritionTip();  // Generate nutrition tip based on updated foods
  input.value = '';
}

function updateTable() {
  const tbody = document.getElementById('intake-table-body');
  tbody.innerHTML = '';
  let totalCalories = 0; // Add this variable to accumulate calories
  selectedFoods.forEach((food, index) => {
    totalCalories += food.calories * food.multiplier; // Sum up calories
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

  // Update the total calories progress
  document.getElementById('totalCalories').innerText = totalCalories.toFixed(1);
  const maxCalories = 2500; // Set the max calories goal (example)
  const progress = (totalCalories / maxCalories) * 100;
  document.getElementById('caloriesProgress').style.width = `${progress}%`;
}

function updateMultiplier(index, newValue) {
  const val = parseFloat(newValue);
  selectedFoods[index].multiplier = isNaN(val) || val < 0 ? 1 : val;
  updateTable();
  updateNutrientPieChart();  // Update the pie chart after multiplier change
  updateChart();  // Update the overall nutrient chart (bar chart)
  generateNutritionTip();  // Generate a new nutrition tip after multiplier change
}

function updateNutrientPieChart() {
  const totals = { protein: 0, carbs: 0, fats: 0 };

  selectedFoods.forEach(f => {
    totals.protein += f.protein * f.multiplier;
    totals.carbs += f.carbs * f.multiplier;
    totals.fats += f.fats * f.multiplier;
  });

  // Set up the pie chart
  const ctx = document.getElementById('progressChart').getContext('2d');
  if (pieChart) pieChart.destroy();  // Destroy the existing pie chart if it exists
  pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Protein', 'Carbs', 'Fats'],
      datasets: [{
        data: [totals.protein, totals.carbs, totals.fats],
        backgroundColor: ['#3b82f6', '#f59e0b', '#10b981'],  // Colors for each segment
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
    totals.Protein += f.protein * f.multiplier;
    totals.Carbs += f.carbs * f.multiplier;
    totals.Fats += f.fats * f.multiplier;
    totals.Fiber += f.fiber * f.multiplier;
    totals.Sugar += f.sugar * f.multiplier;
    totals.Water += f.water * f.multiplier;
    totals.Sodium += f.sodium * f.multiplier;
    totals.Calcium += f.calcium * f.multiplier;
    totals.Iron += f.iron * f.multiplier;
    totals.Potassium += f.potassium * f.multiplier;
    totals.Cholesterol += f.cholesterol * f.multiplier;
  });

  const nutrientColors = {
    Protein: '#3b82f6',
    Carbs: '#f59e0b',
    Fats: '#10b981',
    Fiber: '#a78bfa',
    Sugar: '#f472b6',
    Water: '#60a5fa',
    Sodium: '#f87171',
    Calcium: '#34d399',
    Iron: '#fb923c',
    Potassium: '#8b5cf6',
    Cholesterol: '#f43f5e'
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
  updateTable();
  updateNutrientPieChart();  // Update the pie chart after food removal
  updateChart();  // Update the overall nutrient chart (bar chart)
  
}



document.addEventListener('DOMContentLoaded', fetchFoods);
