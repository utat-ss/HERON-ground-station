$('#functionModal').on('show.bs.modal', function(e) {
    const functionId = $(e.relatedTarget).data('func-id');
    const chosenFunction = functions[functionId];

    $('#func-name-label').text(chosenFunction.name);
    $('#func-desc').text(chosenFunction.description);

    const numArgs = chosenFunction.arguments.length;

    switch(numArgs) {
        case 0: document.getElementById("argblocker").style.display = "none";
                break;
        case 1: document.getElementById("argblocker").style.display = "none";
                document.getElementById("arg2blocker").style.display = "block";

                document.getElementById("arg1label").textContent = chosenFunction.arguments[0].name + ":";
                document.getElementById("arg1Desc").innerHTML = chosenFunction.arguments[0].description;
                break;
        case 2: document.getElementById("argblocker").style.display = "block";
                document.getElementById("arg2blocker").style.display = "block ";

                document.getElementById("arg1label").textContent = chosenFunction.arguments[0].name + ":";
                document.getElementById("arg1Desc").innerHTML = chosenFunction.arguments[0].description;
                document.getElementById("arg2label").textContent = chosenFunction.arguments[1].name + ":";
                document.getElementById("arg2Desc").innerHTML = chosenFunction.arguments[1].description;
                break;
    }

    currFuncId = functionId;
});

function submitForm() {
    document.getElementById("hiddenField").value = currFuncId;
    document.getElementById("functionForm").submit();

    document.getElementById("arg1").value = "";
    document.getElementById("arg2").value = "";
}
