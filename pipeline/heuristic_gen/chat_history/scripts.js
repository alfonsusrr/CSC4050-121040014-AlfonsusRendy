document.addEventListener('DOMContentLoaded', async () => {
    const file = "http://localhost:9000/dbench-gpt4.json";
    const container = document.getElementById('json-content');
  
    // Function to fetch and parse JSON data
    async function fetchJSON(file) {
      try {
        const response = await fetch(file);
        return response.ok ? await response.json() : [];
      } catch (error) {
        console.error('Error fetching JSON:', error);
        return [];
      }
    }
  
    // Fetch all JSON files and merge their content
    const data = await fetchJSON(file);
    console.log(data)
  
    // Render each item inside Bootstrap cards
    data.forEach(item => {
      const card = document.createElement('div');
      card.className = 'col-md-4 mb-4';
      card.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">ID: ${item.id}</h5>
            <p class="card-text">Name: ${item.name}</p>
            <p class="card-text">Email: ${item.email}</p>
          </div>
        </div>
      `;
      container.appendChild(card);
    });
  });
  