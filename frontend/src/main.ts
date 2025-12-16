const myButton = document.getElementById("test");
const player_name = document.getElementsByClassName("player_name");
const fpts = document.getElementsByClassName("fpts/min");
const resultDiv = document.getElementById("result");

myButton?.addEventListener("click", async () => {
    try {
        alert("test");
        const response = await fetch(`/pull`);
        const data = await response.json();
        if (!resultDiv) return;
        resultDiv.innerHTML = "";
        if (data.error) {
            alert(data.error);
        } else {
            for (let i = 0; i < data.length; i++) {
                resultDiv.innerHTML += `
                    <div class="grid-container">
                        <div class="grid-name">
                            <p id="name">${data[i]["name"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">Average FPTS/MIN</p>
                            <p class="data">${data[i]["avg_fpts/min"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">PTS</p>
                            <p class="data">${data[i]["points"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">REB</p>
                            <p class="data">${data[i]["rebounds"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">AST</p>
                            <p class="data">${data[i]["assists"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">STL</p>
                            <p class="data">${data[i]["steals"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">BLK</p>
                            <p class="data">${data[i]["blocks"]}</p>
                        </div>
                        <div class="grid-item">
                            <p class="data-label">TO</p>
                            <p class="data">${data[i]["turnovers"]}</p>
                        </div>
                    </div>
                `;
            }
            document.querySelectorAll(".grid-container").forEach((item, i) => {
                item.addEventListener("click", () => {
                    window.location.href = `/player/${data[i].id}`;
                });
            });
        }
    } catch (error) {
        alert(error);
    }
});
