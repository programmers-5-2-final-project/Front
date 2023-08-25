
    
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

searchInput.addEventListener("input", handleSearch);

function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredResults = data.filter(item =>
    item.name.toLowerCase().includes(searchTerm)
    );

    displayResults(filteredResults);
}

function displayResults(results) {
    searchResults.innerHTML = "";
    results.forEach(result => {
    const li = document.createElement("li");
    li.textContent = result.name;
    searchResults.appendChild(li);
    });
}
