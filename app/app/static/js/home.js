const minutes = document.querySelector("#minutes");
const seconds = document.querySelector("#seconds");
const model = document.querySelector("#model");
const max_token = document.querySelector("#max-token");
const loading = document.querySelector("#loading");
const submit = document.querySelector("#submit-button");
const new_chat = document.querySelector("#new-chat");
const chat_space = document.querySelector("#chat-space");
const summarize = document.querySelector("#summarize");
const system = document.querySelector("#system");

let timelimit = 30 * 60;
let startTime = Date.now();
let elapsed = 0;
let remainingTime = timelimit;
let remainingMinutes = Math.floor(remainingTime / 60);
let remainingSeconds = remainingTime - remainingMinutes * 60;
let token_dict = {
    "gpt-3.5-turbo-1106":16385,
    "gpt-4-0613":8192,
    "gpt-4-32k-0613":32768,
    "gpt-4-1106-preview":128000
}

minutes.textContent = remainingMinutes;
seconds.textContent = remainingSeconds;

let intervalId = setInterval(() => {
    remainingTime = timelimit;
    elapsed = Date.now() - startTime;
    elapsed = Math.floor(elapsed/1000);
    remainingTime = remainingTime - elapsed;
    if (remainingTime < 0) {remainingTime = 0;}
    remainingMinutes = Math.floor(remainingTime / 60);
    minutes.textContent = remainingMinutes;
    seconds.textContent = remainingTime - remainingMinutes * 60;
}, 1000)

//model.addEventListener("change", () => {
//    max_token.value = token_dict[model.value];
//})

submit.addEventListener("click", e => {
    const target = e.target;
    setTimeout( () => target.disabled = true );
    submit.classList.add("hidden");
    new_chat.classList.add("hidden");
    loading.classList.remove("hidden");
    chat_space.classList.add("hidden");
    summarize.classList.add("hidden");
})

summarize.addEventListener("click",()=>{
    system.textContent = "Please summarize the following conversation log for a meeting. Please summarize i bullet points. If any action is needed, please define who handle it. Please cover all topics in the conversation.";
    model.options[3].setAttribute("selected","selected");
})