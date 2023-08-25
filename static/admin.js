document.querySelector("form").addEventListener("click", function() {
    let type_action = document.querySelector("#type-action");
    type_action.setCustomValidity("");

    if (type_action.value != "none") {
        document.querySelectorAll("#select > *").forEach(function(e) {
            e.style.display="none";
            e.setCustomValidity("");
        });

        document.querySelector(`#${type_action.value}-action`).style.display = "block";
    }
});

document.querySelector("form").addEventListener("submit", function(e) {
    e.preventDefault();

    let type_action = document.querySelector("#type-action");
    let id = document.querySelector("#id");
    let admin = document.querySelector(`#admin`);

    type_action.setCustomValidity("");
    id.setCustomValidity("");
    admin.setCustomValidity("");

    if (type_action.value == "none") {
        type_action.setCustomValidity("Fill in the required fields");
        type_action.reportValidity();
        return false;
    }
    else if (id.value ==  "") {
        id.setCustomValidity("Fill in the required fields");
        id.reportValidity();
        return false;
    }
    else if (admin.value ==  "") {
        admin.setCustomValidity("Fill in the required fields");
        admin.reportValidity();
        return false;
    }

    let action = document.querySelector(`#${type_action.value}-action`);
    action.setCustomValidity("");

    if (action.value == "none") {
        action.setCustomValidity("Fill in the required fields");
        action.reportValidity();
        return false;
    }

    document.querySelector("form").submit();
});

document.querySelector("#id").oninput = async function() {
    await fetch("/utils/id/"+document.querySelector("#id").value).then((response) => response.json()).then((js) => {
        document.querySelector("#fid").value = js["id"];
    });
};