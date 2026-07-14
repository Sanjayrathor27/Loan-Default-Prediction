document.getElementById("predictForm").addEventListener("submit", function(e) {
    e.preventDefault();

    let formData = new FormData(this);
    let data = {};

    formData.forEach((value, key) => {
        if (!isNaN(value)) {
            data[key] = Number(value);
        } else {
            data[key] = value.toLowerCase().trim();
        }
    });

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        const box = document.getElementById("result");

        if (result.error) {
            box.style.background = "#fee2e2";
            box.style.color = "#991b1b";
            box.innerText = result.error;
        } else if (result.prediction === 1) {
            box.style.background = "#fee2e2";
            box.style.color = "#991b1b";
            box.innerHTML = "⚠️ High Risk of Loan Default<br>Probability: " + result.probability;
        } else {
            box.style.background = "#dcfce7";
            box.style.color = "#166534";
            box.innerHTML = "✅ Low Risk of Loan Default<br>Probability: " + result.probability;
        }
    });
});
