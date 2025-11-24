// const playerCard = document.getElementsByClassName("card")
const myButton = document.getElementById("test");
const player_name = document.getElementsByClassName("player_name");
const fpts = document.getElementsByClassName("fpts/min");
const resultDiv = document.getElementById("result");

myButton.addEventListener("click", async () => {
    try {
        const response = await fetch(`/getBron`);
        const data = await response.json();
        if (data.error) {
            alert(data.error);
        } else {
            resultDiv.innerHTML = `
                <div class="card">
                    <strong>Name: </strong>${data.name}<br>
                    <strong>Average FPTS: </strong>${data.avg_fpts}<br>
                </div>
            `;
        }
    } catch (error) {
        alert(error);
    }
});
