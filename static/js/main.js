// const playerCard = document.getElementsByClassName("card")
const myButton = document.getElementById("test");
const player_name = document.getElementsByClassName("player_name");
const fpts = document.getElementsByClassName("fpts/min");
const resultDiv = document.getElementById("result");

myButton.addEventListener("click", async () => {
    try {
        const response = await fetch(`/pull5`);
        const data = await response.json();
        if (data.error) {
            alert(data.error);
        } else {
            for (let i = 0; i < data.length; i++) {
                resultDiv.innerHTML += `
                    <div class="card">
                        <div class="float_left player_name">
                            ${data[i].name}
                        </div>
                        <div class="titles">
                            <strong>Average FPTS/MIN:</strong>
                        </div>
                        <div class="stats">
                            ${data[i]["avg_fpts/min"]}
                        </div>
                    </div>
                `;
            }
        }
    } catch (error) {
        alert(error);
    }
});
