const default_option = {
    text: "This is a toast",
    duration: 3000,
}

function showToast(text ,options=default_option){
    if(typeof text !== "string"){
        text = JSON.stringify(text)
    }
    options.text = text
    Toastify(options).showToast();
}
