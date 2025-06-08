document.addEventListener('DOMContentLoaded', () => {
  // Use a generic selector to get the TOTAL_FORMS input regardless of prefix
  const totalForms = document.querySelector('input[name$="TOTAL_FORMS"]');
  const formsContainer = document.querySelector('[data-ingredient-forms]');
  const emptyFormDiv = document.getElementById('empty-form');

  if (!totalForms) {
    console.error('Could not find TOTAL_FORMS input. Check your formset prefix and management form.');
    return;
  }
  if (!formsContainer) {
    console.error('Could not find container for ingredient forms ([data-ingredient-forms] attribute).');
    return;
  }
  if (!emptyFormDiv) {
    console.error('Could not find empty form template with ID "empty-form".');
    return;
  }

  console.log('TOTAL_FORMS element found:', totalForms);
  console.log('Forms container found:', formsContainer);
  console.log('Empty form template found:', emptyFormDiv);

  const addBtn = document.getElementById('add-ingredient');
  if (!addBtn) {
    console.error('Could not find Add Ingredient button with ID "add-ingredient".');
    return;
  }
  console.log('Add Ingredient button found:', addBtn);

  // Update __prefix__ in the cloned form HTML to the current form index
  function updateFormIndex(html, index) {
    const updatedHtml = html.replace(/__prefix__/g, index);
    console.log(`Updated form HTML with index ${index}`);
    return updatedHtml;
  }

  // Attach click listeners to all remove buttons (.remove-btn)
  function attachRemoveListeners() {
    const removeBtns = document.querySelectorAll('.remove-btn');
    removeBtns.forEach(btn => {
      btn.removeEventListener('click', handleRemove); // remove old listeners first
      btn.addEventListener('click', handleRemove);
    });
    console.log(`Attached remove listeners to ${removeBtns.length} buttons.`);
  }

  // Remove ingredient form handler
  function handleRemove(event) {
    event.preventDefault();
    const formDiv = event.target.closest('div.flex.flex-col');
    if (!formDiv) {
      console.warn('Could not find ingredient form container to remove.');
      return;
    }

    const deleteCheckbox = formDiv.querySelector('input[type="checkbox"]');
    if (deleteCheckbox) {
      deleteCheckbox.checked = true; // mark for deletion
      formDiv.style.display = 'none'; // hide the form visually
      console.log('Ingredient form marked for deletion and hidden.');
    } else {
      // No checkbox? Just remove from DOM
      formDiv.remove();
      console.log('Ingredient form removed from DOM (no delete checkbox found).');
    }
  }

  // Add new ingredient form on button click
  addBtn.addEventListener('click', () => {
    const currentIndex = parseInt(totalForms.value);
    console.log('Current TOTAL_FORMS value:', currentIndex);

    const newFormHtml = updateFormIndex(emptyFormDiv.innerHTML, currentIndex);

    const wrapper = document.createElement('div');
    wrapper.innerHTML = newFormHtml.trim(); // trim to avoid whitespace nodes
    const newFormElement = wrapper.firstElementChild;

    if (!newFormElement) {
      console.error('Failed to create new form element from empty form HTML.');
      return;
    }

    formsContainer.appendChild(newFormElement);
    totalForms.value = currentIndex + 1;
    console.log('Added new ingredient form. Updated TOTAL_FORMS to', totalForms.value);

    attachRemoveListeners(); // attach listeners to new remove button
  });

  // Initialize existing remove buttons on page load
  attachRemoveListeners();
});
