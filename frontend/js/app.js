const askButton = document.getElementById("askButton");

const promptInput = document.getElementById("promptInput");

const resultSection = document.getElementById("resultSection");

const status = document.getElementById("status");

const riskScore = document.getElementById("riskScore");

const jailbreak =
    document.getElementById("jailbreak");

const injection =
    document.getElementById("injection");

const hallucinationScore =
    document.getElementById("hallucinationScore");

const consistency =
    document.getElementById("consistency");

const aiResponse =
    document.getElementById("aiResponse");

const explanation =
    document.getElementById("explanation");


askButton.addEventListener("click", async () => {

    const prompt = promptInput.value.trim();


    if (!prompt) {

        alert("Please enter a prompt first.");

        return;
    }


    askButton.disabled = true;

    askButton.textContent = "Analyzing...";


    try {

        const response = await fetch(
            "https://safeguard-ai-zk8v.onrender.com/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    prompt: prompt
                })
            }
        );


        const data = await response.json();

        console.log("Backend Response:", data);


        // Show result section

        resultSection.style.display = "block";


        // -------------------------
        // STATUS
        // -------------------------

        status.textContent = data.status;


        if (data.status === "SAFE") {

            status.classList.remove("blocked");

            status.classList.add("safe");

        } else {

            status.classList.remove("safe");

            status.classList.add("blocked");

        }


        // -------------------------
        // RISK SCORE
        // -------------------------

        riskScore.textContent =
            data.safety.risk_score + "/100";


        // -------------------------
        // JAILBREAK
        // -------------------------

        if (data.safety.jailbreak_detected) {

            jailbreak.textContent = "Detected";

            jailbreak.classList.add("danger");

        } else {

            jailbreak.textContent = "Not Detected";

            jailbreak.classList.remove("danger");

        }


        // -------------------------
        // PROMPT INJECTION
        // -------------------------

        if (data.safety.prompt_injection_detected) {

            injection.textContent = "Detected";

            injection.classList.add("danger");

        } else {

            injection.textContent = "Not Detected";

            injection.classList.remove("danger");

        }


        // -------------------------
        // AI RESPONSE
        // -------------------------

        aiResponse.textContent =
            data.response;


        // -------------------------
        // HALLUCINATION
        // -------------------------

        if (data.hallucination) {

            hallucinationScore.textContent =
                data.hallucination.hallucination_score + "/100";


            consistency.textContent =
                data.hallucination.factual_consistency;


            explanation.textContent =
                data.hallucination.explanation;

        } else {

            hallucinationScore.textContent = "N/A";

            consistency.textContent = "N/A";

            explanation.textContent =
                "Prompt was blocked by the safety scanner.";

        }

    }


    catch (error) {

        console.error("Error:", error);

        resultSection.style.display = "block";

        status.textContent = "ERROR";

        explanation.textContent =
            "Unable to connect to SafeGuard AI backend.";

    }


    askButton.disabled = false;

    askButton.textContent = "Analyze Prompt";

});