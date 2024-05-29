sortable('#functionList', {
    copy: true,
    acceptFrom: false
});
sortable('#newScheduleList', {
    acceptFrom: '#functionList, #newScheduleList',
    itemSerializer: (item) => {
        return item.node.innerText
    }
});

function showScheduler() {
    document.getElementById("scheduleMaker").style.display = "block";
}

function submitSchedule() {
    const scheduleData = sortable('#newScheduleList','serialize')[0]['items'];

    const settings = {
        "url": "http://localhost:5000/scheduler",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        "data": {
            "schedule": JSON.stringify(scheduleData)
        }
    };

    $.ajax(settings).done(function (response) {
        document.getElementById("scheduleMaker").style.display = "none";
        document.getElementById("newScheduleList").innerHTML = '';
    });
}
