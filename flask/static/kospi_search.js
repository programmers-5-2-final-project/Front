// search.js
const kospi_simbol_company_dict = {{ kospi_simbol_company_dict | tojson | safe }};
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

searchInput.addEventListener("input", handleSearch);

function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredResults = kospiData.filter(item =>
        item.name.toLowerCase().includes(searchTerm)
    );

    displayResults(filteredResults);
}

function displayResults(results) {
    searchResults.innerHTML = "";
    results.forEach(result => {
        const li = document.createElement("li");
        li.textContent = result.name;
        li.addEventListener("click", () => {
            // 선택한 목록의 상세 페이지로 이동
            window.location.href = `main/detail/${result.code}`;
        });
        searchResults.appendChild(li);
    });
}
