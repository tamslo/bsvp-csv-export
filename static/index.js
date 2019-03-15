function runExport(exporter) {
  const backendUrl = window.location.origin;
  const manufacturers = Array.from(
    document.getElementsByClassName("manufacturer-selection")
  )
    .filter(function(manufacturer) {
      return manufacturer.checked;
    })
    .map(function(manufacturer) {
      return manufacturer.getAttribute("data-name");
    });
  return fetch(`${backendUrl}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exporter, manufacturers })
  });
}

function toggleAllManufacturers() {
  let button = document.getElementById("toggle-manufacturers-button");
  const selectValue = "select-all";
  const deselectValue = "deselect-all";
  const select = button.getAttribute("value") === selectValue;

  Array.from(document.getElementsByClassName("manufacturer-selection")).forEach(
    function(checkbox) {
      checkbox.checked = select;
    }
  );

  const newButtonText = select ? "Alle abwählen" : "Alle auswählen";
  const newButtonValue = select ? deselectValue : selectValue;
  button.innerHTML = newButtonText;
  button.setAttribute("value", newButtonValue);
}
