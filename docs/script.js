const main = document.getElementById("libraries");

fetch("libraries.json")
  .then(res => res.json())
  .then(data => {
    data.forEach(lib => {
      const div = document.createElement("div");
      div.className = "library";
      div.innerHTML = `
        <h2>${lib.name}</h2>
        <p>${lib.description}</p>
        <p>Authors: ${lib.authors}</p>
        <a href="${lib.addToLib}" target="_blank"><button>Add to Excalidraw ➡️</button></a>
        <a href="${lib.source}" target="_blank"><button>Source ↓</button></a>
      `;
      main.appendChild(div);
    });
  });
